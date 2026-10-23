"""
DeepShield AI — Multimodal Audio-Visual Training & Quadrant Benchmark
Compares DecoupledAsymmetricFusion against NaiveJointConcatenation across
all 4 FakeAVCeleb quadrants (RR, FR, RF, FF) and tests single-modality fallbacks.
"""

import os
import json
import time
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from experiments.multimodal.dataset import (
    MultimodalQuadrantDataset,
    generate_multimodal_quadrant_embeddings,
)
from experiments.multimodal.models import (
    NaiveJointConcatenation,
    DecoupledAsymmetricFusion,
)
from experiments.image.metrics import evaluate_forensic_predictions


def evaluate_multimodal_model(model, samples, device="cpu"):
    """
    Evaluates multimodal model overall and broken down across all 4 quadrants (RR, FR, RF, FF),
    plus missing-modality fallback resilience.
    """
    model.eval()
    all_preds, all_labels = [], []
    quadrant_preds = {"RR": [], "FR": [], "RF": [], "FF": []}
    quadrant_labels = {"RR": [], "FR": [], "RF": [], "FF": []}

    # Missing modality test stores
    video_only_preds = []
    audio_only_preds = []

    with torch.no_grad():
        for item in samples:
            f_v = item["f_v"].unsqueeze(0).to(device)
            f_a = item["f_a"].unsqueeze(0).to(device)
            label = item["label"]
            quad = item["quadrant"]

            # 1. Full multimodal prediction
            if isinstance(model, DecoupledAsymmetricFusion):
                prob = model.predict_proba(f_v=f_v, f_a=f_a).item()
                # 2. Missing modality tests
                p_v_only = model.predict_proba(f_v=f_v, f_a=None).item()
                p_a_only = model.predict_proba(f_v=None, f_a=f_a).item()
            else:
                prob = model.predict_proba(f_v, f_a).item()
                p_v_only = model.predict_proba(f_v, torch.zeros_like(f_a)).item()
                p_a_only = model.predict_proba(torch.zeros_like(f_v), f_a).item()

            all_preds.append(prob)
            all_labels.append(label)
            quadrant_preds[quad].append(prob)
            quadrant_labels[quad].append(label)
            video_only_preds.append(p_v_only)
            audio_only_preds.append(p_a_only)

    overall_metrics = evaluate_forensic_predictions(np.array(all_labels), np.array(all_preds))

    # Quadrant breakdown
    quad_results = {}
    for q in ["RR", "FR", "RF", "FF"]:
        q_p = np.array(quadrant_preds[q])
        q_l = np.array(quadrant_labels[q])
        q_pred = (q_p >= 0.5).astype(int)
        acc = float(np.mean(q_pred == q_l))
        quad_results[q] = {
            "accuracy": acc,
            "mean_confidence": float(np.mean(q_p)),
            "sample_count": len(q_l),
        }

    # Fallback accuracy
    v_only_metrics = evaluate_forensic_predictions(np.array(all_labels), np.array(video_only_preds))
    a_only_metrics = evaluate_forensic_predictions(np.array(all_labels), np.array(audio_only_preds))

    return {
        "overall": overall_metrics,
        "quadrants": quad_results,
        "fallback_video_only": v_only_metrics,
        "fallback_audio_only": a_only_metrics,
    }


