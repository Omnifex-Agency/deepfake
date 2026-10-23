"""
DeepShield AI — Audio Model Training & Calibration Engine
Trains candidate audio forensic architectures (LFCC-LCNN, SincAASIST, WhisperSpecRNet),
monitors validation Equal Error Rate (EER), and calibrates predictions.
"""

import os
import sys
import json
import time
import argparse
from typing import Optional, Dict, Tuple
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from experiments.audio.dataset import (
    ForensicAudioDataset,
    create_audio_train_val_test_splits,
    generate_controlled_audio_smoke_dataset,
)
from experiments.audio.models import build_audio_model
from experiments.audio.metrics import evaluate_audio_predictions
from experiments.image.models import TemperatureScaler


def train_audio_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []

    for inputs, labels, _ in loader:
        inputs = inputs.to(device)
        labels = labels.to(device).float()

        optimizer.zero_grad()
        logits = model(inputs).squeeze(-1)
        loss = criterion(logits, labels)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss += loss.item() * len(labels)
        probs = torch.sigmoid(logits).detach().cpu().numpy()
        all_preds.extend(probs)
        all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(loader.dataset)
    metrics = evaluate_audio_predictions(np.array(all_labels), np.array(all_preds))
    metrics["loss"] = avg_loss
    return metrics


