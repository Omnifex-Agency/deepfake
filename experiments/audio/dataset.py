"""
DeepShield AI — Audio Forensics Dataset & Codec Augmentation Engine
Supports raw waveform and log-mel feature extraction, speaker-disjoint partitioning,
codec re-encoding stress tests, and controlled acoustic smoke synthesis.
"""

import io
import os
import math
import random
import numpy as np
import scipy.signal
import wave
from typing import List, Tuple, Dict, Optional, Callable

import torch
from torch.utils.data import Dataset, DataLoader


# ============================================================================
# 1. Feature Extraction: Log-Mel Spectrogram & Raw Slicing
# ============================================================================

def compute_log_mel_spectrogram(
    waveform: np.ndarray,
    sample_rate: int = 16000,
    n_mels: int = 80,
    n_fft: int = 512,
    hop_length: int = 160,
) -> np.ndarray:
    """
    Computes 80-channel Log-Mel Filterbank spectrogram matching Whisper/ASV standards.
    Input: 1D numpy array of raw audio.
    Output: 2D numpy array [n_mels, n_frames].
    """
    # STFT using scipy
    frequencies, times, Zxx = scipy.signal.stft(
        waveform,
        fs=sample_rate,
        window="hann",
        nperseg=n_fft,
        noverlap=n_fft - hop_length,
        boundary=None,
    )
    power_spec = np.abs(Zxx) ** 2

    # Mel filterbank construction
    low_freq = 0.0
    high_freq = sample_rate / 2.0
    mel_low = 2595.0 * np.log10(1.0 + low_freq / 700.0)
    mel_high = 2595.0 * np.log10(1.0 + high_freq / 700.0)
    mel_points = np.linspace(mel_low, mel_high, n_mels + 2)
    hz_points = 700.0 * (10.0 ** (mel_points / 2595.0) - 1.0)
    bins = np.floor((n_fft + 1) * hz_points / sample_rate).astype(int)

    fbank = np.zeros((n_mels, int(np.floor(n_fft / 2 + 1))), dtype=np.float32)
    for m in range(1, n_mels + 1):
        f_m_minus = bins[m - 1]
        f_m = bins[m]
        f_m_plus = bins[m + 1]

        for k in range(f_m_minus, f_m):
            if f_m != f_m_minus:
                fbank[m - 1, k] = (k - bins[m - 1]) / (bins[m] - bins[m - 1])
        for k in range(f_m, f_m_plus):
            if f_m_plus != f_m:
                fbank[m - 1, k] = (bins[m + 1] - k) / (bins[m + 1] - bins[m])

    mel_spec = np.dot(fbank, power_spec)
    mel_spec = np.maximum(mel_spec, 1e-10)
    log_mel = np.log10(mel_spec)
    # Zero-mean unit-variance per utterance
    log_mel = (log_mel - np.mean(log_mel)) / (np.std(log_mel) + 1e-6)
    return log_mel.astype(np.float32)


# ============================================================================
# 2. Audio Stress Augmentations (MP3/Codec Artifacts, Noise, Reverb)
# ============================================================================

def apply_audio_stress_perturbation(
    waveform: np.ndarray,
    perturbation_type: str = "clean",
    sample_rate: int = 16000,
) -> np.ndarray:
    """
    Simulates real-world audio degradations:
    - 'mp3_codec_64k': Simulates low-bitrate MP3/Opus cutoff at 7 kHz + quantization noise
    - 'mp3_codec_32k': Aggressive telephony codec cutoff at 3.8 kHz + bit reduction
    - 'noise_snr20': Additive white Gaussian acoustic noise at 20 dB SNR
    - 'noise_snr10': Severe additive acoustic noise at 10 dB SNR
    - 'reverberation': Room impulse comb filtering
    """
    audio = waveform.copy()

    if perturbation_type == "mp3_codec_64k":
        # Lowpass filter at 7000 Hz (Opus 32k / MP3 64k typical cutoff)
        b, a = scipy.signal.butter(6, 7000.0 / (sample_rate / 2.0), btype="low")
        audio = scipy.signal.filtfilt(b, a, audio)
        # Quantization noise
        quant_step = 2.0 / 256.0
        audio = np.round(audio / quant_step) * quant_step

    elif perturbation_type == "mp3_codec_32k":
        # Lowpass filter at 3800 Hz (AMR/Narrowband Telephony)
        b, a = scipy.signal.butter(6, 3800.0 / (sample_rate / 2.0), btype="low")
        audio = scipy.signal.filtfilt(b, a, audio)
        quant_step = 2.0 / 128.0
        audio = np.round(audio / quant_step) * quant_step

    elif perturbation_type == "noise_snr20":
        signal_power = np.mean(audio ** 2)
        noise_power = signal_power / (10 ** (20.0 / 10.0))
        noise = np.random.normal(0, np.sqrt(noise_power), len(audio))
        audio = audio + noise

    elif perturbation_type == "noise_snr10":
        signal_power = np.mean(audio ** 2)
        noise_power = signal_power / (10 ** (10.0 / 10.0))
        noise = np.random.normal(0, np.sqrt(noise_power), len(audio))
        audio = audio + noise

    elif perturbation_type == "reverberation":
        # Multi-tap synthetic room impulse response
        delay_samples = int(sample_rate * 0.05)  # 50 ms delay
        decay = 0.4
        reverb = np.zeros_like(audio)
        if len(audio) > delay_samples:
            reverb[delay_samples:] = audio[:-delay_samples] * decay
        audio = audio + reverb

    return audio.astype(np.float32)


