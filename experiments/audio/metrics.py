"""
DeepShield AI — Audio Forensics & Anti-Spoofing Metrics Engine
Computes Equal Error Rate (EER), min t-DCF, ROC-AUC, PR-AUC,
Expected Calibration Error (ECE), and audio inference latency.
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


def compute_equal_error_rate(
    y_true: np.ndarray, y_score: np.ndarray
) -> Tuple[float, float]:
    """
    Computes Equal Error Rate (EER) and the optimal decision threshold.
    EER occurs where False Acceptance Rate (FAR) == False Rejection Rate (FRR).
    
    Parameters:
        y_true: Ground truth binary labels (0 = Bonafide/Real, 1 = Spoofed/Fake)
        y_score: Predicted risk scores or probabilities of being Spoofed/Fake
        
    Returns:
        eer: Equal Error Rate in [0.0, 1.0]
        threshold: The threshold tau* where FAR == FRR
    """
    y_true = np.asarray(y_true, dtype=int)
    y_score = np.asarray(y_score, dtype=float)

    # Sort scores in descending order
    sorted_indices = np.argsort(y_score)[::-1]
    sorted_scores = y_score[sorted_indices]
    sorted_labels = y_true[sorted_indices]

    n_fake = np.sum(sorted_labels == 1)
    n_real = np.sum(sorted_labels == 0)

    if n_fake == 0 or n_real == 0:
        return 0.5, 0.5

    # True positives (fake detected as fake) and False positives (real detected as fake)
    tp_cumsum = np.cumsum(sorted_labels == 1)
    fp_cumsum = np.cumsum(sorted_labels == 0)

    # FAR: real accepted as real? In anti-spoofing terminology:
    # False Alarm / False Acceptance Rate (real misclassified as fake)
    # False Rejection / Miss Rate (fake misclassified as real)
    # Let's align with ASVspoof standards:
    # FRR = false_negative_fakes / n_fake (fakes that bypassed the system)
    # FAR = false_positive_fakes / n_real (legitimate speakers falsely flagged as fake)
    far = fp_cumsum / n_real
    frr = (n_fake - tp_cumsum) / n_fake

    # Find point where far and frr intersect
    diff = np.abs(far - frr)
    best_idx = np.argmin(diff)

    eer = float((far[best_idx] + frr[best_idx]) / 2.0)
    opt_threshold = float(sorted_scores[best_idx])

    return eer, opt_threshold


def compute_audio_expected_calibration_error(
    y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 15
) -> float:
    """Computes Expected Calibration Error (ECE) for audio probabilities."""
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n_samples = len(y_true)

    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]

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


def evaluate_audio_predictions(
    y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5
) -> Dict[str, float]:
    """
    Evaluates audio predictions against full ASVspoof and forensic metrics.
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

    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        roc_auc = 0.5

    try:
        precisions, recalls, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(recalls, precisions)
    except ValueError:
        pr_auc = 0.0

    eer, opt_thresh = compute_equal_error_rate(y_true, y_prob)
    ece = compute_audio_expected_calibration_error(y_true, y_prob, n_bins=15)
    brier = brier_score_loss(y_true, y_prob)

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()

    return {
        "equal_error_rate": float(eer),
        "optimal_eer_threshold": float(opt_thresh),
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "macro_f1": float(macro_f1),
        "roc_auc": float(roc_auc),
        "pr_auc": float(pr_auc),
        "expected_calibration_error": float(ece),
        "brier_score": float(brier),
        "true_positives": int(tp),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
    }


def benchmark_audio_latency(
    model, sample_input, device: str = "cpu", n_warmup: int = 15, n_iterations: int = 60
) -> Dict[str, float]:
    """Measures audio inference latency in ms per 4-second audio clip."""
    import torch

    model.eval()
    model.to(device)
    sample_input = sample_input.to(device)

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
            latencies.append((t1 - t0) * 1000.0)

    latencies = np.array(latencies)
    batch_size = sample_input.shape[0] if len(sample_input.shape) > 1 else 1

    return {
        "mean_latency_ms": float(np.mean(latencies)),
        "std_latency_ms": float(np.std(latencies)),
        "p95_latency_ms": float(np.percentile(latencies, 95)),
        "throughput_clips_per_sec": float(batch_size / (np.mean(latencies) / 1000.0)),
    }
