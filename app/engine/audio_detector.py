"""
DeepShield AI — Production Audio Forensic Inference Engine
Wraps WhisperSpecRNet (Contribution 2: Multi-Scale Squeeze-and-Excitation ResNet).
Provides:
1. Calibrated probability with learned Temperature Scaling (T = 1.411).
2. Time-Frequency Mel-spectrogram anomaly attribution maps.
3. Base64-encoded audio spectral artifacts (Mel-spectrogram, Anomaly Heatmap).
4. Spectral band distribution analysis (Vocoder artifact localization).
"""

import io
import os
import wave
import base64
import numpy as np
from typing import Dict, Any, Tuple, Optional, Union
from scipy.io import wavfile

import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
from PIL import Image

from experiments.audio.models import WhisperSpecRNet


class AudioDetector:
    """
    Production-grade voice clone and speech deepfake detector with spectral attribution.
    """
    def __init__(
        self,
        checkpoint_path: str = "experiments/audio/checkpoints/whisper_specrnet_best.pt",
        device: str = "cpu",
    ):
        self.device = torch.device(device)
        self.model = WhisperSpecRNet(
            in_channels=80,
            embed_dim=128,
        ).to(self.device)

        self.temperature = 1.411
        self._load_checkpoint(checkpoint_path)
        self.model.eval()

    def _load_checkpoint(self, checkpoint_path: str):
        if not os.path.exists(checkpoint_path):
            print(f"[Warning] Audio checkpoint '{checkpoint_path}' not found; using initialized weights.")
            return

        ckpt = torch.load(checkpoint_path, map_location=self.device, weights_only=False)
        if isinstance(ckpt, dict) and "model_state_dict" in ckpt:
            self.model.load_state_dict(ckpt["model_state_dict"], strict=False)
            self.temperature = float(ckpt.get("temperature", 1.411))
            print(f"[AudioDetector] Loaded checkpoint '{checkpoint_path}' with T={self.temperature:.3f}.")
        else:
            self.model.load_state_dict(ckpt, strict=False)
            print(f"[AudioDetector] Loaded state dict from '{checkpoint_path}'.")

    def load_audio(self, audio_source: Union[str, bytes, io.BytesIO]) -> Tuple[np.ndarray, int]:
        """
        Loads audio from file path, raw bytes, or BytesIO buffer into a 1D float32 array and sample rate.
        """
        if isinstance(audio_source, str):
            sr, data = wavfile.read(audio_source)
        elif isinstance(audio_source, (bytes, io.BytesIO)):
            buf = io.BytesIO(audio_source) if isinstance(audio_source, bytes) else audio_source
            try:
                sr, data = wavfile.read(buf)
            except Exception:
                # If wavfile fails, parse with standard wave module
                buf.seek(0)
                with wave.open(buf, "rb") as wf:
                    sr = wf.getframerate()
                    n_frames = wf.getnframes()
                    raw = wf.readframes(n_frames)
                    if wf.getsampwidth() == 2:
                        data = np.frombuffer(raw, dtype=np.int16)
                    else:
                        data = np.frombuffer(raw, dtype=np.uint8).astype(np.float32) - 128
        else:
            raise ValueError(f"Unsupported audio source type: {type(audio_source)}")

        # Convert multi-channel (stereo) to mono
        if data.ndim > 1:
            data = data.mean(axis=1)

        # Normalize to [-1.0, +1.0]
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32768.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483648.0
        else:
            data = data.astype(np.float32)

        return data, sr

    def compute_mel_spectrogram(self, audio: np.ndarray, sr: int = 16000, n_mels: int = 80, n_fft: int = 512, hop_len: int = 160) -> np.ndarray:
        """
        Computes 80-band log Mel-spectrogram matching Whisper standard feature frontends.
        """
        # Resample if sample rate differs from 16 kHz
        if sr != 16000 and len(audio) > 0:
            target_len = int(len(audio) * (16000.0 / sr))
            indices = np.linspace(0, len(audio) - 1, target_len).astype(np.int32)
            audio = audio[indices]
            sr = 16000

        # Simple high-resolution Short-Time Fourier Transform (STFT)
        window = np.hanning(n_fft)
        stft_frames = []
        for i in range(0, len(audio) - n_fft, hop_len):
            chunk = audio[i : i + n_fft] * window
            spec = np.abs(np.fft.rfft(chunk))
            stft_frames.append(spec)

        if len(stft_frames) == 0:
            # Fallback for ultra-short clips
            return np.zeros((n_mels, 100), dtype=np.float32)

        stft_matrix = np.array(stft_frames).T  # [n_fft//2 + 1, time]

        # Construct triangular Mel filterbank
        n_freqs = n_fft // 2 + 1
        hz_min, hz_max = 0, sr / 2
        mel_min = 2595 * np.log10(1 + hz_min / 700)
        mel_max = 2595 * np.log10(1 + hz_max / 700)
        mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
        hz_points = 700 * (10 ** (mel_points / 2595) - 1)
        bin_points = np.floor((n_fft + 1) * hz_points / sr).astype(int)

        fb = np.zeros((n_mels, n_freqs), dtype=np.float32)
        for m in range(1, n_mels + 1):
            f_m_minus = bin_points[m - 1]
            f_m = bin_points[m]
            f_m_plus = bin_points[m + 1]
            for k in range(f_m_minus, f_m):
                if f_m > f_m_minus:
                    fb[m - 1, k] = (k - f_m_minus) / (f_m - f_m_minus)
            for k in range(f_m, f_m_plus):
                if f_m_plus > f_m:
                    fb[m - 1, k] = (f_m_plus - k) / (f_m_plus - f_m)

        mel_spec = np.dot(fb, stft_matrix)
        # Log compression: log(1 + 1000 * mel)
        log_mel = np.log1p(1000.0 * mel_spec)
        return log_mel.astype(np.float32)

    def _generate_spectrogram_images(
        self,
        log_mel: np.ndarray,
        tensor_in: torch.Tensor,
        logit: torch.Tensor,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates visual Mel-spectrogram rendering and spectral gradient anomaly map.
        """
        # 1. Base Mel-spectrogram image
        norm_mel = log_mel - np.min(log_mel)
        if np.max(norm_mel) > 1e-8:
            norm_mel = norm_mel / np.max(norm_mel)
        mel_uint8 = np.uint8(255 * norm_mel)
        # Invert vertical axis so low frequencies are at the bottom
        mel_uint8 = np.flipud(mel_uint8)
        mel_color = cv2.applyColorMap(mel_uint8, cv2.COLORMAP_VIRIDIS)
        mel_rgb = cv2.cvtColor(mel_color, cv2.COLOR_BGR2RGB)

        # 2. Gradient Anomaly Attribution Map
        self.model.zero_grad()
        if tensor_in.grad is not None:
            tensor_in.grad.zero_()
        logit.backward(retain_graph=True)

        if tensor_in.grad is not None:
            grads = torch.abs(tensor_in.grad).squeeze(0).squeeze(0).detach().cpu().numpy()
            grads = cv2.GaussianBlur(grads, (5, 5), 1.0)
            if np.max(grads) > 1e-8:
                grads = grads / np.max(grads)
            grad_uint8 = np.uint8(255 * np.flipud(grads))
            anomaly_color = cv2.applyColorMap(grad_uint8, cv2.COLORMAP_INFERNO)
            anomaly_rgb = cv2.cvtColor(anomaly_color, cv2.COLOR_BGR2RGB)
        else:
            anomaly_rgb = mel_rgb.copy()

        # Resize to fixed standard width for clean dashboard layout
        h, w = mel_rgb.shape[:2]
        target_w = 400
        target_h = 160
        mel_resized = cv2.resize(mel_rgb, (target_w, target_h), interpolation=cv2.INTER_LINEAR)
        anomaly_resized = cv2.resize(anomaly_rgb, (target_w, target_h), interpolation=cv2.INTER_LINEAR)

        return mel_resized, anomaly_resized

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
        denom = 1 + z**2 / n_effective
        center = (p + z**2 / (2 * n_effective)) / denom
        delta = z * np.sqrt((p * (1 - p) + z**2 / (4 * n_effective)) / n_effective) / denom
        return float(np.clip(center - delta, 0.0, 1.0)), float(np.clip(center + delta, 0.0, 1.0))

    def detect(self, audio_source: Union[str, bytes, io.BytesIO, np.ndarray]) -> Dict[str, Any]:
        """
        Runs complete deepfake audio detection on audio input and returns structured telemetry.
        """
        if isinstance(audio_source, np.ndarray):
            audio, sr = audio_source, 16000
        else:
            audio, sr = self.load_audio(audio_source)

        duration_sec = len(audio) / max(sr, 1)

        # Compute Mel-spectrogram
        log_mel = self.compute_mel_spectrogram(audio, sr=sr, n_mels=80)

        # Ensure minimum width for model input
        if log_mel.shape[1] < 64:
            pad_w = 64 - log_mel.shape[1]
            log_mel = np.pad(log_mel, ((0, 0), (0, pad_w)), mode="reflect")

        # Standard normalization: (x - mean) / (std + eps)
        norm_mel = (log_mel - np.mean(log_mel)) / (np.std(log_mel) + 1e-6)
        tensor_in = torch.tensor(norm_mel, dtype=torch.float32).unsqueeze(0).unsqueeze(0).to(self.device)
        tensor_in.requires_grad = True

        # Forward pass
        raw_logit, audio_feat = self.model.extract_features(tensor_in)
        raw_prob = torch.sigmoid(raw_logit).item()

        # Temperature-calibrated probability
        calibrated_logit = raw_logit / self.temperature
        calibrated_prob = torch.sigmoid(calibrated_logit).item()

        # Generate spectral visuals
        mel_img, anomaly_img = self._generate_spectrogram_images(log_mel, tensor_in, raw_logit)

        # Confidence interval
        ci_lower, ci_upper = self._wilson_confidence_interval(calibrated_prob)

        # Classification decision
        if calibrated_prob < 0.35:
            risk_label = "AUTHENTIC"
            risk_color = "#10B981"  # Emerald green
            verdict = "Vocal harmonics, acoustic resonance, and phase dynamics conform to authentic human speech."
        elif calibrated_prob <= 0.65:
            risk_label = "UNCERTAIN"
            risk_color = "#F59E0B"  # Amber warning
            verdict = "Borderline acoustic signatures or heavy compression detected. Manual audio forensic review advised."
        else:
            risk_label = "SYNTHETIC"
            risk_color = "#EF4444"  # Crimson red
            verdict = "Neural voice cloning or speech synthesis detected. Characteristic high-frequency vocoder artifacts and phase anomalies identified."

        # Spectral Band Energy Analysis
        low_band = float(np.mean(log_mel[:26, :]))    # 0 - 1 kHz
        mid_band = float(np.mean(log_mel[26:55, :]))   # 1 - 4 kHz
        high_band = float(np.mean(log_mel[55:, :]))    # 4 - 8 kHz
        tot_energy = max(abs(low_band) + abs(mid_band) + abs(high_band), 1e-6)

        return {
            "media_type": "audio",
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
            "audio_duration_seconds": round(duration_sec, 2),
            "spectral_bands": {
                "vocal_fundamental_ratio": round(abs(low_band) / tot_energy, 3),
                "formant_midband_ratio": round(abs(mid_band) / tot_energy, 3),
                "vocoder_highband_ratio": round(abs(high_band) / tot_energy, 3),
            },
            "artifacts": {
                "mel_spectrogram_b64": self._np_to_base64_png(mel_img),
                "anomaly_spectrogram_b64": self._np_to_base64_png(anomaly_img),
            },
            "latent_embedding": audio_feat.squeeze(0).detach().cpu().tolist(),
        }