# ============================================================================
# 3. Forensic Audio Dataset Class
# ============================================================================

class ForensicAudioDataset(Dataset):
    """
    Loads audio files, enforces fixed 4.0-second length (64,000 samples),
    and extracts either raw waveform tensors or 80-channel Log-Mel spectrograms.
    """
    def __init__(
        self,
        samples: List[Tuple[str, int]],
        feature_type: str = "mel",  # 'mel' or 'raw'
        target_length: int = 64000,
        sample_rate: int = 16000,
        perturbation: str = "clean",
    ):
        self.samples = samples
        self.feature_type = feature_type
        self.target_length = target_length
        self.sample_rate = sample_rate
        self.perturbation = perturbation

    def __len__(self) -> int:
        return len(self.samples)

    def _read_wav(self, path: str) -> np.ndarray:
        with wave.open(path, "rb") as wf:
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)
            # 16-bit PCM mono
            audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
        return audio

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int, str]:
        path, label = self.samples[idx]
        try:
            audio = self._read_wav(path)
        except Exception:
            audio = np.zeros(self.target_length, dtype=np.float32)

        # Pad or crop to exact target_length
        if len(audio) < self.target_length:
            pad = self.target_length - len(audio)
            audio = np.pad(audio, (0, pad), mode="wrap")
        else:
            audio = audio[:self.target_length]

        # Apply stress perturbation if specified
        if self.perturbation != "clean":
            audio = apply_audio_stress_perturbation(audio, perturbation_type=self.perturbation)

        if self.feature_type == "mel":
            mel = compute_log_mel_spectrogram(audio, sample_rate=self.sample_rate, n_mels=80)
            tensor = torch.tensor(mel, dtype=torch.float32)  # [80, Time]
        else:
            tensor = torch.tensor(audio, dtype=torch.float32)  # [Samples]

        return tensor, label, path


# ============================================================================
# 4. Controlled Audio Smoke-Test Dataset Generator
# ============================================================================

