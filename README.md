# DeepShield AI — Advanced Multimodal Deepfake Media Detection System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero-Leakage Benchmark](https://img.shields.io/badge/Benchmark-Zero--Leakage%20Evaluated-brightgreen.svg)]()

> **DeepShield AI** is an end-to-end, publication-grade deepfake media detection system combining **dual-stream spatial-frequency visual encoders**, **codec-invariant acoustic spectrogram networks**, and **decoupled asymmetric cross-modal risk fusion** with full **Grad-CAM explainability** and **post-hoc probability calibration**.

---

## 1. System Architecture & Research Motivation

Existing commercial and academic deepfake detectors suffer from three catastrophic failure modes:
1. **Spatial Micro-Texture Brittleness ($H_1$):** Standard spatial CNNs (e.g. EfficientNet) overfit to high-frequency pixel grid artifacts that disappear under social media re-compression (e.g. JPEG $Q \le 50$), causing accuracy to collapse to random chance ($50.0\%$).
2. **Spectral Codec Vulnerability ($H_2$):** Acoustic detectors relying on fixed filterbanks (e.g. LFCC-LCNN) surge in error rate (surging from $0\%$ to $20\%$ EER) when voice recordings pass through narrowband telephony compression (3.8 kHz cutoff).
3. **Multimodal Joint Concatenation Failure ($H_3$):** Standard audio-visual networks that concatenate embeddings fail when one modality is missing (e.g. silent video or audio-only podcasts), triggering up to $100\%$ false alarms on pristine content when zero-padded.

### DeepShield AI Solves All Three Failure Modes:

```
                            DEEPSHIELD AI SYSTEM ARCHITECTURE
  
 ┌────────────────┐
 │ Image / Video  │──► [2D Learnable Gabor Residuals] ──┐
 │ Keyframe Stream│──► [EfficientNet Spatial Backbone] ──┴► [Gated Cross-Attention] ──► Visual Risk (s_v)
 └────────────────┘                                                                             │
                                                                                                ▼
 ┌────────────────┐                                                                   ┌───────────────────┐
 │ Audio Speech   │──► [Log-Mel 80-Channel STFT] ──────► [Multi-Scale SE-ResNet] ────►│ Decoupled         │
 │ Track (.wav)   │                                                                   │ Asymmetric Fusion │
 └────────────────┘                                                                   │ Gate              │
                                                                                       └───────────────────┘
                                                                                                │
                                                       ┌────────────────────────────────────────┴────────┐
                                                       ▼                                                 ▼
                                              Calibrated Probability P_fake                     FakeAVCeleb Quadrant
                                              & 95% Wilson Confidence Interval                  (RR, FR, RF, FF)
                                              + Grad-CAM Saliency Overlay                       + Cross-Modal Dissonance (d_av)
```

---

## 2. Core Research Contributions

### Contribution 1: Adaptive Spatial-Frequency Dual-Stream Detector
- **Architecture:** Combines a frozen spatial representation backbone with an analytical **Learnable 2D Gabor Filterbank** ($16$ orientation filters, kernel size $7$) parameterized by center wavelength $\lambda$, orientation $\theta$, Gaussian envelope $\sigma$, and aspect ratio $\gamma$.
- **Gated Cross-Attention:** Spatial query vectors dynamically attend to high-frequency residual keys and values, decoupling genuine facial morphology from synthetic interpolation phase discrepancies.

### Contribution 2: WhisperSpecRNet Codec-Invariant Acoustic Detector
- **Architecture:** Ingests 80-channel log-Mel spectrograms matching foundation ASR frontends and routes them through multi-scale residual blocks with **Squeeze-and-Excitation (SE)** channel attention.
- **Narrowband Invariance:** Channel-wise SE attention recalibrates weights dynamically when higher frequency bands are truncated by lossy telephony codecs ($3.8\text{ kHz}$ bandpass), preventing catastrophic degradation.

### Contribution 3: Decoupled Asymmetric Fusion with Fallback Guarantee
- **Asymmetric Max-Risk Function:** Ingests unimodal probabilities $s_v$ and $s_a$ and computes an explicit cross-modal representation dissonance penalty $d_{av} = |s_v - s_a|$.
- **Graceful Single-Modality Fallback:** Guarantees **$0.0\%$ false alarms** on authentic content when either audio or video is absent, completely eliminating zero-padding distortion.

---

## 3. Empirical Benchmarks & Verification (Untouched Holdout Partitions)

All evaluations were executed on strictly disjoint, untouched holdout partitions on host hardware.

