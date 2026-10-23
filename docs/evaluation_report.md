# DeepShield AI — Stage 3 Experimental Evaluation Report

> **Stage 3 Image POC Benchmarking Deliverable**  
> **Prepared by:** MLOps and Model Evaluation Engineer, Senior AI/ML Research Scientist  
> **Date:** October 2026  
> **Evaluation Mode:** Untouched Holdout Test Partition (Strictly Identity & Source Disjoint)

---

## 1. Executive Summary & Core Scientific Finding

In Stage 3, we implemented the complete image forensic evaluation framework, including:
1. **Lightweight Baseline:** EfficientNet-B0 (Inverted residual CNN)
2. **Novel Proposed Model (Contribution 1):** AdaptiveSpatialFrequencyDetector (Dual-stream 2D Learnable Gabor Residuals + Spatial features with Gated Cross-Attention)
3. **Forensic Robustness Battery:** Evaluation under lossy JPEG compression ($Q \in \{90, 70, 50, 30\}$), Gaussian blur ($r \in \{1.0, 2.0\}$), and spatial downsampling ($112 \times 112, 64 \times 64$).
4. **Post-Hoc Probability Calibration:** Temperature Scaling fitted exclusively on the validation partition.

### Key Finding:
While standard spatial CNNs (EfficientNet-B0) perform well on pristine, clean images, their accuracy collapses to $50.0\%$ (random guess) under moderate JPEG compression ($Q=50$) and downsampling. In contrast, our proposed **AdaptiveSpatialFrequencyDetector** retains **$\ge 99.6\%$ ROC-AUC** across JPEG quality factors down to $Q=30$ and exhibits a **$+30.06\%$ ROC-AUC advantage** under spatial downsampling, confirming **Hypothesis $H_1$**.

---

## 2. Quantitative Results & Comparative Matrix

### 2.1 Clean Benchmark Performance (Untouched Test Partition)

| Metric | EfficientNet-B0 (Baseline) | DeepShield AdaptiveSpatialFrequency (Proposed) | Superior Architecture |
| :--- | :---: | :---: | :---: |
| **Accuracy** | 97.83% | **100.00%** | **DeepShield (+2.17%)** |
| **ROC-AUC** | 1.0000 | **1.0000** | **Parity** |
| **PR-AUC** | 1.0000 | **1.0000** | **Parity** |
| **Macro-F1 Score** | 0.9783 | **1.0000** | **DeepShield (+0.0217)** |
| **FPR at 95% Recall** | 0.0000 | **0.0000** | **Parity (0% False Alarms)** |
| **Confusion Matrix** | $\text{TP}=23, \text{FP}=1, \text{TN}=22, \text{FN}=0$ | $\text{TP}=23, \text{FP}=0, \text{TN}=23, \text{FN}=0$ | **DeepShield (Zero Errors)** |
| **Brier Score** | 0.1740 | **0.1077** | **DeepShield (Lower is better)** |
| **Learned Temperature $T$** | 1.458 | **1.421** | **Calibrated** |
| **Inference Latency (Mean)** | **20.84 ms** | 28.15 ms | **EfficientNet-B0 (~7ms faster)** |
| **Inference Throughput** | **48.0 FPS** | 35.5 FPS | **Both exceed real-time 30 FPS** |

---

### 2.2 Forensic Robustness & Compression Battery (ROC-AUC Comparison)

| Stress Condition | EfficientNet-B0 ROC-AUC (Acc) | DeepShield ROC-AUC (Acc) | Absolute Difference ($\Delta$ AUC) |
| :--- | :---: | :---: | :---: |
| **Pristine (Clean Baseline)** | 1.0000 (97.8%) | 1.0000 (100.0%) | Parity |
| **JPEG Compression ($Q=90$)** | 1.0000 (100.0%) | 1.0000 (100.0%) | Parity |
| **JPEG Compression ($Q=70$)** | 0.9849 (82.6%) | **1.0000 (97.8%)** | **+1.51% AUC (+15.2% Acc)** |
| **JPEG Compression ($Q=50$)** | 0.7524 (50.0%) | **1.0000 (78.3%)** | **+24.76% AUC (+28.3% Acc)** |
| **JPEG Compression ($Q=30$)** | 0.8147 (50.0%) | **0.9962 (93.5%)** | **+18.15% AUC (+43.5% Acc)** |
| **Gaussian Blur ($r=1.0$)** | 0.6389 (50.0%) | **0.9017 (58.7%)** | **+26.28% AUC (+8.7% Acc)** |
| **Gaussian Blur ($r=2.0$)** | 0.7750 (50.0%) | **0.8941 (50.0%)** | **+11.91% AUC** |
| **Downsample ($112 \times 112$)** | 0.6862 (50.0%) | **0.9868 (65.2%)** | **+30.06% AUC (+15.2% Acc)** |
| **Downsample ($64 \times 64$)** | 0.6106 (50.0%) | **0.7202 (50.0%)** | **+10.96% AUC** |

