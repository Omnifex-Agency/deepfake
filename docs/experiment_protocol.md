# DeepShield AI — Standardized Experimental & Evaluation Protocol

> **Scientific Evaluation & Benchmarking Standards**  
> **Prepared by:** MLOps and Model Evaluation Engineer, Senior AI/ML Research Scientist  
> **Date:** October 2026

---

## 1. Primary Evaluation Metrics & Mathematical Formulations

To ensure strict comparability across baselines and novel architectures, every experiment must report the following metrics:

### 1.1 Classification Performance Metrics
- **Accuracy (ACC):**
  $$\text{ACC} = \frac{TP + TN}{TP + TN + FP + FN}$$
- **Precision (P), Recall (R), and Macro-F1:**
  $$P = \frac{TP}{TP + FP}, \quad R = \frac{TP}{TP + FN}, \quad F_1 = 2 \cdot \frac{P \cdot R}{P + R}$$
  Macro-$F_1$ averages $F_1$ independently across bonafide and synthetic classes to prevent minority class masking.
- **ROC-AUC (Area Under the Receiver Operating Characteristic Curve):**
  Evaluates True Positive Rate versus False Positive Rate across all classification thresholds $\tau \in [0, 1]$.
- **PR-AUC (Area Under the Precision-Recall Curve):**
  Mandatory for imbalanced evaluation (e.g., real-world 1:99 fake-to-real distribution).
- **False Positive Rate at 95% Recall (FPR95):**
  Measures the false alarm rate when the system is tuned to catch 95% of all deepfakes. Essential for legal and compliance applications.

### 1.2 Audio Anti-Spoofing Metrics
- **Equal Error Rate (EER):**
  The operational operating point where the False Acceptance Rate (FAR) equals the False Rejection Rate (FRR):
  $$\text{EER} = \text{FAR}(\tau^*) = \text{FRR}(\tau^*)$$
- **Minimum Tandem Detection Cost Function ($\min t\text{-DCF}$):**
  Standard ASVspoof metric evaluating the impact of spoofing countermeasures on an automatic speaker verification (ASV) system:
  $$t\text{-DCF} = C_{\text{miss}} \cdot P_{\text{target}} \cdot P_{\text{miss}}^{\text{cm}} + C_{\text{fa}} \cdot P_{\text{nontarget}} \cdot P_{\text{fa}}^{\text{cm}}$$

### 1.3 Calibration & Uncertainty Metrics
- **Expected Calibration Error (ECE):**
  Measures the correspondence between predicted confidence $\hat{p}$ and empirical ground-truth accuracy across $M=15$ equally spaced bins:
  $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
- **Brier Score:**
  Mean squared error between predicted probabilities and one-hot ground-truth labels:
  $$\text{BS} = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$$

### 1.4 Computational & System Efficiency Metrics
- **Inference Latency:** Mean and 95th percentile latency (ms per sample) measured across 1,000 warm iterations.
- **Peak GPU VRAM Usage:** Tracked via `torch.cuda.max_memory_allocated()`.
- **Parameter Count & Checkpoint Footprint:** Total trainable versus frozen parameters.

---

## 2. Robustness Perturbation Benchmarks

Every candidate model must be evaluated under five standardized stress tests:

```
                               ROBUSTNESS EVALUATION BATTERY
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 1. JPEG Compression:    Evaluate at Quality Factors Q ∈ {95, 80, 70, 50, 30}     │
│ 2. Spatial Resizing:    Bicubic downscale to {128x128, 96x96} then restore to 224│
│ 3. Additive Noise:      Gaussian noise (σ ∈ {5, 10, 15}) & Poisson sensor noise  │
│ 4. Audio Codec Sweep:   Opus (16, 24, 32 kbps), AAC (32, 64 kbps), MP3 (64 kbps) │
│ 5. Cross-Generator OOD: Zero-shot evaluation on completely unseen generative AI: │
│                         • Image: Stable Diffusion v1.5, Midjourney v4, Celeb-DF  │
│                         • Audio: ElevenLabs cloned speech, Bark, Tortoise-TTS    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Leakage Prevention Checklist

Before running any training script, the following four assertions must pass:
1. `assert len(set(train_identities).intersection(set(test_identities))) == 0` (Zero identity leakage).
2. `assert len(set(train_source_videos).intersection(set(test_source_videos))) == 0` (Zero source clip leakage).
3. All feature normalization statistics (mean, std) must be computed strictly on the training set and applied frozen to validation and test sets.
4. Post-hoc calibration (Temperature Scaling) must be fitted on the **validation set only**, and evaluated on the untouched test set.
