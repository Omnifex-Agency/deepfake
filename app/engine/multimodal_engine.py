"""
DeepShield AI — Production Multimodal Forensic Engine
Coordinates:
1. ImageDetector (Contribution 1: Adaptive 2D Gabor Residuals + Spatial Attention)
2. AudioDetector (Contribution 2: Multi-Scale SE ResNet)
3. DecoupledAsymmetricFusion (Contribution 3: Asymmetric Max-Risk Gating + Cross-Modal Dissonance)
Provides:
- FakeAVCeleb 4-Quadrant Classification (RR, FR, RF, FF)
- Cross-Modal Dissonance Penalty d_av = |s_v - s_a|
- Temporal Frame Risk Timeline
- 100% Graceful Single-Modality Fallback (Video-Only / Audio-Only)
"""

import os
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List, Optional, Union

import torch

from app.engine.image_detector import ImageDetector
from app.engine.audio_detector import AudioDetector
from experiments.multimodal.models import DecoupledAsymmetricFusion


class MultimodalEngine:
    """
    Unified multimodal forensic orchestration engine.
    """
    def __init__(
        self,
        image_ckpt: str = "experiments/image/checkpoints/deepshield_best.pt",
        audio_ckpt: str = "experiments/audio/checkpoints/whisper_specrnet_best.pt",
        fusion_ckpt: str = "experiments/multimodal/checkpoints/deepshield_fusion.pt",
        device: str = "cpu",
    ):
        self.device = torch.device(device)
        self.image_detector = ImageDetector(checkpoint_path=image_ckpt, device=device)
        self.audio_detector = AudioDetector(checkpoint_path=audio_ckpt, device=device)

        self.fusion_model = DecoupledAsymmetricFusion(visual_dim=128, audio_dim=128).to(self.device)
        self._load_fusion_checkpoint(fusion_ckpt)
        self.fusion_model.eval()

    def _load_fusion_checkpoint(self, checkpoint_path: str):
        if not os.path.exists(checkpoint_path):
            print(f"[Warning] Multimodal checkpoint '{checkpoint_path}' not found; using initialized weights.")
            return

        ckpt = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        self.fusion_model.load_state_dict(ckpt, strict=False)
        print(f"[MultimodalEngine] Loaded fusion model from '{checkpoint_path}'.")

    def analyze_image(self, pil_image: Image.Image) -> Dict[str, Any]:
        """
        Processes single image file with single-modality fallback.
        """
        img_res = self.image_detector.detect(pil_image)
        s_v = torch.tensor([[img_res["calibrated_probability"]]], dtype=torch.float32).to(self.device)

        with torch.no_grad():
            fused_logit, _, _ = self.fusion_model(s_v=s_v, s_a=None)
            fused_prob = torch.sigmoid(fused_logit).item()

        return {
            "mode": "image_only",
            "overall_risk_label": img_res["risk_label"],
            "overall_risk_color": img_res["risk_color"],
            "verdict": img_res["verdict"],
            "joint_calibrated_probability": round(fused_prob, 4),
            "visual_risk_score": img_res["calibrated_probability"],
            "audio_risk_score": None,
            "cross_modal_dissonance": 0.0,
            "quadrant": "FR" if fused_prob >= 0.5 else "RR",
            "quadrant_description": "Single-frame visual forensic inspection (audio stream absent).",
            "image_forensics": img_res,
            "audio_forensics": None,
            "temporal_timeline": None,
        }

    def analyze_audio(self, audio_source: Union[str, bytes, np.ndarray]) -> Dict[str, Any]:
        """
        Processes single audio file with single-modality fallback.
        """
        aud_res = self.audio_detector.detect(audio_source)
        s_a = torch.tensor([[aud_res["calibrated_probability"]]], dtype=torch.float32).to(self.device)

        with torch.no_grad():
            fused_logit, _, _ = self.fusion_model(s_v=None, s_a=s_a)
            fused_prob = torch.sigmoid(fused_logit).item()

        return {
            "mode": "audio_only",
            "overall_risk_label": aud_res["risk_label"],
            "overall_risk_color": aud_res["risk_color"],
            "verdict": aud_res["verdict"],
            "joint_calibrated_probability": round(fused_prob, 4),
            "visual_risk_score": None,
            "audio_risk_score": aud_res["calibrated_probability"],
            "cross_modal_dissonance": 0.0,
            "quadrant": "RF" if fused_prob >= 0.5 else "RR",
            "quadrant_description": "Acoustic voice clone inspection (visual stream absent).",
            "image_forensics": None,
            "audio_forensics": aud_res,
            "temporal_timeline": None,
        }

    def analyze_video(
        self,
        video_path: str,
        audio_source: Optional[Union[str, bytes, np.ndarray]] = None,
        max_sampled_frames: int = 12,
    ) -> Dict[str, Any]:
        """
        Extracts keyframes from video, samples timeline, evaluates audio (if provided),
        and applies Decoupled Asymmetric Fusion.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Unable to open video stream at: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = max(float(cap.get(cv2.CAP_PROP_FPS)), 1.0)
        duration_sec = total_frames / fps

        # Uniformly sample frame indices
        n_samples = min(max_sampled_frames, max(1, total_frames))
        sample_indices = np.linspace(0, max(0, total_frames - 1), n_samples, dtype=int)

        frame_timeline = []
        peak_frame_score = -1.0
        peak_image_report = None
        frame_scores = []

        for f_idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(f_idx))
            ret, bgr_frame = cap.read()
            if not ret or bgr_frame is None:
                continue

            rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(rgb_frame)
            frame_res = self.image_detector.detect(pil_frame)

            prob = frame_res["calibrated_probability"]
            frame_scores.append(prob)
            timestamp = round(float(f_idx) / fps, 2)

            frame_timeline.append({
                "frame_index": int(f_idx),
                "timestamp_sec": timestamp,
                "probability": prob,
                "risk_label": frame_res["risk_label"],
            })

            if prob > peak_frame_score:
                peak_frame_score = prob
                peak_image_report = frame_res

        cap.release()

        # Aggregate visual risk: robust 85th percentile to catch transient face swaps
        if len(frame_scores) > 0:
            s_v_val = float(np.percentile(frame_scores, 85))
        else:
            s_v_val = 0.50

        # Evaluate audio stream if present
        aud_res = None
        s_a_val = None
        if audio_source is not None:
            try:
                aud_res = self.audio_detector.detect(audio_source)
                s_a_val = aud_res["calibrated_probability"]
            except Exception as e:
                print(f"[Warning] Audio analysis encountered error: {e}")

        # Decoupled Asymmetric Fusion
        tensor_sv = torch.tensor([[s_v_val]], dtype=torch.float32).to(self.device)
        tensor_sa = torch.tensor([[s_a_val]], dtype=torch.float32).to(self.device) if s_a_val is not None else None

        with torch.no_grad():
            fused_logit, _, _ = self.fusion_model(s_v=tensor_sv, s_a=tensor_sa)
            fused_prob = torch.sigmoid(fused_logit).item()

        # Cross-modal representation dissonance
        if s_a_val is not None:
            d_av = abs(s_v_val - s_a_val)
        else:
            d_av = 0.0

        # Determine FakeAVCeleb quadrant
        is_v_fake = s_v_val >= 0.5
        is_a_fake = (s_a_val >= 0.5) if s_a_val is not None else False

        if not is_v_fake and not is_a_fake:
            quadrant = "RR"
            quad_desc = "Authentic Video & Audio — Both streams verified natural."
        elif is_v_fake and not is_a_fake:
            quadrant = "FR"
            quad_desc = "Fake Video + Authentic Audio — Targeted Face Swap / Expression Synthesis detected."
        elif not is_v_fake and is_a_fake:
            quadrant = "RF"
            quad_desc = "Authentic Video + Fake Audio — Voice Cloning / Speech Synthesis manipulation detected."
        else:
            quadrant = "FF"
            quad_desc = "Full Synthetic AV Deepfake — Both visual and acoustic streams manipulated."

        # Risk categorization
        if fused_prob < 0.35:
            risk_label = "AUTHENTIC"
            risk_color = "#10B981"
            verdict = "Both visual keyframes and acoustic harmonics exhibit authentic physiological consistency."
        elif fused_prob <= 0.65:
            risk_label = "UNCERTAIN"
            risk_color = "#F59E0B"
            verdict = "Discrepancy or subtle artifacts observed between video keyframes and audio stream. Expert review recommended."
        else:
            risk_label = "SYNTHETIC"
            risk_color = "#EF4444"
            verdict = f"Deepfake detected in quadrant [{quadrant}]. High forensic risk score with structural anomalies."

        return {
            "mode": "multimodal_video",
            "overall_risk_label": risk_label,
            "overall_risk_color": risk_color,
            "verdict": verdict,
            "joint_calibrated_probability": round(fused_prob, 4),
            "visual_risk_score": round(s_v_val, 4),
            "audio_risk_score": round(s_a_val, 4) if s_a_val is not None else None,
            "cross_modal_dissonance": round(d_av, 4),
            "quadrant": quadrant,
            "quadrant_description": quad_desc,
            "video_metadata": {
                "total_frames": total_frames,
                "fps": round(fps, 2),
                "duration_seconds": round(duration_sec, 2),
                "sampled_frames_count": len(frame_timeline),
            },
            "temporal_timeline": frame_timeline,
            "peak_frame_forensics": peak_image_report,
            "audio_forensics": aud_res,
        }
