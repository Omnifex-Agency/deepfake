"""
DeepShield AI — Forensic Evaluation & Metrics Engine
Computes comprehensive classification metrics, calibration quality (ECE, Brier),
and inference benchmarks for deepfake detection.
"""

import time
import numpy as np
from typing import Dict, Tuple, Optional
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    precision_recall_curve,
    auc,
    confusion_matrix,
    brier_score_loss,
)


def compute_expected_calibration_error(
    y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 15
) -> float:
    """
    Computes Expected Calibration Error (ECE) across M equally spaced bins.
    ECE = sum_m (|B_m| / N) * |acc(B_m) - conf(B_m)|
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n_samples = len(y_true)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]

        # Samples within the bin (inclusive of lower, exclusive of upper unless last bin)
        if i == n_bins - 1:
            in_bin = (y_prob >= bin_lower) & (y_prob <= bin_upper)
        else:
            in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)

        bin_size = np.sum(in_bin)
        if bin_size > 0:
            bin_acc = np.mean(y_true[in_bin])
            bin_conf = np.mean(y_prob[in_bin])
            ece += (bin_size / n_samples) * np.abs(bin_acc - bin_conf)

    return float(ece)


def compute_fpr_at_recall(
    y_true: np.ndarray, y_prob: np.ndarray, target_recall: float = 0.95
) -> float:
    """
    Computes False Positive Rate (FPR) when the decision threshold achieves >= target_recall.
    """
    thresholds = np.sort(np.unique(y_prob))[::-1]
    best_fpr = 1.0

    for tau in thresholds:
        y_pred = (y_prob >= tau).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fn = np.sum((y_pred == 0) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        tn = np.sum((y_pred == 0) & (y_true == 0))

        actual_positives = tp + fn
        actual_negatives = fp + tn

        if actual_positives == 0 or actual_negatives == 0:
            continue

        rec = tp / actual_positives
        fpr = fp / actual_negatives

        if rec >= target_recall:
            best_fpr = min(best_fpr, fpr)

    return float(best_fpr)


def evaluate_forensic_predictions(
    y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5
) -> Dict[str, float]:
    """
    Comprehensive forensic evaluation returning all required metrics.
    
    Parameters:
        y_true: Ground truth binary labels (0 = Bonafide/Real, 1 = Fake/Synthetic)
        y_prob: Predicted probability of being Fake (values in [0.0, 1.0])
        threshold: Decision threshold (default 0.5)
        
    Returns:
        Dict containing accuracy, precision, recall, f1, macro_f1, roc_auc, pr_auc,
        fpr95, ece, brier_score, and confusion matrix counts.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_prob = np.asarray(y_prob, dtype=float)
    y_prob = np.clip(y_prob, 1e-7, 1.0 - 1e-7)
    y_pred = (y_prob >= threshold).astype(int)

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

    # ROC-AUC
    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        roc_auc = 0.5

    # PR-AUC
    try:
        precisions, recalls, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(recalls, precisions)
    except ValueError:
        pr_auc = 0.0

    # Calibration & Error metrics
    ece = compute_expected_calibration_error(y_true, y_prob, n_bins=15)
    brier = brier_score_loss(y_true, y_prob)
    fpr95 = compute_fpr_at_recall(y_true, y_prob, target_recall=0.95)

    # Confusion matrix breakdown
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    return {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "macro_f1": float(macro_f1),
        "roc_auc": float(roc_auc),
        "pr_auc": float(pr_auc),
        "fpr_at_95_recall": float(fpr95),
        "expected_calibration_error": float(ece),
        "brier_score": float(brier),
        "true_positives": int(tp),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
    }


def benchmark_inference_latency(
    model, sample_input, device: str = "cpu", n_warmup: int = 20, n_iterations: int = 100
) -> Dict[str, float]:
    """
    Accurately benchmarks inference latency (mean ms, p95 ms, throughput samples/sec).
    """
    import torch

    model.eval()
    model.to(device)
    sample_input = sample_input.to(device)

    # Warmup
    with torch.no_grad():
        for _ in range(n_warmup):
            _ = model(sample_input)

    latencies = []
    with torch.no_grad():
        for _ in range(n_iterations):
            t0 = time.perf_counter()
            _ = model(sample_input)
            if device.startswith("cuda") and torch.cuda.is_available():
                torch.cuda.synchronize()
            t1 = time.perf_counter()
            latencies.append((t1 - t0) * 1000.0)  # ms

    latencies = np.array(latencies)
    batch_size = sample_input.shape[0] if len(sample_input.shape) > 3 else 1

    return {
        "mean_latency_ms": float(np.mean(latencies)),
        "std_latency_ms": float(np.std(latencies)),
        "p95_latency_ms": float(np.percentile(latencies, 95)),
        "p99_latency_ms": float(np.percentile(latencies, 99)),
        "throughput_samples_per_sec": float(batch_size / (np.mean(latencies) / 1000.0)),
    }
