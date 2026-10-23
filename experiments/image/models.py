"""
DeepShield AI — Forensic Model Zoo
Implements candidate architectures for Image Deepfake Detection:
1. EfficientNetB0Detector (Lightweight baseline)
2. MesoInception4Detector (Established specialized forensic baseline)
3. ResNet50Detector (Standard forensic CNN baseline)
4. AdaptiveSpatialFrequencyDetector (DeepShield Novel Proposed Contribution 1)
Plus TemperatureScaler for post-hoc ECE calibration.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from typing import Tuple, Dict, Optional


# ============================================================================
# 1. Post-Hoc Temperature Scaler for Probability Calibration
# ============================================================================

class TemperatureScaler(nn.Module):
    """
    Learns a single scalar temperature T > 0 to calibrate logits:
    p = sigmoid(logit / T)
    Optimized via Negative Log-Likelihood (NLL) on a held-out validation set.
    """
    def __init__(self):
        super().__init__()
        self.temperature = nn.Parameter(torch.ones(1) * 1.5)

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        # Constrain temperature to be strictly positive
        temp = torch.clamp(self.temperature, min=0.01)
        return logits / temp

    def fit(self, val_logits: torch.Tensor, val_labels: torch.Tensor, max_iter: int = 50, lr: float = 0.01):
        """Fits temperature on validation logits and labels via LBFGS or Adam."""
        val_logits = val_logits.detach()
        val_labels = val_labels.detach().float()
        optimizer = torch.optim.LBFGS([self.temperature], lr=lr, max_iter=max_iter)
        bce_loss = nn.BCEWithLogitsLoss()

        def eval_loss():
            optimizer.zero_grad()
            scaled_logits = self.forward(val_logits)
            loss = bce_loss(scaled_logits.squeeze(), val_labels)
            loss.backward()
            return loss

        optimizer.step(eval_loss)
        return float(self.temperature.item())


# ============================================================================
# 2. Model 1: Lightweight Baseline — EfficientNet-B0 Detector
# ============================================================================

class EfficientNetB0Detector(nn.Module):
    """
    Lightweight, high-speed deepfake detector based on EfficientNet-B0.
    Inverted residual bottleneck blocks with Squeeze-and-Excitation.
    Total parameters: ~4.0M - 5.3M. Suitable for edge and mobile deployment.
    """
    def __init__(self, pretrained: bool = True, dropout: float = 0.3):
        super().__init__()
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        backbone = models.efficientnet_b0(weights=weights)
        self.features = backbone.features
        self.avgpool = backbone.avgpool
        in_features = backbone.classifier[1].in_features

        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout, inplace=True),
            nn.Linear(in_features, 128),
            nn.BatchNorm1d(128),
            nn.SiLU(inplace=True),
            nn.Dropout(p=dropout / 2),
            nn.Linear(128, 1),
        )
        self.temperature_scaler = TemperatureScaler()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Returns raw logit for Fake class."""
        feat = self.features(x)
        feat = self.avgpool(feat)
        feat = torch.flatten(feat, 1)
        logits = self.classifier(feat)
        return logits

    def predict_proba(self, x: torch.Tensor, calibrated: bool = True) -> torch.Tensor:
        """Returns calibrated probability in [0, 1]."""
        logits = self.forward(x)
        if calibrated:
            logits = self.temperature_scaler(logits)
        return torch.sigmoid(logits)


# ============================================================================
# 3. Model 2: Established Baseline — MesoInception-4 Forensic Detector
# ============================================================================

class MesoInceptionBlock(nn.Module):
    """Inception block with dual dilated receptive fields as in Afchar et al."""
    def __init__(self, in_channels: int, a1: int, b1: int, b2: int):
        super().__init__()
        self.branch1 = nn.Sequential(
            nn.Conv2d(in_channels, a1, kernel_size=1, padding=0),
            nn.BatchNorm2d(a1),
            nn.ReLU(inplace=True),
        )
        self.branch2 = nn.Sequential(
            nn.Conv2d(in_channels, b1, kernel_size=1, padding=0),
            nn.BatchNorm2d(b1),
            nn.ReLU(inplace=True),
            nn.Conv2d(b1, b2, kernel_size=3, padding=1),
            nn.BatchNorm2d(b2),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out1 = self.branch1(x)
        out2 = self.branch2(x)
        return torch.cat([out1, out2], dim=1)


class MesoInception4Detector(nn.Module):
    """
    MesoInception-4: A specialized compact forensic CNN focusing on meso-scale
    facial texture anomalies (Afchar et al., IEEE WIFS 2018).
    Total parameters: ~28,000 (extremely lightweight).
    """
    def __init__(self, in_channels: int = 3):
        super().__init__()
        self.inc1 = MesoInceptionBlock(in_channels, 1, 4, 4)
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.inc2 = MesoInceptionBlock(5, 2, 4, 4)
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv3 = nn.Sequential(
            nn.Conv2d(6, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(16, 16, kernel_size=5, padding=2),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=4, stride=4),
        )

        self.dropout = nn.Dropout(0.5)
        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))
        self.fc1 = nn.Linear(16 * 4 * 4, 16)
        self.leaky_relu = nn.LeakyReLU(0.1)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.maxpool1(self.inc1(x))
        x = self.maxpool2(self.inc2(x))
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.adaptive_pool(x)
        x = torch.flatten(x, 1)
        x = self.dropout(x)
        x = self.leaky_relu(self.fc1(x))
        x = self.dropout(x)
        logits = self.fc2(x)
        return logits

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.forward(x))


