"""
DeepShield AI — Model Training & Calibration Engine
Trains candidate architectures, performs validation monitoring,
and calibrates output probabilities using Temperature Scaling.
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

from experiments.image.dataset import (
    ForensicImageDataset,
    get_forensic_transforms,
    create_train_val_test_splits,
    generate_controlled_smoke_dataset,
)
from experiments.image.models import (
    EfficientNetB0Detector,
    MesoInception4Detector,
    ResNet50Detector,
    AdaptiveSpatialFrequencyDetector,
    TemperatureScaler,
)
from experiments.image.metrics import evaluate_forensic_predictions


def build_model(model_name: str, pretrained: bool = True):
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


def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []

    for images, labels, _ in loader:
        images = images.to(device)
        labels = labels.to(device).float()

        optimizer.zero_grad()
        logits = model(images).squeeze(-1)
        loss = criterion(logits, labels)
        loss.backward()

        # Gradient clipping for numerical stability
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss += loss.item() * len(labels)
        probs = torch.sigmoid(logits).detach().cpu().numpy()
        all_preds.extend(probs)
        all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(loader.dataset)
    metrics = evaluate_forensic_predictions(np.array(all_labels), np.array(all_preds))
    metrics["loss"] = avg_loss
    return metrics


def validate_epoch(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    all_preds, all_labels, all_logits = [], [], []

    with torch.no_grad():
        for images, labels, _ in loader:
            images = images.to(device)
            labels = labels.to(device).float()

            logits = model(images).squeeze(-1)
            loss = criterion(logits, labels)

            total_loss += loss.item() * len(labels)
            probs = torch.sigmoid(logits).cpu().numpy()
            all_logits.extend(logits.cpu().numpy())
            all_preds.extend(probs)
            all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / len(loader.dataset)
    metrics = evaluate_forensic_predictions(np.array(all_labels), np.array(all_preds))
    metrics["loss"] = avg_loss
    return metrics, np.array(all_logits), np.array(all_labels)


def train_model(
    model_name: str = "efficientnet_b0",
    data_dir: Optional[str] = None,
    epochs: int = 5,
    batch_size: int = 16,
    lr: float = 1e-4,
    device: str = "cpu",
    output_dir: str = "experiments/image/checkpoints",
):
    os.makedirs(output_dir, exist_ok=True)

    # 1. Prepare data (use smoke dataset if data_dir not provided)
    if data_dir is None or not os.path.exists(data_dir):
        smoke_dir = os.path.join(output_dir, "smoke_data")
        print(f"[Data] Generating controlled smoke-test dataset at {smoke_dir}...")
        meta = generate_controlled_smoke_dataset(smoke_dir, n_real=150, n_fake=150, seed=42)
        real_dir = meta["real_dir"]
        fake_dir = meta["fake_dir"]
    else:
        real_dir = os.path.join(data_dir, "real")
        fake_dir = os.path.join(data_dir, "fake")

    train_samples, val_samples, test_samples = create_train_val_test_splits(
        real_dir, fake_dir, train_ratio=0.7, val_ratio=0.15, seed=42
    )
    print(f"[Data] Partitioned: {len(train_samples)} Train, {len(val_samples)} Val, {len(test_samples)} Test samples.")

    train_ds = ForensicImageDataset(train_samples, transform=get_forensic_transforms(is_train=True))
    val_ds = ForensicImageDataset(val_samples, transform=get_forensic_transforms(is_train=False))
    test_ds = ForensicImageDataset(test_samples, transform=get_forensic_transforms(is_train=False))

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    # 2. Build model & optimizer
    model = build_model(model_name, pretrained=True)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    criterion = nn.BCEWithLogitsLoss()
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    best_val_auc = 0.0
    best_checkpoint_path = os.path.join(output_dir, f"{model_name}_best.pt")

    history = {"train_loss": [], "val_loss": [], "val_auc": [], "val_f1": []}

    print(f"\n[Training] Starting {epochs} epochs for {model_name} on {device}...")
    t_start = time.time()

    for epoch in range(1, epochs + 1):
        t0 = time.time()
        train_metrics = train_epoch(model, train_loader, optimizer, criterion, device)
        val_metrics, val_logits, val_labels = validate_epoch(model, val_loader, criterion, device)
        scheduler.step()
        elapsed = time.time() - t0

        history["train_loss"].append(train_metrics["loss"])
        history["val_loss"].append(val_metrics["loss"])
        history["val_auc"].append(val_metrics["roc_auc"])
        history["val_f1"].append(val_metrics["f1_score"])

        print(
            f"Epoch {epoch:02d}/{epochs:02d} [{elapsed:.1f}s] | "
            f"Train Loss: {train_metrics['loss']:.4f} | "
            f"Val Loss: {val_metrics['loss']:.4f} | "
            f"Val AUC: {val_metrics['roc_auc']:.4f} | "
            f"Val F1: {val_metrics['f1_score']:.4f} | "
            f"Val ECE: {val_metrics['expected_calibration_error']:.4f}"
        )

        if val_metrics["roc_auc"] > best_val_auc:
            best_val_auc = val_metrics["roc_auc"]
            torch.save(
                {
                    "model_name": model_name,
                    "state_dict": model.state_dict(),
                    "epoch": epoch,
                    "val_auc": best_val_auc,
                },
                best_checkpoint_path,
            )

    print(f"[Training] Completed in {time.time() - t_start:.1f}s. Best Val AUC: {best_val_auc:.4f}")

    # 3. Fit Temperature Scaling on validation logits
    checkpoint = torch.load(best_checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint["state_dict"], strict=False)
    val_metrics, val_logits, val_labels = validate_epoch(model, val_loader, criterion, device)

    scaler = TemperatureScaler()
    opt_temp = scaler.fit(torch.tensor(val_logits), torch.tensor(val_labels))
    print(f"[Calibration] Optimal learned Temperature T = {opt_temp:.3f}")

    # Update checkpoint with optimal temperature
    checkpoint["temperature"] = float(opt_temp)
    torch.save(checkpoint, best_checkpoint_path)

    # 4. Final Evaluation on Untouched Test Set
    test_metrics_raw, test_logits, test_labels = validate_epoch(model, test_loader, criterion, device)
    calibrated_test_probs = torch.sigmoid(torch.tensor(test_logits) / opt_temp).numpy()
    test_metrics_calibrated = evaluate_forensic_predictions(test_labels, calibrated_test_probs)

    print("\n" + "="*60)
    print(f"FINAL UNTOUCHED TEST SET RESULTS: {model_name}")
    print("="*60)
    print(f"  Accuracy:                   {test_metrics_calibrated['accuracy']:.4f}")
    print(f"  ROC-AUC:                    {test_metrics_calibrated['roc_auc']:.4f}")
    print(f"  PR-AUC:                     {test_metrics_calibrated['pr_auc']:.4f}")
    print(f"  Macro-F1:                   {test_metrics_calibrated['macro_f1']:.4f}")
    print(f"  FPR at 95% Recall:          {test_metrics_calibrated['fpr_at_95_recall']:.4f}")
    print(f"  ECE (Before Calibration):   {test_metrics_raw['expected_calibration_error']:.4f}")
    print(f"  ECE (After Temperature T):  {test_metrics_calibrated['expected_calibration_error']:.4f}")
    print(f"  Brier Score:                {test_metrics_calibrated['brier_score']:.4f}")
    print(f"  Confusion Matrix:           TP={test_metrics_calibrated['true_positives']}, FP={test_metrics_calibrated['false_positives']}, TN={test_metrics_calibrated['true_negatives']}, FN={test_metrics_calibrated['false_negatives']}")
    print("="*60)

    # Save summary report
    report = {
        "model_name": model_name,
        "best_val_auc": float(best_val_auc),
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
    parser.add_argument("--model", type=str, default="efficientnet_b0", choices=["efficientnet_b0", "mesoinception4", "resnet50", "deepshield"])
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--data_dir", type=str, default=None)
    args = parser.parse_args()

    train_model(
        model_name=args.model,
        data_dir=args.data_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        device=args.device,
    )