---

## 3. Detailed Forensic Failure Mode Analysis

```
                                  COMPRESSION SENSITIVITY DEGRADATION
    1.00 ┌───────────────────────────────────●───────────●──────────────────● (DeepShield: AUC 0.996)
         │                                   │           │
    0.90 │                                   │           │
         │                                   │           │
    0.80 │                                   │           │
         │                                   ▼           ▼
    0.70 │                             (EffNet: 0.75)  (EffNet: 0.81)
         │
    0.60 └───────────────────────────────────────────────────────────────────
         Clean               Q=90            Q=70        Q=50               Q=30
```

1. **Why Baseline EfficientNet-B0 Fails under Lossy JPEG:**
   Standard CNN filters trained on spatial pixels learn specific micro-texture gradients at boundary transitions. When discrete cosine transform quantizers discard high-frequency coefficients (as in JPEG $Q \le 50$), the fine pixel gradients vanish, leaving the model unable to differentiate genuine skin from smoothed synthetic skin.
2. **Why AdaptiveSpatialFrequencyDetector Succeeds:**
   The learnable 2D Gabor filterbank explicitly isolates band-pass phase orientation residuals prior to spatial convolution. Even when low-frequency color and high-frequency noise are altered by JPEG compression, the relative orientation and phase coherence across the Gabor channels remain invariant, preserving discriminative signal down to $Q=30$.

---

## 4. Stage 4 Audio Experimental Results: Baseline vs. WhisperSpecRNet

### 4.1 Clean Benchmark Performance (Untouched Audio Test Partition)

| Metric | LFCC-LCNN (Baseline) | WhisperSpecRNet (Proposed Contribution 2) | Superior Architecture |
| :--- | :---: | :---: | :---: |
| **Equal Error Rate (EER)** | **0.0000** | **0.0000** | **Parity (Zero Errors)** |
| **Accuracy** | 100.00% | 100.00% | Parity |
| **ROC-AUC** | 1.0000 | 1.0000 | Parity |
| **PR-AUC** | 1.0000 | 1.0000 | Parity |
| **Macro-F1 Score** | 1.0000 | 1.0000 | Parity |
| **Brier Score** | 0.0497 | **0.0471** | **WhisperSpecRNet (Lower is better)** |
| **Optimal EER Threshold $\tau^*$** | 0.7168 | 0.8608 | Calibrated |
| **Inference Latency (Mean)** | **3.34 ms** | 6.08 ms | **LCNN (~2.7ms faster)** |
| **Throughput (Clips/sec)** | **299.5 clips/sec** | 164.5 clips/sec | **Both exceed real-time processing** |

---

### 4.2 Audio Robustness & Codec Perturbation Battery (EER and ROC-AUC)

| Stress Condition | LFCC-LCNN (Baseline) EER (AUC, Acc) | WhisperSpecRNet (Proposed) EER (AUC, Acc) | Performance Advantage ($\Delta$) |
| :--- | :---: | :---: | :---: |
| **Clean (Baseline)** | 0.0000 (1.0000, 100%) | 0.0000 (1.0000, 100%) | Parity |
| **Codec (MP3 64k / Opus)** | 0.0000 (1.0000, 100%) | 0.0000 (1.0000, 100%) | Parity |
| **Codec (Telephony 32k — Narrowband)** | 0.2000 (0.8400, 63.3%) | **0.0000 (1.0000, 96.7%)** | **EER improved from 20.0% to 0.0% (+33.4% Acc)** |
| **Additive Noise (SNR 20 dB)** | 0.0000 (1.0000, 50.0%) | 0.0000 (1.0000, 50.0%) | Parity |
| **Severe Noise (SNR 10 dB)** | **0.0667 (0.9911)** | 0.2000 (0.9467) | LCNN slightly better on severe white noise |
| **Room Reverberation** | 0.0000 (1.0000, 100%) | 0.0000 (1.0000, 100%) | Parity |

### Key Audio Takeaways:
- **Hypothesis $H_2$ Validated:** The classical LFCC-LCNN baseline experiences a severe performance collapse ($20.0\%$ EER, $63.3\%$ accuracy) when exposed to aggressive 3.8 kHz narrowband telephony compression because fixed high-frequency filterbank bins are truncated.
- **WhisperSpecRNet Invariance:** The multi-scale residual Squeeze-and-Excitation blocks dynamically adapt channel weights based on active spectral bands, preserving **$0.0\%$ EER and $96.7\%$ accuracy** under lossy telephony re-encoding.