# ============================================================================
# 4. Model 3: ResNet-50 Forensic Baseline (Wang et al. Style)
# ============================================================================

class ResNet50Detector(nn.Module):
    """
    Standard deep residual network for synthetic artifact detection (Wang et al., CVPR 2020).
    Total parameters: ~23.5M. Canonical research comparison standard.
    """
    def __init__(self, pretrained: bool = True):
        super().__init__()
        weights = models.ResNet50_Weights.DEFAULT if pretrained else None
        backbone = models.resnet50(weights=weights)
        self.conv1 = backbone.conv1
        self.bn1 = backbone.bn1
        self.relu = backbone.relu
        self.maxpool = backbone.maxpool
        self.layer1 = backbone.layer1
        self.layer2 = backbone.layer2
        self.layer3 = backbone.layer3
        self.layer4 = backbone.layer4
        self.avgpool = backbone.avgpool
        self.fc = nn.Linear(backbone.fc.in_features, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        logits = self.fc(x)
        return logits

    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.forward(x))


# ============================================================================
# 5. Model 4: DeepShield Novel Proposed Architecture (Contribution 1)
#    Adaptive Spatial-Frequency Gated Fusion Network
# ============================================================================

class Learnable2DGaborFilter(nn.Module):
    """
    Learnable 2D Gabor Filterbank extracting high-frequency spatial residuals
    and synthetic interpolation phase traces.
    """
    def __init__(self, in_channels: int = 3, n_filters: int = 16, kernel_size: int = 7):
        super().__init__()
        self.in_channels = in_channels
        self.n_filters = n_filters
        self.kernel_size = kernel_size
        self.padding = kernel_size // 2

        # Initialize learnable Gabor parameters
        self.sigma = nn.Parameter(torch.linspace(1.5, 4.0, n_filters))
        self.theta = nn.Parameter(torch.linspace(0, math.pi, n_filters))
        self.lambd = nn.Parameter(torch.linspace(2.0, 6.0, n_filters))
        self.gamma = nn.Parameter(torch.ones(n_filters) * 0.5)

        # Coordinate grid
        d = kernel_size // 2
        y, x = torch.meshgrid(
            torch.arange(-d, d + 1, dtype=torch.float32),
            torch.arange(-d, d + 1, dtype=torch.float32),
            indexing="ij"
        )
        self.register_buffer("grid_x", x.clone().contiguous(), persistent=False)
        self.register_buffer("grid_y", y.clone().contiguous(), persistent=False)

    def _generate_kernels(self) -> torch.Tensor:
        """Constructs Gabor filter kernels from parameters."""
        kernels = []
        for i in range(self.n_filters):
            sig = torch.clamp(self.sigma[i], min=0.5)
            theta = self.theta[i]
            lamb = torch.clamp(self.lambd[i], min=1.0)
            gam = torch.clamp(self.gamma[i], min=0.1, max=1.0)

            # Rotation
            x_theta = self.grid_x * torch.cos(theta) + self.grid_y * torch.sin(theta)
            y_theta = -self.grid_x * torch.sin(theta) + self.grid_y * torch.cos(theta)

            # Gabor equation
            gaussian = torch.exp(-0.5 * (x_theta**2 + (gam**2) * (y_theta**2)) / (sig**2))
            sinusoid = torch.cos(2.0 * math.pi * x_theta / lamb)
            kernel = gaussian * sinusoid

            # Zero-mean normalization to ensure high-pass residual filter
            kernel = kernel - torch.mean(kernel)
            norm = torch.sqrt(torch.sum(kernel**2) + 1e-8)
            kernel = kernel / norm
            kernels.append(kernel)

        kernel_tensor = torch.stack(kernels, dim=0)  # [n_filters, K, K]
        # Repeat across input channels
        kernel_tensor = kernel_tensor.unsqueeze(1).repeat(1, self.in_channels, 1, 1)
        return kernel_tensor

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        kernels = self._generate_kernels()
        return F.conv2d(x, kernels, padding=self.padding)