def run_multimodal_experiment(output_dir="experiments/multimodal/reports", n_per_quadrant=60, epochs=15):
    os.makedirs(output_dir, exist_ok=True)
    device = "cpu"

    print("="*70)
    print("DEEPSHIELD AI — STAGE 5 MULTIMODAL AUDIO-VISUAL POC BENCHMARK")
    print("="*70)

    train_samples, val_samples, test_samples = generate_multimodal_quadrant_embeddings(
        n_per_quadrant=n_per_quadrant, seed=42
    )
    print(f"[Data] Created 4-Quadrant partitions: {len(train_samples)} Train, {len(val_samples)} Val, {len(test_samples)} Test samples.")

    # 1. Train Baseline: NaiveJointConcatenation
    print("\n[1/2] Training Baseline: NaiveJointConcatenation...")
    model_baseline = NaiveJointConcatenation(visual_dim=128, audio_dim=128)
    opt_base = torch.optim.AdamW(model_baseline.parameters(), lr=1e-3, weight_decay=1e-4)
    crit_base = nn.BCEWithLogitsLoss()

    for epoch in range(1, epochs + 1):
        model_baseline.train()
        for item in train_samples:
            f_v = item["f_v"].unsqueeze(0)
            f_a = item["f_a"].unsqueeze(0)
            target = torch.tensor([item["label"]], dtype=torch.float32)

            opt_base.zero_grad()
            out = model_baseline(f_v, f_a).squeeze(-1)
            loss = crit_base(out, target)
            loss.backward()
            opt_base.step()

    # 2. Train Proposed: DecoupledAsymmetricFusion (DeepShield Contribution 3)
    print("[2/2] Training Proposed: DecoupledAsymmetricFusion...")
    model_proposed = DecoupledAsymmetricFusion(visual_dim=128, audio_dim=128)
    opt_prop = torch.optim.AdamW(model_proposed.parameters(), lr=1e-3, weight_decay=1e-4)
    crit_prop = nn.BCEWithLogitsLoss()

    for epoch in range(1, epochs + 1):
        model_proposed.train()
        for item in train_samples:
            f_v = item["f_v"].unsqueeze(0)
            f_a = item["f_a"].unsqueeze(0)
            target = torch.tensor([item["label"]], dtype=torch.float32)

            opt_prop.zero_grad()
            fused_logit, _, _ = model_proposed(f_v=f_v, f_a=f_a)
            loss = crit_prop(fused_logit.squeeze(-1), target)
            loss.backward()
            opt_prop.step()

    # 3. Evaluate Both on Untouched Test Samples
    print("\n[Evaluation] Evaluating models on untouched 4-quadrant test partition...")
    res_baseline = evaluate_multimodal_model(model_baseline, test_samples, device=device)
    res_proposed = evaluate_multimodal_model(model_proposed, test_samples, device=device)

    # 4. Formatted Comparative Report
    print("\n" + "="*70)
    print(f"{'EVALUATION METRIC':<32} | {'BASELINE (NAIVE CONCAT)':<20} | {'DEEPSHIELD ASYMMETRIC':<20}")
    print("="*70)
    print(f"{'Overall Accuracy':<32} | {res_baseline['overall']['accuracy']:<20.4f} | {res_proposed['overall']['accuracy']:<20.4f}")
    print(f"{'Overall ROC-AUC':<32} | {res_baseline['overall']['roc_auc']:<20.4f} | {res_proposed['overall']['roc_auc']:<20.4f}")
    print(f"{'Overall PR-AUC':<32} | {res_baseline['overall']['pr_auc']:<20.4f} | {res_proposed['overall']['pr_auc']:<20.4f}")
    print(f"{'Overall Macro-F1':<32} | {res_baseline['overall']['macro_f1']:<20.4f} | {res_proposed['overall']['macro_f1']:<20.4f}")
    print(f"{'Brier Score (Lower is better)':<32} | {res_baseline['overall']['brier_score']:<20.4f} | {res_proposed['overall']['brier_score']:<20.4f}")

    print("\n" + "-"*70)
    print(f"{'QUADRANT BREAKDOWN ACCURACY':<32} | {'BASELINE':<20} | {'DEEPSHIELD PROPOSED':<20}")
    print("-"*70)
    print(f"{'RR (Real Video + Real Audio)':<32} | {res_baseline['quadrants']['RR']['accuracy']:<20.4f} | {res_proposed['quadrants']['RR']['accuracy']:<20.4f}")
    print(f"{'FR (Fake Video + Real Audio)':<32} | {res_baseline['quadrants']['FR']['accuracy']:<20.4f} | {res_proposed['quadrants']['FR']['accuracy']:<20.4f}")
    print(f"{'RF (Real Video + Fake Audio - Cloned)':<32} | {res_baseline['quadrants']['RF']['accuracy']:<20.4f} | {res_proposed['quadrants']['RF']['accuracy']:<20.4f}")
    print(f"{'FF (Fake Video + Fake Audio)':<32} | {res_baseline['quadrants']['FF']['accuracy']:<20.4f} | {res_proposed['quadrants']['FF']['accuracy']:<20.4f}")

    print("\n" + "-"*70)
    print(f"{'SINGLE-MODALITY FALLBACK (ROBUSTNESS)':<32} | {'BASELINE (ZERO-PAD)':<20} | {'DEEPSHIELD FALLBACK':<20}")
    print("-"*70)
    print(f"{'Audio Missing (Video-Only Input)':<32} | {res_baseline['fallback_video_only']['accuracy']:<20.4f} | {res_proposed['fallback_video_only']['accuracy']:<20.4f}")
    print(f"{'Video Missing (Audio-Only Input)':<32} | {res_baseline['fallback_audio_only']['accuracy']:<20.4f} | {res_proposed['fallback_audio_only']['accuracy']:<20.4f}")
    print("="*70)

    # Save checkpoints
    ckpt_dir = "experiments/multimodal/checkpoints"
    os.makedirs(ckpt_dir, exist_ok=True)
    torch.save(model_baseline.state_dict(), os.path.join(ckpt_dir, "baseline_fusion.pt"))
    torch.save(model_proposed.state_dict(), os.path.join(ckpt_dir, "deepshield_fusion.pt"))
    print(f"[Checkpoints] Saved multimodal models to {ckpt_dir}/")

    # Save final report to JSON
    final_report = {
        "baseline_naive_concat": res_baseline,
        "deepshield_asymmetric_fusion": res_proposed,
    }
    with open(os.path.join(output_dir, "multimodal_report.json"), "w") as f:
        json.dump(final_report, f, indent=2)

    return final_report


if __name__ == "__main__":
    run_multimodal_experiment()
