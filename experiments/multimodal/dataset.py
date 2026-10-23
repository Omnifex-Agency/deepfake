"""
DeepShield AI — Multimodal Audio-Visual Dataset Engine
Generates and manages 4-quadrant multimodal evaluation datasets matching FakeAVCeleb:
- RR: Real Video + Real Audio (Binary Label: 0)
- FR: Fake Video + Real Audio (Binary Label: 1)
- RF: Real Video + Fake Audio (Binary Label: 1)
- FF: Fake Video + Fake Audio (Binary Label: 1)
"""

import os
import random
import numpy as np
from typing import List, Tuple, Dict, Optional

import torch
from torch.utils.data import Dataset, DataLoader


class MultimodalQuadrantDataset(Dataset):
    """
    Dataset containing paired visual embeddings f_v, audio embeddings f_a,
    quadrant categories ('RR', 'FR', 'RF', 'FF'), and binary label (0 if RR else 1).
    """
    def __init__(
        self,
        samples: List[Dict],
        drop_modality_prob: float = 0.0,
    ):
        """
        samples: List of dicts with keys:
            'f_v': visual feature tensor [128]
            'f_a': audio feature tensor [128]
            'quadrant': 'RR', 'FR', 'RF', or 'FF'
            'label': 0 (real) or 1 (fake)
        drop_modality_prob: Probability of masking one modality during training
        """
        self.samples = samples
        self.drop_modality_prob = drop_modality_prob

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict:
        item = self.samples[idx]
        f_v = item["f_v"].clone()
        f_a = item["f_a"].clone()
        label = item["label"]
        quadrant = item["quadrant"]

        has_v = True
        has_a = True

        if self.drop_modality_prob > 0.0:
            r = random.random()
            if r < self.drop_modality_prob / 2.0:
                has_a = False
                f_a = None
            elif r < self.drop_modality_prob:
                has_v = False
                f_v = None

        return {
            "f_v": f_v,
            "f_a": f_a,
            "has_v": has_v,
            "has_a": has_a,
            "label": label,
            "quadrant": quadrant,
        }


def generate_multimodal_quadrant_embeddings(
    n_per_quadrant: int = 50, seed: int = 42
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Generates synthetic 128-dim embeddings simulating the output of
    our Stage 3 image model and Stage 4 audio model across the 4 quadrants:
    - Real Video: centered at mu_v_real = -1.0
    - Fake Video: centered at mu_v_fake = +1.0
    - Real Audio: centered at mu_a_real = -1.0
    - Fake Audio: centered at mu_a_fake = +1.0
    Returns train_samples, val_samples, test_samples with strictly balanced quadrants.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    embed_dim = 128

    def make_samples(n):
        items = []
        for quad in ["RR", "FR", "RF", "FF"]:
            is_v_fake = quad in ["FR", "FF"]
            is_a_fake = quad in ["RF", "FF"]
            label = 0 if quad == "RR" else 1

            mu_v = 1.2 if is_v_fake else -1.2
            mu_a = 1.2 if is_a_fake else -1.2

            for _ in range(n):
                # Sample embeddings with natural intra-class variance
                v_vec = torch.randn(embed_dim) * 0.8 + mu_v
                a_vec = torch.randn(embed_dim) * 0.8 + mu_a

                # In RR and FF, audio-visual synchrony aligns (lower dissonance)
                # In FR and RF, cross-modal dissonance is elevated
                if quad in ["FR", "RF"]:
                    # Inject cross-modal desynchronization shift
                    a_vec = a_vec + torch.randn(embed_dim) * 0.4

                items.append({
                    "f_v": v_vec,
                    "f_a": a_vec,
                    "quadrant": quad,
                    "label": label,
                })
        random.shuffle(items)
        return items

    train_samples = make_samples(int(n_per_quadrant * 0.7))
    val_samples = make_samples(int(n_per_quadrant * 0.15))
    test_samples = make_samples(int(n_per_quadrant * 0.15))

    return train_samples, val_samples, test_samples