class GatedCrossAttentionFusion(nn.Module):
    """
    Gated Cross-Attention mechanism fusing spatial appearance features
    with frequency residual features.
    """
    def __init__(self, dim: int):
        super().__init__()
        self.query = nn.Linear(dim, dim)
        self.key = nn.Linear(dim, dim)
        self.value = nn.Linear(dim, dim)
        self.gate = nn.Sequential(
            nn.Linear(dim * 2, dim),
            nn.Sigmoid(),
        )
        self.scale = 1.0 / math.sqrt(dim)

    def forward(self, spatial_feat: torch.Tensor, freq_feat: torch.Tensor) -> torch.Tensor:
        # Cross-attention: Spatial queries attend to Frequency keys/values
        q = self.query(spatial_feat)
        k = self.key(freq_feat)
        v = self.value(freq_feat)

        attn_score = torch.sum(q * k, dim=-1, keepdim=True) * self.scale
        attn_weight = torch.sigmoid(attn_score)
        cross_context = attn_weight * v

        # Gated blending
        gate_input = torch.cat([spatial_feat, cross_context], dim=-1)
        g = self.gate(gate_input)
        fused = g * spatial_feat + (1.0 - g) * cross_context
        return fused


class AdaptiveSpatialFrequencyDetector(nn.Module):
    """
    DeepShield Proposed Architecture (Contribution 1):
    Dual-stream network combining:
    - Branch 1: Spatial representation encoder (EfficientNet-B0 backbone)
    - Branch 2: High-frequency learnable Gabor residual encoder
    Fused via Gated Cross-Attention to achieve invariant cross-generator detection.
    """
    def __init__(self, pretrained: bool = True, embed_dim: int = 128):
        super().__init__()
        # Spatial branch
        weights = models.EfficientNet_B0_Weights.DEFAULT if pretrained else None
        effnet = models.efficientnet_b0(weights=weights)
        self.spatial_backbone = effnet.features
        self.spatial_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.spatial_proj = nn.Linear(1280, embed_dim)

        # Frequency residual branch
        self.gabor_filterbank = Learnable2DGaborFilter(in_channels=3, n_filters=16, kernel_size=7)
        self.freq_backbone = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.freq_proj = nn.Linear(128, embed_dim)

        # Cross-attention fusion & head
        self.fusion = GatedCrossAttentionFusion(dim=embed_dim)
        self.classifier = nn.Sequential(
            nn.LayerNorm(embed_dim),
            nn.Dropout(0.3),
            nn.Linear(embed_dim, 64),
            nn.GELU(),
            nn.Dropout(0.15),
            nn.Linear(64, 1),
        )
        self.temperature_scaler = TemperatureScaler()

    def extract_features(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # Spatial stream
        s_feat = self.spatial_pool(self.spatial_backbone(x))
        s_feat = self.spatial_proj(torch.flatten(s_feat, 1))

        # Frequency stream
        gabor_residuals = self.gabor_filterbank(x)
        f_feat = self.freq_backbone(gabor_residuals)
        f_feat = self.freq_proj(torch.flatten(f_feat, 1))

        return s_feat, f_feat

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        s_feat, f_feat = self.extract_features(x)
        fused = self.fusion(s_feat, f_feat)
        logits = self.classifier(fused)
        return logits

    def predict_proba(self, x: torch.Tensor, calibrated: bool = True) -> torch.Tensor:
        logits = self.forward(x)
        if calibrated:
            logits = self.temperature_scaler(logits)
        return torch.sigmoid(logits)


def build_model(model_name: str, pretrained: bool = True) -> nn.Module:
    """Factory creating model instances by name."""
    name = model_name.lower()
    if name == "efficientnet_b0":
        return EfficientNetB0Detector(pretrained=pretrained)
    elif name == "mesoinception4":
        return MesoInception4Detector()
    elif name == "resnet50":
        return ResNet50Detector(pretrained=pretrained)
    elif name in ["adaptive_spatial_frequency", "deepshield"]:
        return AdaptiveSpatialFrequencyDetector(pretrained=pretrained)
    else:
        raise ValueError(f"Unknown model architecture: {model_name}")

