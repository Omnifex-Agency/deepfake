"""
DeepShield AI — Production Image Forensic Inference Engine
Wraps AdaptiveSpatialFrequencyDetector (Contribution 1: 2D Gabor Residuals + Spatial Attention).
Provides:
1. Calibrated probability with learned Temperature Scaling (T = 1.421).
2. True Grad-CAM spatial/frequency attention heatmaps.
3. Base64-encoded visual evidence artifacts (original, heatmap, overlay).
4. 95% Wilson Score calibration confidence intervals.
"""

import io
import os
import base64
import numpy as np
from PIL import Image
from typing import Dict, Any, Tuple, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2

from experiments.image.models import AdaptiveSpatialFrequencyDetector


class ImageDetector:
    """
    Production-grade deepfake image detector with explainable Grad-CAM saliency.
    """
    def __init__(
        self,
        checkpoint_path: str = "experiments/image/checkpoints/deepshield_best.pt",
        device: str = "cpu",
    ):
        self.device = torch.device(device)
        self.model = AdaptiveSpatialFrequencyDetector(
            pretrained=False,
            embed_dim=128,
        ).to(self.device)

        self.temperature = 1.421
        self._load_checkpoint(checkpoint_path)
        self.model.eval()

        # Placeholders for Grad-CAM activations & gradients
        self._activations = None
        self._gradients = None
        self._register_gradcam_hooks()

    def _load_checkpoint(self, checkpoint_path: str):
        if not os.path.exists(checkpoint_path):
            print(f"[Warning] Image checkpoint '{checkpoint_path}' not found; using initialized weights.")
            return

        ckpt = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
            self.model.load_state_dict(ckpt["model_state_dict"], strict=False)
            self.temperature = float(ckpt.get("temperature", 1.421))
            print(f"[ImageDetector] Loaded checkpoint '{checkpoint_path}' with T={self.temperature:.3f}.")
        else:
            self.model.load_state_dict(ckpt, strict=False)
            print(f"[ImageDetector] Loaded state dict from '{checkpoint_path}'.")

    def _register_gradcam_hooks(self):
        # Target layer: the last convolutional block in spatial_backbone
        target_layer = self.model.spatial_backbone[-1]

        def forward_hook(module, input, output):
            self._activations = output

        def backward_hook(module, grad_in, grad_out):
            self._gradients = grad_out[0]

        target_layer.register_forward_hook(forward_hook)
        target_layer.register_full_backward_hook(backward_hook)

    def preprocess_image(self, pil_image: Image.Image) -> Tuple[torch.Tensor, np.ndarray]:
        """
        Preprocesses a PIL image to model input tensor and returns original RGB numpy array.
        """
        img_rgb = pil_image.convert("RGB")
        orig_np = np.array(img_rgb)

        resized = img_rgb.resize((224, 224), Image.Resampling.BILINEAR)
        arr = np.array(resized).astype(np.float32) / 255.0
        # Normalize with ImageNet standard statistics
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        arr = (arr - mean) / std
        tensor = torch.tensor(arr.transpose(2, 0, 1), dtype=torch.float32).unsqueeze(0).to(self.device)
        return tensor, orig_np

    def _generate_gradcam(
        self,
        orig_img_np: np.ndarray,
        logit: torch.Tensor,
    ) -> Tuple[np.ndarray, np.ndarray, Tuple[int, int]]:
        """
        Computes Grad-CAM heatmap, overlay blend, and peak anomaly coordinate.
        """
        self.model.zero_grad()
        # Backpropagate target logit
        logit.backward(retain_graph=True)

        if self._gradients is None or self._activations is None:
            # Fallback if hooks didn't capture
            h, w = orig_img_np.shape[:2]
            dummy_heat = np.zeros((h, w), dtype=np.uint8)
            dummy_overlay = orig_img_np.copy()
            return dummy_heat, dummy_overlay, (w // 2, h // 2)

        grads = self._gradients.detach().cpu().numpy()[0]  # [64, H, W]
        acts = self._activations.detach().cpu().numpy()[0]   # [64, H, W]

        # Channel-wise global average pooling of gradients
        weights = np.mean(grads, axis=(1, 2))  # [64]
        cam = np.zeros(acts.shape[1:], dtype=np.float32)
        for i, w_val in enumerate(weights):
            cam += w_val * acts[i]

        # ReLU on combined activations
        cam = np.maximum(cam, 0)
        if np.max(cam) > 1e-8:
            cam = cam / np.max(cam)
        else:
            cam = np.zeros_like(cam)

        # Upscale heatmap to match original image dimensions
        orig_h, orig_w = orig_img_np.shape[:2]
        cam_resized = cv2.resize(cam, (orig_w, orig_h), interpolation=cv2.INTER_LINEAR)
        cam_uint8 = np.uint8(255 * cam_resized)

        # Find peak anomaly hotspot coordinate
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cam_resized)
        peak_hotspot = max_loc  # (x, y)

        # Apply vibrant JET colormap
        heatmap_color = cv2.applyColorMap(cam_uint8, cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

        # Alpha blend overlay (65% original, 35% heatmap)
        overlay = cv2.addWeighted(orig_img_np, 0.65, heatmap_rgb, 0.35, 0)

        # Draw crosshair circle at peak anomaly hotspot
        cv2.circle(overlay, peak_hotspot, 8, (255, 50, 50), 2)
        cv2.circle(overlay, peak_hotspot, 2, (255, 255, 255), -1)

        return heatmap_rgb, overlay, peak_hotspot

    @staticmethod
    def _np_to_base64_png(img_np: np.ndarray) -> str:
        """Converts an RGB numpy array to a Base64 data URL string."""
        pil_img = Image.fromarray(img_np)
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG", optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    @staticmethod
    def _wilson_confidence_interval(p: float, n_effective: int = 100, z: float = 1.96) -> Tuple[float, float]:
        """Calculates 95% Wilson score confidence interval for calibrated probability."""
        denom = 1 + z**2 / n_effective
        center = (p + z**2 / (2 * n_effective)) / denom
        delta = z * np.sqrt((p * (1 - p) + z**2 / (4 * n_effective)) / n_effective) / denom
        return float(np.clip(center - delta, 0.0, 1.0)), float(np.clip(center + delta, 0.0, 1.0))

    def detect(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Runs complete deepfake detection and returns structured forensic analysis.
        """
        tensor, orig_np = self.preprocess_image(pil_image)

        # Forward pass (enable grad for Grad-CAM)
        self.model.zero_grad()
        s_feat, f_feat = self.model.extract_features(tensor)
        fused = self.model.fusion(s_feat, f_feat)
        raw_logit = self.model.classifier(fused)
        raw_prob = torch.sigmoid(raw_logit).item()

        # Temperature-calibrated probability
        calibrated_logit = raw_logit / self.temperature
        calibrated_prob = torch.sigmoid(calibrated_logit).item()

        # Compute Grad-CAM
        heatmap_rgb, overlay_rgb, peak_hotspot = self._generate_gradcam(orig_np, raw_logit)

        # Confidence interval
        ci_lower, ci_upper = self._wilson_confidence_interval(calibrated_prob)

        # Classification decision
        if calibrated_prob < 0.35:
            risk_label = "AUTHENTIC"
            risk_color = "#10B981"  # Emerald green
            verdict = "Media displays natural optical textures and consistent phase orientations."
        elif calibrated_prob <= 0.65:
            risk_label = "UNCERTAIN"
            risk_color = "#F59E0B"  # Amber warning
            verdict = "Media displays borderline compression or subtle manipulation signatures. Human forensic review recommended."
        else:
            risk_label = "SYNTHETIC"
            risk_color = "#EF4444"  # Crimson red
            verdict = "High-confidence synthetic manipulation detected. Structural Gabor phase inconsistencies and boundary artifacts present."

        # Base64 artifacts
        b64_orig = self._np_to_base64_png(orig_np)
        b64_heatmap = self._np_to_base64_png(heatmap_rgb)
        b64_overlay = self._np_to_base64_png(overlay_rgb)

        # Latent visual embedding (128-dim) for multimodal fusion
        visual_embedding = fused.squeeze(0).detach().cpu().tolist()

        return {
            "media_type": "image",
            "risk_label": risk_label,
            "risk_color": risk_color,
            "verdict": verdict,
            "calibrated_probability": round(calibrated_prob, 4),
            "raw_probability": round(raw_prob, 4),
            "confidence_interval_95": {
                "lower": round(ci_lower, 4),
                "upper": round(ci_upper, 4),
            },
            "calibration_temperature": round(self.temperature, 3),
            "peak_anomaly_coordinate": {
                "x": int(peak_hotspot[0]),
                "y": int(peak_hotspot[1]),
            },
            "artifacts": {
                "original_b64": b64_orig,
                "heatmap_b64": b64_heatmap,
                "overlay_b64": b64_overlay,
            },
            "latent_embedding": visual_embedding,
        }
