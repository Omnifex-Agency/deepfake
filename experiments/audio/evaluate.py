"""
DeepShield AI — Audio Robustness Battery & Latency Profiler
Tests audio checkpoints under MP3 codecs (64k, 32k), additive acoustic noise,
reverberation, and benchmarks millisecond inference latency per audio clip.
"""

import os
import json
import argparse
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from experiments.audio.dataset import (
    ForensicAudioDataset,
    create_audio_train_val_test_splits,
)
from experiments.audio.models import build_audio_model
from experiments.audio.metrics import evaluate_audio_predictions, benchmark_audio_latency


def run_audio_robustness_battery(
    model_name: str,
    checkpoint_path: str,
    data_dir: str,
    device: str = "cpu",
    batch_size: int = 16,
    output_dir: str = "experiments/audio/reports",
) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    # 1. Load checkpoint and model
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model = build_audio_model(model_name)
    model.load_state_dict(checkpoint["state_dict"], strict=False)
    model.to(device)
    model.eval()

    temperature = checkpoint.get("temperature", 1.0)
    feat_type = checkpoint.get("feature_type", "mel")
    print(f"[Audio Evaluation] Loaded {model_name} from {checkpoint_path} (T = {temperature:.2f}, Features: {feat_type})")

    # 2. Get test samples
    real_dir = os.path.join(data_dir, "real")
    fake_dir = os.path.join(data_dir, "fake")
    _, _, test_samples = create_audio_train_val_test_splits(
        real_dir, fake_dir, train_ratio=0.7, val_ratio=0.15, seed=42
    )
    print(f"[Audio Evaluation] Evaluating on {len(test_samples)} untouched test audio clips...")

    # 3. Audio stress perturbation suite
    perturbations = [
        ("Clean (Baseline)", "clean"),
        ("Codec (MP3 64k / Opus)", "mp3_codec_64k"),
        ("Codec (Telephony 32k)", "mp3_codec_32k"),
        ("Noise (20 dB SNR)", "noise_snr20"),
        ("Noise (10 dB SNR - Severe)", "noise_snr10"),
        ("Room Reverberation", "reverberation"),
    ]

    results = {}

    for pert_name, pert_type in perturbations:
        test_ds = ForensicAudioDataset(test_samples, feature_type=feat_type, perturbation=pert_type)
        loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

        all_probs, all_labels = [], []
        with torch.no_grad():
            for inputs, labels, _ in loader:
                inputs = inputs.to(device)
                logits = model(inputs).squeeze(-1)
                scaled_logits = logits / temperature
                probs = torch.sigmoid(scaled_logits).cpu().numpy()
                all_probs.extend(probs)
                all_labels.extend(labels.numpy())

        metrics = evaluate_audio_predictions(np.array(all_labels), np.array(all_probs))
        results[pert_name] = metrics
        print(f"  {pert_name:<28} | EER: {metrics['equal_error_rate']:.4f} | AUC: {metrics['roc_auc']:.4f} | Acc: {metrics['accuracy']:.4f} | ECE: {metrics['expected_calibration_error']:.4f}")

    # 4. Latency Benchmark
    if feat_type == "raw":
        dummy_input = torch.randn(1, 64000).to(device)
    else:
        dummy_input = torch.randn(1, 80, 400).to(device)

    latency_stats = benchmark_audio_latency(model, dummy_input, device=device, n_warmup=10, n_iterations=40)
    print(f"\n[Audio Latency] Mean: {latency_stats['mean_latency_ms']:.2f} ms | P95: {latency_stats['p95_latency_ms']:.2f} ms | Throughput: {latency_stats['throughput_clips_per_sec']:.1f} clips/sec")

    # 5. Output Report
    full_report = {
        "model_name": model_name,
        "feature_type": feat_type,
        "checkpoint": checkpoint_path,
        "temperature": temperature,
        "robustness_results": results,
        "latency_stats": latency_stats,
    }

    out_file = os.path.join(output_dir, f"{model_name}_audio_robustness_report.json")
    with open(out_file, "w") as f:
        json.dump(full_report, f, indent=2)

    return full_report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--device", type=str, default="cpu")
    args = parser.parse_args()

    run_audio_robustness_battery(
        model_name=args.model,
        checkpoint_path=args.checkpoint,
        data_dir=args.data_dir,
        device=args.device,
    )