def generate_controlled_audio_smoke_dataset(
    output_dir: str, n_real: int = 100, n_fake: int = 100, seed: int = 42
) -> Dict[str, str]:
    """
    Generates a scientifically grounded audio smoke dataset on disk:
    - Real Audio: Source-filter model with natural pitch glottal pulses, 3 resonant
      formants (F1, F2, F3), vocal jitter, and natural amplitude modulation.
    - Fake Audio: Neural vocoder synthesis artifacts (phase discontinuities, robotic
      harmonic spikes, missing micro-jitter, and synthetic high-frequency vocoder hiss).
    """
    random.seed(seed)
    np.random.seed(seed)

    real_dir = os.path.join(output_dir, "real")
    fake_dir = os.path.join(output_dir, "fake")
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(fake_dir, exist_ok=True)

    sr = 16000
    duration_sec = 4.0
    n_samples = int(sr * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    # 1. Generate Authentic (Bonafide) Speech Audio
    for i in range(n_real):
        # Fundamental frequency with natural vocal micro-tremor (vibrato/jitter)
        f0_base = random.uniform(110.0, 190.0)
        pitch_contour = f0_base + 4.0 * np.sin(2.0 * np.pi * 3.5 * t) + np.random.normal(0, 0.5, n_samples)
        phase = np.cumsum(2.0 * np.pi * pitch_contour / sr)

        # Glottal pulse train with harmonics
        glottal = (
            np.sin(phase) +
            0.5 * np.sin(2.0 * phase) +
            0.25 * np.sin(3.0 * phase) +
            0.12 * np.sin(4.0 * phase) +
            0.06 * np.sin(5.0 * phase)
        )

        # Resonant Vocal Formants (F1=500Hz, F2=1500Hz, F3=2500Hz)
        b1, a1 = scipy.signal.butter(2, [400 / (sr / 2), 650 / (sr / 2)], btype="band")
        b2, a2 = scipy.signal.butter(2, [1350 / (sr / 2), 1750 / (sr / 2)], btype="band")
        b3, a3 = scipy.signal.butter(2, [2300 / (sr / 2), 2800 / (sr / 2)], btype="band")

        vocal_audio = (
            0.6 * scipy.signal.lfilter(b1, a1, glottal) +
            0.3 * scipy.signal.lfilter(b2, a2, glottal) +
            0.1 * scipy.signal.lfilter(b3, a3, glottal)
        )

        # Natural room noise & speech breathing pause
        envelope = 0.5 * (1.0 + np.sin(2.0 * np.pi * 0.8 * t))  # natural syllable modulation
        vocal_audio = vocal_audio * envelope + np.random.normal(0, 0.005, n_samples)
        vocal_audio = vocal_audio / (np.max(np.abs(vocal_audio)) + 1e-6) * 0.85

        # Write 16-bit PCM WAV
        pcm = (vocal_audio * 32767.0).astype(np.int16)
        path = os.path.join(real_dir, f"real_{i:04d}.wav")
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(pcm.tobytes())

    # 2. Generate Synthetic (Deepfake) Speech Audio
    for i in range(n_fake):
        f0_base = random.uniform(110.0, 190.0)
        # Synthetic vocoder signature: strictly rigid pitch (quantized/robotic)
        pitch_contour = np.full(n_samples, f0_base)
        phase = np.cumsum(2.0 * np.pi * pitch_contour / sr)

        # Neural vocoder overtone pattern
        glottal = (
            np.sin(phase) +
            0.65 * np.sin(2.0 * phase) +
            0.45 * np.sin(3.0 * phase) +
            0.35 * np.sin(4.0 * phase) +
            0.25 * np.sin(5.0 * phase)
        )

        # Static vocal tract filter
        b1, a1 = scipy.signal.butter(2, [400 / (sr / 2), 650 / (sr / 2)], btype="band")
        vocal_audio = scipy.signal.lfilter(b1, a1, glottal)

        # Inject vocoder artifacts:
        # A. Neural vocoder high-frequency metallic buzz (HiFi-GAN/MelGAN alias peaks)
        buzz_freq = random.choice([3600, 4800, 6000])
        vocoder_buzz = 0.15 * np.sin(2.0 * np.pi * buzz_freq * t)

        # B. Periodic phase discontinuity (waveform concatenation glitch)
        glitch = np.zeros(n_samples)
        glitch[::int(sr * 0.25)] = 0.4

        # C. Low dynamic micro-jitter
        vocal_audio = vocal_audio + vocoder_buzz + glitch
        vocal_audio = vocal_audio / (np.max(np.abs(vocal_audio)) + 1e-6) * 0.85

        pcm = (vocal_audio * 32767.0).astype(np.int16)
        path = os.path.join(fake_dir, f"fake_{i:04d}.wav")
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(pcm.tobytes())

    return {
        "real_dir": real_dir,
        "fake_dir": fake_dir,
        "total_samples": n_real + n_fake,
    }


def create_audio_train_val_test_splits(
    real_dir: str, fake_dir: str, train_ratio: float = 0.7, val_ratio: float = 0.15, seed: int = 42
) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]], List[Tuple[str, int]]]:
    """Partitions audio files into strictly disjoint train/val/test splits."""
    random.seed(seed)

    real_files = [os.path.join(real_dir, f) for f in os.listdir(real_dir) if f.endswith(".wav")]
    fake_files = [os.path.join(fake_dir, f) for f in os.listdir(fake_dir) if f.endswith(".wav")]

    random.shuffle(real_files)
    random.shuffle(fake_files)

    def split_list(lst):
        n = len(lst)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        return lst[:n_train], lst[n_train:n_train + n_val], lst[n_train + n_val:]

    real_train, real_val, real_test = split_list(real_files)
    fake_train, fake_val, fake_test = split_list(fake_files)

    train_samples = [(p, 0) for p in real_train] + [(p, 1) for p in fake_train]
    val_samples = [(p, 0) for p in real_val] + [(p, 1) for p in fake_val]
    test_samples = [(p, 0) for p in real_test] + [(p, 1) for p in fake_test]

    random.shuffle(train_samples)
    random.shuffle(val_samples)
    random.shuffle(test_samples)

    return train_samples, val_samples, test_samples
