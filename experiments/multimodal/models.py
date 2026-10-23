"""
DeepShield AI — Multimodal Audio-Visual Fusion Engine
Implements:
1. DecoupledAsymmetricFusion (DeepShield Contribution 3):
   - Computes unimodal risk scores s_v and s_a
   - Computes cross-modal dissonance penalty d_av = |s_v - s_a|
   - Dynamic modality dropout & seamless single-modality fallback
2. NaiveJointConcatenation (Baseline):
   - Concatenates visual and audio embeddings into a single MLP.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict, Optional


class NaiveJointConcatenation(nn.Module):
    """
    Baseline multimodal architecture:
    Directly concatenates visual feature vector f_v and audio feature vector f_a
    into a joint multi-layer perceptron.
    Fails when one modality is missing (requires zero-padding or imputing).
    Suffers from visual dominance on audio-only fakes (RF).
    """
    def __init__(self, visual_dim: int = 128, audio_dim: int = 128, hidden_dim: int = 64):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(visual_dim + audio_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, f_v: torch.Tensor, f_a: Optional[torch.Tensor] = None) -> torch.Tensor:
        if f_a is None:
            f_a = torch.zeros_like(f_v)
        joint = torch.cat([f_v, f_a], dim=-1)
        return self.fc(joint)

    def predict_proba(self, f_v: torch.Tensor, f_a: Optional[torch.Tensor] = None) -> torch.Tensor:
        return torch.sigmoid(self.forward(f_v, f_a))


class DecoupledAsymmetricFusion(nn.Module):
    """
    DeepShield Proposed Multimodal Architecture (Contribution 3):
    1. Ingests unimodal risk scores (or logits) s_v and s_a.
    2. Computes an explicit cross-modal representation dissonance penalty:
       d_av = |s_v - s_a|
    3. Fuses scores using an asymmetric gated risk function:
       P_fake = max(s_v, s_a, sigma(w_v * s_v + w_a * s_a + w_d * d_av + b))
    4. Guarantees 100% graceful unimodal fallback when either audio or video is absent!
    """
    def __init__(self, visual_dim: int = 128, audio_dim: int = 128):
        super().__init__()
        # Unimodal calibration linear heads (if raw embeddings passed)
        self.visual_head = nn.Linear(visual_dim, 1)
        self.audio_head = nn.Linear(audio_dim, 1)

        # Cross-modal dissonance gate
        self.dissonance_gate = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(inplace=True),
            nn.Linear(16, 1),
        )

    def forward(
        self,
        f_v: Optional[torch.Tensor] = None,
        f_a: Optional[torch.Tensor] = None,
        s_v: Optional[torch.Tensor] = None,
        s_a: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Returns:
            fused_logit: Final decision logit
            s_v: Visual stream probability
            s_a: Audio stream probability
        """
        # If embeddings passed, compute unimodal logits
        if s_v is None and f_v is not None:
            s_v = torch.sigmoid(self.visual_head(f_v))
        if s_a is None and f_a is not None:
            s_a = torch.sigmoid(self.audio_head(f_a))

        # Handle Single-Modality Fallbacks
        if s_v is None and s_a is not None:
            # Video absent (audio-only file)
            dummy_s_v = torch.zeros_like(s_a)
            return torch.logit(s_a, eps=1e-6), dummy_s_v, s_a

        if s_a is None and s_v is not None:
            # Audio absent (silent video or still image)
            dummy_s_a = torch.zeros_like(s_v)
            return torch.logit(s_v, eps=1e-6), s_v, dummy_s_a

        # Both modalities present: compute cross-modal dissonance
        d_av = torch.abs(s_v - s_a)
        combined_features = torch.cat([s_v, s_a, d_av], dim=-1)
        gate_logit = self.dissonance_gate(combined_features)
        gate_prob = torch.sigmoid(gate_logit)

        # Asymmetric Max-Risk Fusion: If either stream indicates a manipulation,
        # or if the cross-modal dissonance is significant, flag as fake!
        max_unimodal = torch.maximum(s_v, s_a)
        fused_prob = torch.maximum(max_unimodal, gate_prob)
        fused_prob = torch.clamp(fused_prob, 1e-6, 1.0 - 1e-6)
        fused_logit = torch.logit(fused_prob)

        return fused_logit, s_v, s_a

    def predict_proba(
        self,
        f_v: Optional[torch.Tensor] = None,
        f_a: Optional[torch.Tensor] = None,
        s_v: Optional[torch.Tensor] = None,
        s_a: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        fused_logit, _, _ = self.forward(f_v=f_v, f_a=f_a, s_v=s_v, s_a=s_a)
        return torch.sigmoid(fused_logit)