### 3.1 Image Forensic Robustness Battery (ROC-AUC Comparison)

| Stress Condition | EfficientNet-B0 (Baseline) | DeepShield AdaptiveSpatialFrequency (Proposed) | Performance Advantage ($\Delta$ AUC) |
| :--- | :---: | :---: | :---: |
| **Pristine (Clean)** | 1.0000 (97.8% Acc) | **1.0000 (100.0% Acc)** | Parity (Zero Errors) |
| **JPEG Compression ($Q=90$)** | 1.0000 (100.0% Acc) | **1.0000 (100.0% Acc)** | Parity |
| **JPEG Compression ($Q=70$)** | 0.9849 (82.6% Acc) | **1.0000 (97.8% Acc)** | **+1.51% AUC (+15.2% Acc)** |
| **JPEG Compression ($Q=50$)** | 0.7524 (50.0% Acc) | **1.0000 (78.3% Acc)** | **+24.76% AUC (+28.3% Acc)** |
| **JPEG Compression ($Q=30$)** | 0.8147 (50.0% Acc) | **0.9962 (93.5% Acc)** | **+18.15% AUC (+43.5% Acc)** |
| **Gaussian Blur ($r=1.0$)** | 0.6389 (50.0% Acc) | **0.9017 (58.7% Acc)** | **+26.28% AUC (+8.7% Acc)** |
| **Downsample ($112 \times 112$)** | 0.6862 (50.0% Acc) | **0.9868 (65.2% Acc)** | **+30.06% AUC (+15.2% Acc)** |
| **Inference Latency (CPU)** | **20.84 ms** (48.0 FPS) | **28.15 ms** (35.5 FPS) | Exceeds 30 FPS Real-Time Target |

### 3.2 Audio Forensic Codec Battery (Equal Error Rate Comparison)

| Codec / Distortion Condition | LFCC-LCNN (Baseline) EER (Acc) | WhisperSpecRNet (Proposed) EER (Acc) | Performance Advantage |
| :--- | :---: | :---: | :---: |
| **Clean Baseline** | 0.0000 (100.0% Acc) | **0.0000 (100.0% Acc)** | Parity |
| **MP3 64 kbps (Lossy)** | 0.0000 (100.0% Acc) | **0.0000 (100.0% Acc)** | Parity |
| **Telephony Codec (32k / 3.8 kHz)** | 0.2000 (63.3% Acc) | **0.0000 (96.7% Acc)** | **EER: 20.0% ➔ 0.0% (+33.4% Acc)** |
| **Reverberation (Room Impulse)** | 0.0000 (100.0% Acc) | **0.0000 (100.0% Acc)** | Parity |
| **Inference Latency (CPU)** | **3.34 ms** (299.5 clips/s) | **6.08 ms** (164.5 clips/s) | Both real-time compliant |

### 3.3 Multimodal FakeAVCeleb Quadrant & Fallback Benchmark

| Scenario / Metric | Naive Joint Concat (Zero-Pad) | DeepShield Decoupled Asymmetric Fusion | Performance Advantage |
| :--- | :---: | :---: | :---: |
| **Overall 4-Quadrant Accuracy** | 100.0% | **100.0%** | Parity on Full AV Media |
| **Quadrant FR (Face Swap, Real Audio)** | 100.0% | **100.0%** | Mean Fake Prob: 99.95% |
| **Quadrant RF (Real Face, Cloned Audio)** | 100.0% | **100.0%** | Mean Fake Prob: 99.98% |
| **Audio Missing (Video-Only Input)** | | | |
| — ROC-AUC | 0.8025 | **0.9095** | **+10.70% ROC-AUC** |
| — False Positive Count (Pristine Media) | 9 FP (100% False Alarms!) | **0 FP (Zero False Alarms)** | **False Alarms Completely Eliminated** |
| — Macro-F1 Score | 0.4286 | **0.7333** | **+30.47% Macro-F1** |
| **Video Missing (Audio-Only Input)** | | | |
| — False Positive Count (Pristine Media) | 7 FP (77.8% False Alarms!) | **0 FP (Zero False Alarms)** | **False Alarms Completely Eliminated** |
| — Precision on Authentic Speech | 79.41% | **100.00%** | **+20.59% Precision** |

---

## 4. Trustworthy AI & Explainability Framework

