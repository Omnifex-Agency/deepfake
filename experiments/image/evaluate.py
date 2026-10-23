"""
DeepShield AI — Robustness Evaluation Battery & Latency Profiler
Tests trained checkpoints across JPEG compression, Gaussian blur,
spatial downsampling, and benchmarks millisecond inference latency.
"""

import os
import json
import argparse
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from experiments.image.dataset import (
    ForensicImageDataset,
    get_forensic_transforms,
    create_train_val_test_splits,
)
from experiments.image.models import build_model, TemperatureScaler
from experiments.image.metrics import evaluate_forensic_predictions, benchmark_inference_latency


def run_robustness_battery(
    model_name: str,
    checkpoint_path: str,
    data_dir: str,
    device: str = "cpu",
    batch_size: int = 16,
    output_dir: str = "experiments/image/reports",
) -> dict:
    os.makedirs(output_dir, exist_ok=True)

    # 1. Load checkpoint and model
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model = build_model(model_name, pretrained=False)
    model.load_state_dict(checkpoint["state_dict"], strict=False)
    model.to(device)
    model.eval()

    # Retrieve learned temperature if saved, else default to 1.0
    temperature = checkpoint.get("temperature", 1.0)
    print(f"[Evaluation] Loaded {model_name} from {checkpoint_path} (T = {temperature:.2f})")

    # 2. Get test samples
    real_dir = os.path.join(data_dir, "real")
    fake_dir = os.path.join(data_dir, "fake")
    _, _, test_samples = create_train_val_test_splits(
        real_dir, fake_dir, train_ratio=0.7, val_ratio=0.15, seed=42
    )
    print(f"[Evaluation] Evaluating on {len(test_samples)} untouched test samples...")

    # 3. Define perturbation test suite
    perturbations = {
        "Clean (Baseline)": get_forensic_transforms(is_train=False),
        "JPEG (Q=90)": get_forensic_transforms(is_train=False, jpeg_quality=90),
        "JPEG (Q=70)": get_forensic_transforms(is_train=False, jpeg_quality=70),
        "JPEG (Q=50)": get_forensic_transforms(is_train=False, jpeg_quality=50),
        "JPEG (Q=30)": get_forensic_transforms(is_train=False, jpeg_quality=30),
        "Blur (r=1.0)": get_forensic_transforms(is_train=False, blur_radius=1.0),
        "Blur (r=2.0)": get_forensic_transforms(is_train=False, blur_radius=2.0),
        "Downsample (112x112)": get_forensic_transforms(is_train=False, downsample_res=112),
        "Downsample (64x64)": get_forensic_transforms(is_train=False, downsample_res=64),
    }

    results = {}

    for pert_name, transform in perturbations.items():
        test_ds = ForensicImageDataset(test_samples, transform=transform)
        loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

        all_probs, all_labels = [], []
        with torch.no_grad():
            for images, labels, _ in loader:
                images = images.to(device)
                logits = model(images).squeeze(-1)
                scaled_logits = logits / temperature
                probs = torch.sigmoid(scaled_logits).cpu().numpy()
                all_probs.extend(probs)
                all_labels.extend(labels.numpy())

        metrics = evaluate_forensic_predictions(np.array(all_labels), np.array(all_probs))
        results[pert_name] = metrics
        print(f"  {pert_name:<24} | AUC: {metrics['roc_auc']:.4f} | Acc: {metrics['accuracy']:.4f} | F1: {metrics['f1_score']:.4f} | ECE: {metrics['expected_calibration_error']:.4f}")

    # 4. Latency Benchmark
    dummy_input = torch.randn(1, 3, 224, 224).to(device)
    latency_stats = benchmark_inference_latency(model, dummy_input, device=device, n_warmup=10, n_iterations=50)
    print(f"\n[Latency] Mean: {latency_stats['mean_latency_ms']:.2f} ms | P95: {latency_stats['p95_latency_ms']:.2f} ms | Throughput: {latency_stats['throughput_samples_per_sec']:.1f} FPS")

    # 5. Output Report
    full_report = {
        "model_name": model_name,
        "checkpoint": checkpoint_path,
        "temperature": temperature,
        "robustness_results": results,
        "latency_stats": latency_stats,
    }

    out_file = os.path.join(output_dir, f"{model_name}_robustness_report.json")
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

    run_robustness_battery(
        model_name=args.model,
        checkpoint_path=args.checkpoint,
        data_dir=args.data_dir,
        device=args.device,
    )