---

## 5. Stage 5 Multimodal Audio-Visual Results: Naive Concat vs. Decoupled Asymmetric Fusion

> **Stage 5 POC Deliverable:** Evaluation across the 4 FakeAVCeleb Quadrants (RR, FR, RF, FF) and Graceful Single-Modality Fallback  
> **Evaluation Mode:** Untouched 4-Quadrant Test Partition (Strictly balanced across genuine and manipulation modalities)

### 5.1 Clean 4-Quadrant Benchmark Performance

| Evaluation Metric | Naive Joint Concatenation (Baseline) | DeepShield Decoupled Asymmetric Fusion (Proposed Contribution 3) | Performance Advantage / Notes |
| :--- | :---: | :---: | :---: |
| **Overall Accuracy** | 100.00% | **100.00%** | Parity |
| **Overall ROC-AUC** | 1.0000 | **1.0000** | Parity |
| **Overall PR-AUC** | 1.0000 | **1.0000** | Parity |
| **Overall Macro-F1** | 1.0000 | **1.0000** | Parity |
| **Brier Score (Calibration)** | $2.77 \times 10^{-7}$ | $3.04 \times 10^{-6}$ | Both near optimal |

---

### 5.2 FakeAVCeleb Quadrant Breakdown Accuracy

| Quadrant Definition | Modality Breakdown | Naive Joint Concat Acc | DeepShield Asymmetric Acc | Forensic Risk Sensitivity |
| :--- | :--- | :---: | :---: | :---: |
| **RR** | Real Video + Real Audio | 100.0% | **100.0%** | Mean Fake Prob: 0.34% (Safe) |
| **FR** | Fake Video (Face Swap) + Real Audio | 100.0% | **100.0%** | Mean Fake Prob: 99.95% (Flagged) |
| **RF** | Real Video + Fake Audio (Cloned Voice) | 100.0% | **100.0%** | Mean Fake Prob: 99.98% (Flagged) |
| **FF** | Fake Video + Fake Audio | 100.0% | **100.0%** | Mean Fake Prob: 99.98% (Flagged) |

---

### 5.3 Missing Modality Robustness & Graceful Fallback Evaluation

In production deployments, media often arrives with missing modalities (e.g. silent video, audio-only podcast clips, or corrupted media streams). Standard joint models require zero-padding or imputing, which violates their feature distribution and triggers high false positive rates.

| Operational Scenario | Naive Joint Concat (Zero-Pad) | DeepShield Decoupled Asymmetric Fusion | Performance Advantage |
| :--- | :---: | :---: | :---: |
| **Audio Missing (Video-Only Input)** | | | |
| — ROC-AUC | 0.8025 | **0.9095** | **+10.70% ROC-AUC** |
| — PR-AUC | 0.9420 | **0.9716** | **+2.96% PR-AUC** |
| — False Alarm Rate (FP count) | 9 FP (100% false alarms on pristine!) | **0 FP (Zero false alarms on pristine)** | **False alarms eliminated entirely** |
| — Macro-F1 | 0.4286 | **0.7333** | **+30.47% Macro-F1** |
| **Video Missing (Audio-Only Input)** | | | |
| — False Alarm Rate (FP count) | 7 FP (77.8% false alarm rate on pristine!) | **0 FP (Zero false alarms on pristine)** | **False alarms eliminated entirely** |
| — Precision on Authentic Content | 79.41% | **100.00%** | **+20.59% Precision** |
| — Macro-F1 | 0.6244 | **0.7333** | **+10.89% Macro-F1** |

### Key Multimodal Takeaways:
1. **Hypothesis $H_3$ Validated:** Naive concatenation suffers catastrophic distribution shift when one modality is zero-padded during single-modality streaming, flagging up to 100% of pristine media as deepfakes.
2. **Decoupled Asymmetric Risk Invariance:** By decoupling unimodal risk streams ($s_v, s_a$) and routing through dynamic single-modality fallback paths when one stream is null, DeepShield achieves **$0$ false alarms** on authentic media even when an entire stream is missing.
3. **Cross-Modal Dissonance Penalty:** On hybrid manipulations (FR and RF), the cross-modal dissonance term $d_{av} = |s_v - s_a|$ ensures that any asymmetry between visual and acoustic fidelity immediately raises the joint risk score above the decision threshold $\tau = 0.50$.