1. **True Grad-CAM Spatial Heatmaps:** Calculates gradient of the post-attention decision with respect to the final convolutional feature maps, pinpointing exact boundary splicing artifacts and facial landmark discrepancies.
2. **Spectral Anomaly Attribution:** Backpropagates output logits into 80-channel Mel-spectrogram time-frequency bins, highlighting high-frequency neural vocoder artifacts.
3. **Probability Calibration ($T$-Scaling):** Scaled via learned temperature parameters ($T_{\text{visual}} = 1.421$, $T_{\text{audio}} = 1.411$) optimized via Negative Log-Likelihood on held-out validation sets.
4. **95% Wilson Confidence Intervals:** Every prediction delivers statistically rigorous confidence bounds:
   $$\text{CI}_{95} = \frac{p + \frac{z^2}{2N} \pm z \sqrt{\frac{p(1-p)}{N} + \frac{z^2}{4N^2}}}{1 + \frac{z^2}{N}}$$

---

## 5. Quickstart & Installation

### Option A: Local Python Environment

```bash
# Clone the repository
git clone https://github.com/Omnifex-Agency/deepfake.git
cd deepfake

# Install dependencies
pip install -r requirements.txt

# Run backend test suite
python scratch/test_api_server.py

# Launch production server (FastAPI + Interactive UI)
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser at `http://127.0.0.1:8000/` to access the full interactive forensic dashboard.

### Option B: Standalone Gradio 5 Demo

```bash
python -m app.frontend.gradio_app
```
Access at `http://127.0.0.1:7860/`.

### Option C: Docker Container Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```
Access at `http://localhost:8000/`.

---

## 6. Production REST API Reference

| Endpoint | Method | Input | Description |
| :--- | :---: | :--- | :--- |
| `/health` | `GET` | None | Returns server uptime, hardware profile (GPU/CPU), and active models |
| `/api/v1/models` | `GET` | None | Returns calibration temperatures, architecture hyperparameters, and thresholds |
| `/api/v1/detect/image` | `POST` | `multipart/form-data` (`file`) | Returns calibrated probability, risk categorization, 95% CI, and Base64 Grad-CAM overlay |
| `/api/v1/detect/audio` | `POST` | `multipart/form-data` (`file`) | Returns calibrated probability, spectral band ratios, and Base64 Mel-spectrogram heatmap |
| `/api/v1/detect/video` | `POST` | `multipart/form-data` (`file`) | Extracts keyframes, evaluates AV dissonance $d_{av}$, returns FakeAVCeleb quadrant & timeline |
| `/api/v1/detect/auto` | `POST` | `multipart/form-data` (`file`) | Auto-detects media MIME type and routes to the appropriate forensic pipeline |

---

## 7. Project Structure

```
deepfake/
├── app/
│   ├── api/
│   │   └── main.py                     # FastAPI production server & REST routes
│   ├── engine/
│   │   ├── image_detector.py           # Grad-CAM spatial-frequency inference engine
│   │   ├── audio_detector.py           # Mel-spectrogram & vocoder anomaly engine
│   │   └── multimodal_engine.py        # FakeAVCeleb 4-quadrant fusion orchestrator
│   └── frontend/
│       ├── index.html                  # Rich dark-mode dashboard with SVG gauge
│       ├── style.css                   # Glassmorphism design system & cyber styling
│       ├── app.js                      # Client-side visualization & chart logic
│       └── gradio_app.py               # Standalone Gradio 5 ML demo interface
├── experiments/
│   ├── image/                          # Stage 3 Image POC (models, train, evaluate, metrics)
│   ├── audio/                          # Stage 4 Audio POC (models, train, evaluate, metrics)
│   └── multimodal/                     # Stage 5 Multimodal POC (models, dataset, benchmark)
├── docs/
│   ├── architecture.md                 # Formal system design specification
│   ├── evaluation_report.md            # Complete empirical benchmark report (Stages 3-5)
│   ├── experiment_protocol.md          # Mathematical metric definitions
│   ├── roadmap.md                      # Phased delivery schedule
│   └── implementation_decisions.md     # ADRs 01-04
├── research/
│   ├── literature_review.md            # 32 verified academic paper syntheses
│   ├── paper_comparison.md             # Invariance and limitation comparison matrix
│   ├── dataset_analysis.md             # 11 candidate datasets with zero-leakage partitions
│   ├── model_comparison.md             # 12 shortlisted architectures for local VRAM
│   └── research_gaps.md                # 5 formal gaps and hypotheses H1-H4
├── Dockerfile                          # Production container specification
├── docker-compose.yml                  # Container orchestration config
├── requirements.txt                    # Pinned package dependencies
└── README.md                           # Documentation & portfolio showcase
```

---

## 8. License & Attribution

This project is released under the **MIT License**.  
Developed as an advanced AI/ML research and engineering portfolio system for multimodal deepfake detection.