def validate_audio_epoch(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_preds, all_labels, all_logits = [], [], []

    with torch.no_grad():
        for inputs, labels, _ in loader:
            inputs = inputs.to(device)
            labels = labels.to(device).float()

            logits = model(inputs).squeeze(-1)
            loss = criterion(logits, labels)

            total_loss += loss.item() * len(labels)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_logits.extend(logits.cpu().numpy())
            all_preds.extend(probs)
            all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(loader.dataset)
    metrics = evaluate_audio_predictions(np.array(all_labels), np.array(all_preds))
    metrics["loss"] = avg_loss
    return metrics, np.array(all_logits), np.array(all_labels)


def train_audio_model(
    model_name: str = "lcnn",
    data_dir: Optional[str] = None,
    epochs: int = 4,
    batch_size: int = 16,
    lr: float = 2e-4,
    device: str = "cpu",
    output_dir: str = "experiments/audio/checkpoints",
):
    os.makedirs(output_dir, exist_ok=True)

    # 1. Prepare data
    if data_dir is None or not os.path.exists(data_dir):
        smoke_dir = os.path.join(output_dir, "smoke_audio")
        print(f"[Audio Data] Generating controlled audio smoke dataset at {smoke_dir}...")
        meta = generate_controlled_audio_smoke_dataset(smoke_dir, n_real=100, n_fake=100, seed=42)
        real_dir = meta["real_dir"]
        fake_dir = meta["fake_dir"]
    else:
        real_dir = os.path.join(data_dir, "real")
        fake_dir = os.path.join(data_dir, "fake")

    train_samples, val_samples, test_samples = create_audio_train_val_test_splits(
        real_dir, fake_dir, train_ratio=0.7, val_ratio=0.15, seed=42
    )
    print(f"[Audio Data] Partitioned: {len(train_samples)} Train, {len(val_samples)} Val, {len(test_samples)} Test samples.")

    # Determine input feature type: SincAASIST uses raw waveform; LCNN/WhisperSpecRNet use Log-Mel
    feat_type = "raw" if model_name.lower() in ["sinc_aasist", "aasist", "rawnet"] else "mel"

    train_ds = ForensicAudioDataset(train_samples, feature_type=feat_type)
    val_ds = ForensicAudioDataset(val_samples, feature_type=feat_type)
    test_ds = ForensicAudioDataset(test_samples, feature_type=feat_type)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    # 2. Build model & optimizer
    model = build_audio_model(model_name)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.BCEWithLogitsLoss()
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_val_eer = 1.0
    best_checkpoint_path = os.path.join(output_dir, f"{model_name}_best.pt")
    history = {"train_loss": [], "val_loss": [], "val_eer": [], "val_auc": []}

    print(f"\n[Training] Starting {epochs} epochs for {model_name} ({feat_type} features) on {device}...")
    t_start = time.time()

    for epoch in range(1, epochs + 1):
        t0 = time.time()
        train_metrics = train_audio_epoch(model, train_loader, optimizer, criterion, device)
        val_metrics, val_logits, val_labels = validate_audio_epoch(model, val_loader, criterion, device)
        scheduler.step()
        elapsed = time.time() - t0

        history["train_loss"].append(train_metrics["loss"])
        history["val_loss"].append(val_metrics["loss"])
        history["val_eer"].append(val_metrics["equal_error_rate"])
        history["val_auc"].append(val_metrics["roc_auc"])

        print(
            f"Epoch {epoch:02d}/{epochs:02d} [{elapsed:.1f}s] | "
            f"Train Loss: {train_metrics['loss']:.4f} | "
            f"Val Loss: {val_metrics['loss']:.4f} | "
            f"Val EER: {val_metrics['equal_error_rate']:.4f} | "
            f"Val AUC: {val_metrics['roc_auc']:.4f} | "
            f"Val ECE: {val_metrics['expected_calibration_error']:.4f}"
        )

        if val_metrics["equal_error_rate"] <= best_val_eer:
            best_val_eer = val_metrics["equal_error_rate"]
            torch.save(
                {
                    "model_name": model_name,
                    "state_dict": model.state_dict(),
                    "epoch": epoch,
                    "val_eer": best_val_eer,
                    "feature_type": feat_type,
                },
                best_checkpoint_path,
            )

    print(f"[Training] Completed in {time.time() - t_start:.1f}s. Best Val EER: {best_val_eer:.4f}")

    # 3. Fit Temperature Scaling on validation logits
    checkpoint = torch.load(best_checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["state_dict"], strict=False)
    val_metrics, val_logits, val_labels = validate_audio_epoch(model, val_loader, criterion, device)

    scaler = TemperatureScaler()
    opt_temp = scaler.fit(torch.tensor(val_logits), torch.tensor(val_labels))
    print(f"[Calibration] Optimal learned Temperature T = {opt_temp:.3f}")

    checkpoint["temperature"] = float(opt_temp)
    torch.save(checkpoint, best_checkpoint_path)

    # 4. Final Evaluation on Untouched Test Set
    test_metrics_raw, test_logits, test_labels = validate_audio_epoch(model, test_loader, criterion, device)
    calibrated_test_probs = torch.sigmoid(torch.tensor(test_logits) / opt_temp).numpy()
    test_metrics_calibrated = evaluate_audio_predictions(test_labels, calibrated_test_probs)

    print("\n" + "="*60)
    print(f"FINAL UNTOUCHED TEST SET RESULTS: {model_name}")
    print("="*60)
    print(f"  Equal Error Rate (EER):     {test_metrics_calibrated['equal_error_rate']:.4f}")
    print(f"  Optimal EER Threshold:      {test_metrics_calibrated['optimal_eer_threshold']:.4f}")
    print(f"  Accuracy:                   {test_metrics_calibrated['accuracy']:.4f}")
    print(f"  ROC-AUC:                    {test_metrics_calibrated['roc_auc']:.4f}")
    print(f"  PR-AUC:                     {test_metrics_calibrated['pr_auc']:.4f}")
    print(f"  Macro-F1:                   {test_metrics_calibrated['macro_f1']:.4f}")
    print(f"  ECE (Before Calibration):   {test_metrics_raw['expected_calibration_error']:.4f}")
    print(f"  ECE (After Temperature T):  {test_metrics_calibrated['expected_calibration_error']:.4f}")
    print(f"  Brier Score:                {test_metrics_calibrated['brier_score']:.4f}")
    print(f"  Confusion Matrix:           TP={test_metrics_calibrated['true_positives']}, FP={test_metrics_calibrated['false_positives']}, TN={test_metrics_calibrated['true_negatives']}, FN={test_metrics_calibrated['false_negatives']}")
    print("="*60)

    report = {
        "model_name": model_name,
        "feature_type": feat_type,
        "best_val_eer": float(best_val_eer),
        "temperature": float(opt_temp),
        "test_metrics_raw": test_metrics_raw,
        "test_metrics_calibrated": test_metrics_calibrated,
        "history": history,
    }
    with open(os.path.join(output_dir, f"{model_name}_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="lcnn", choices=["lcnn", "sinc_aasist", "whisper_specrnet"])
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--data_dir", type=str, default=None)
    args = parser.parse_args()

    train_audio_model(
        model_name=args.model,
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
    )
