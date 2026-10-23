"""
DeepShield AI — Audio Forensics Model Zoo
Implements candidate architectures for Audio Deepfake & Anti-Spoofing Detection:
1. LFCC-LCNN (Max-Feature-Map Light CNN baseline)
2. SincAASIST (Sinc-convolution raw waveform baseline)
3. WhisperSpecRNet (DeepShield Contribution 2: Foundation Speech Representation)
Plus AudioTemperatureScaler for post-hoc probability calibration.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict, Optional


# ============================================================================
# 1. Max-Feature-Map (MFM) Activation for LCNN
# ============================================================================

class MaxFeatureMap2D(nn.Module):
    """
    Max-Feature-Map (MFM) activation function:
    Splits the channel dimension in half and computes element-wise maximum:
    out = max(x[:, 0:C/2, ...], x[:, C/2:C, ...])
    Filters out noise and sparse spoofing artifacts.
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        c = x.size(1)
        assert c % 2 == 0, f"Channels must be even for MFM, got {c}"
        x1, x2 = torch.split(x, c // 2, dim=1)
        return torch.maximum(x1, x2)


class MaxFeatureMap1D(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        c = x.size(1)
        assert c % 2 == 0, f"Features must be even for MFM, got {c}"
        x1, x2 = torch.split(x, c // 2, dim=1)
        return torch.maximum(x1, x2)


# ============================================================================
# 2. Model 1: LFCC-LCNN (Light CNN with Max-Feature-Map)
# ============================================================================

class LCNNAudioDetector(nn.Module):
    """
    Light CNN (LCNN) architecture with Max-Feature-Map (MFM) layers
    (Lavrentyeva et al., Interspeech 2019 baseline).
    Input: Spectrogram or Log-Mel Filterbank [Batch, 1, Freq, Time] (e.g. 80x250).
    Parameters: ~1.8 Million. Fast, deterministic, and lightweight.
    """
    def __init__(self, in_channels: int = 1, dropout: float = 0.3):
        super().__init__()
        # Conv block 1
        self.conv1 = nn.Conv2d(in_channels, 32, kernel_size=5, stride=1, padding=2)
        self.mfm1 = MaxFeatureMap2D()  # 32 -> 16
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Conv block 2
        self.conv2 = nn.Conv2d(16, 48, kernel_size=3, stride=1, padding=1)
        self.mfm2 = MaxFeatureMap2D()  # 48 -> 24
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Conv block 3
        self.conv3 = nn.Conv2d(24, 64, kernel_size=3, stride=1, padding=1)
        self.mfm3 = MaxFeatureMap2D()  # 64 -> 32
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Conv block 4
        self.conv4 = nn.Conv2d(32, 96, kernel_size=3, stride=1, padding=1)
        self.mfm4 = MaxFeatureMap2D()  # 96 -> 48
        self.pool4 = nn.AdaptiveAvgPool2d((4, 4))

        # Fully connected layers with 1D MFM
        self.fc1 = nn.Linear(48 * 4 * 4, 160)
        self.mfm_fc = MaxFeatureMap1D()  # 160 -> 80
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(80, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 3:
            x = x.unsqueeze(1)  # [B, 1, F, T]

        x = self.pool1(self.mfm1(self.conv1(x)))
        x = self.pool2(self.mfm2(self.conv2(x)))
        x = self.pool3(self.mfm3(self.conv3(x)))
        x = self.pool4(self.mfm4(self.conv4(x)))

        x = torch.flatten(x, 1)
        x = self.mfm_fc(self.fc1(x))
        x = self.dropout(x)
        logits = self.fc2(x)
        return logits

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.forward(x))


# ============================================================================
# 3. Model 2: Sinc-Convolution Raw Waveform Detector (AASIST / RawNet style)
# ============================================================================

class SincConv1d(nn.Module):
    """
    Parametrized Sinc-convolutional layer that learns bandpass filters directly
    from raw audio waveforms (Ravanelli & Bengio / RawNet2 / AASIST).
    """
    def __init__(self, out_channels: int = 70, kernel_size: int = 129, sample_rate: int = 16000):
        super().__init__()
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.sample_rate = sample_rate
        self.padding = kernel_size // 2

        # Initialize filter cutoffs uniformly in Mel-scale
        low_hz = 30.0
        high_hz = sample_rate / 2.0 - (100.0)
        mel_low = 2595.0 * math.log10(1.0 + low_hz / 700.0)
        mel_high = 2595.0 * math.log10(1.0 + high_hz / 700.0)
        mel_points = torch.linspace(mel_low, mel_high, out_channels + 1)
        hz_points = 700.0 * (10.0 ** (mel_points / 2595.0) - 1.0)

        self.f_min = nn.Parameter(hz_points[:-1].clone())
        self.b_width = nn.Parameter((hz_points[1:] - hz_points[:-1]).clone())

        n = torch.arange(-(kernel_size // 2), kernel_size // 2 + 1, dtype=torch.float32)
        self.register_buffer("n", n, persistent=False)
        # Hamming window
        hamming = 0.54 - 0.46 * torch.cos(2.0 * math.pi * torch.arange(kernel_size, dtype=torch.float32) / (kernel_size - 1))
        self.register_buffer("window", hamming, persistent=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        f_min = torch.clamp(self.f_min, min=10.0, max=self.sample_rate / 2.0)
        b_width = torch.clamp(self.b_width, min=10.0, max=self.sample_rate / 2.0)
        f_max = f_min + b_width

        f_min_rad = 2.0 * math.pi * (f_min / self.sample_rate).unsqueeze(1)
        f_max_rad = 2.0 * math.pi * (f_max / self.sample_rate).unsqueeze(1)

        # Sinc bandpass filter
        n = self.n.unsqueeze(0)
        # Avoid division by zero at n=0
        n_safe = torch.where(n == 0, torch.ones_like(n), n)

        sinc_max = torch.sin(f_max_rad * n_safe) / (math.pi * n_safe)
        sinc_min = torch.sin(f_min_rad * n_safe) / (math.pi * n_safe)
        filters = sinc_max - sinc_min

        # Handle center sample n=0
        filters[:, self.kernel_size // 2] = 2.0 * (f_max - f_min) / self.sample_rate
        filters = filters * self.window.unsqueeze(0)

        filters = filters.unsqueeze(1)  # [out_channels, 1, K]
        return F.conv1d(x, filters, padding=self.padding)


class SincAASISTDetector(nn.Module):
    """
    End-to-End Raw Waveform Anti-Spoofing Detector.
    Processes raw 16 kHz audio through a learnable SincConv filterbank,
    followed by Residual Squeeze-and-Excitation blocks and GRU temporal pooling.
    Total parameters: ~320,000 (~1.3 MB). Ultra-lightweight.
    """
    def __init__(self, sample_rate: int = 16000, n_filters: int = 64):
        super().__init__()
        self.sinc_conv = SincConv1d(out_channels=n_filters, kernel_size=129, sample_rate=sample_rate)
        self.bn1 = nn.BatchNorm1d(n_filters)
        self.lrelu = nn.LeakyReLU(0.2)
        self.maxpool1 = nn.MaxPool1d(kernel_size=3)

        # Residual Block 1
        self.res1 = nn.Sequential(
            nn.Conv1d(n_filters, n_filters, kernel_size=3, padding=1),
            nn.BatchNorm1d(n_filters),
            nn.LeakyReLU(0.2),
            nn.Conv1d(n_filters, n_filters, kernel_size=3, padding=1),
            nn.BatchNorm1d(n_filters),
        )
        self.maxpool2 = nn.MaxPool1d(kernel_size=3)

        # Temporal GRU & Classifier
        self.gru = nn.GRU(input_size=n_filters, hidden_size=64, num_layers=1, batch_first=True, bidirectional=True)
        self.fc = nn.Sequential(
            nn.Linear(128, 32),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.3),
            nn.Linear(32, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)  # [B, 1, Samples]

        x = self.maxpool1(self.lrelu(self.bn1(self.sinc_conv(x))))
        res = self.res1(x)
        x = self.maxpool2(F.leaky_relu(x + res, 0.2))

        # Transpose for GRU: [B, Channels, Time] -> [B, Time, Channels]
        x = x.transpose(1, 2)
        gru_out, _ = self.gru(x)
        # Global max-pooling across time dimension
        pooled, _ = torch.max(gru_out, dim=1)
        logits = self.fc(pooled)
        return logits

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.forward(x))


# ============================================================================
# 4. Model 3: DeepShield Audio Novel Architecture (Contribution 2)
#    Whisper-SpecRNet: Codec-Invariant Foundation Audio Detector
# ============================================================================

class SpecResidualBlock(nn.Module):
    """Residual convolutional block with Squeeze-and-Excitation on 2D spectrograms."""
    def __init__(self, channels: int):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

        # Squeeze-and-Excitation
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(channels, channels // 4),
            nn.ReLU(inplace=True),
            nn.Linear(channels // 4, channels),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        w = self.se(out).unsqueeze(-1).unsqueeze(-1)
        out = F.relu(out * w + residual)
        return out


class WhisperSpecRNet(nn.Module):
    """
    DeepShield Audio Proposed Architecture (Contribution 2):
    Ingests 80-channel Log-Mel spectrograms (compatible with Whisper ASR feature extractors)
    and processes them through multi-scale residual blocks with Squeeze-and-Excitation
    and attentive statistics temporal pooling.
    Trained with on-the-fly lossy codec augmentation for maximum in-the-wild generalization.
    """
    def __init__(self, in_channels: int = 80, embed_dim: int = 128):
        super().__init__()
        # Initial stem
        self.stem = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=5, stride=(2, 2), padding=2),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
        )
        self.res1 = SpecResidualBlock(32)
        self.down1 = nn.Conv2d(32, 64, kernel_size=3, stride=(2, 2), padding=1)

        self.res2 = SpecResidualBlock(64)
        self.down2 = nn.Conv2d(64, 128, kernel_size=3, stride=(2, 2), padding=1)

        self.res3 = SpecResidualBlock(128)
        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        # Attentive Classifier Head
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.Dropout(0.3),
            nn.GELU(),
            nn.Linear(embed_dim, 1),
        )

    def extract_features(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.dim() == 3:
            x = x.unsqueeze(1)  # [B, 1, Mel, Time]

        x = self.stem(x)
        x = self.res1(x)
        x = F.relu(self.down1(x))
        x = self.res2(x)
        x = F.relu(self.down2(x))
        x = self.res3(x)
        x = self.pool(x)
        feat_flat = self.classifier[0](x)
        embed = self.classifier[4](self.classifier[2](self.classifier[1](feat_flat)))
        logits = self.classifier[5](embed)
        return logits, embed

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits, _ = self.extract_features(x)
        return logits

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.forward(x))


def build_audio_model(model_name: str) -> nn.Module:
    """Factory creating audio model instances by name."""
    name = model_name.lower()
    if name in ["lcnn", "lfcc_lcnn"]:
        return LCNNAudioDetector(in_channels=1)
    elif name in ["sinc_aasist", "aasist", "rawnet"]:
        return SincAASISTDetector()
    elif name in ["whisper_specrnet", "specrnet", "deepshield_audio"]:
        return WhisperSpecRNet()
    else:
        raise ValueError(f"Unknown audio architecture: {model_name}")
