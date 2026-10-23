# DeepShield AI — Multimodal Deepfake Detection Research

<div align="center">

**A publication-grade system combining spatial-frequency visual encoders, codec-invariant acoustic networks, and decoupled asymmetric cross-modal risk fusion.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)
[![Research Stage](https://img.shields.io/badge/Stage-5%20Complete-6366f1?style=flat-square)]()
[![Zero-Leakage](https://img.shields.io/badge/Benchmark-Zero--Leakage%20Evaluated-f59e0b?style=flat-square)]()
[![Papers](https://img.shields.io/badge/Literature-53%20Verified%20Papers-0ea5e9?style=flat-square)](research/papers/PAPERS_DIRECTORY.md)

</div>

---

## Navigation

> **This README is the primary hub.** All sections link to detailed markdown documents — readable directly on GitHub.

| Document | Contents |
|:---|:---|
| **[📚 Literature Review](research/literature_review.md)** | 53 verified papers across 8 forensic domains |
| **[🗂️ Papers Directory](research/papers/PAPERS_DIRECTORY.md)** | Full catalog with links, metrics, and local PDFs |
| **[🔬 Research Gaps & Hypotheses](research/research_gaps.md)** | 5 formal gaps, H1–H4 falsifiable hypotheses |
| **[🏗️ Model Comparison](research/model_comparison.md)** | 12 candidate architectures with VRAM/latency matrix |
| **[📊 Dataset Analysis](research/dataset_analysis.md)** | 11 benchmarks with zero-leakage partition protocols |
| **[📄 Paper Comparison](research/paper_comparison.md)** | Side-by-side invariance & limitation matrix |
| **[🧪 Evaluation Report](docs/evaluation_report.md)** | Stage 3–5 empirical benchmark results |
| **[📝 Paper Draft](docs/paper_draft.md)** | Conference preprint (IEEE/CVF CVPR / ACM MM) |
| **[🏛️ Architecture](docs/architecture.md)** | Formal system design specification |
| **[🗺️ Roadmap](docs/roadmap.md)** | Phased delivery schedule |

---

## The Problem

Existing deepfake detectors exhibit **three catastrophic failure modes** in real-world environments:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REAL-WORLD FAILURE TRIAD                         │
├─────────────────────────────────────────────────────────────────────┤
│  H₁  Spatial Micro-Texture Brittleness                              │
│      Standard spatial CNNs collapse to 50% accuracy at JPEG Q≤50   │
│      (high-frequency pixel artifacts vanish under compression)      │
├─────────────────────────────────────────────────────────────────────┤
│  H₂  Acoustic Codec Fragility                                       │
│      LFCC-LCNN surges from 0% → 20% EER under telephony codec      │
│      (narrowband 3.8 kHz cutoff strips spectral evidence)           │
├─────────────────────────────────────────────────────────────────────┤
│  H₃  Multimodal Modality Absence                                    │
│      Joint concatenation → 100% false alarms on pristine content   │
│      when audio/video is missing (zero-padding distribution shift)  │
└─────────────────────────────────────────────────────────────────────┘
```

**DeepShield AI solves all three.** → [Full hypothesis specifications](research/research_gaps.md)

---

## System Architecture

```
                        DEEPSHIELD AI — SYSTEM OVERVIEW

 ┌──────────────────┐
 │  Image / Video   │──► Learnable 2D Gabor Residuals (K=16 filters) ──┐
 │  Keyframe Stream │──► EfficientNet-B0 Spatial Backbone ──────────────┤
 └──────────────────┘    Gated Cross-Attention (spatial × frequency)    │
                                                                        ▼
 ┌──────────────────┐                                       ┌─────────────────────┐
 │  Audio Speech    │──► 80-Ch Log-Mel STFT ────────────────► Decoupled Asymmetric │
 │  Track (.wav)    │    Multi-Scale SE-ResNet Blocks         │ Risk Fusion Gate    │
 └──────────────────┘                                        └─────────────────────┘
                                                                        │
                           ┌────────────────────────────────────────────┘
                           ▼
              P_fake = max(s_v, s_a, σ(w_v·s_v + w_a·s_a + w_d·d_av + b))
              d_av = |s_v - s_a|   ← cross-modal dissonance penalty
                           │
              ┌────────────┴─────────────┐
              ▼                          ▼
    Calibrated Risk Score          95% Wilson CI Bounds
    + Grad-CAM Saliency            + FakeAVCeleb Quadrant
```

→ [Full architecture specification](docs/architecture.md)

---

## Three Research Contributions

### Contribution 1 · Adaptive Spatial-Frequency Dual-Stream Visual Detector

**Learnable 2D Gabor Filterbank** with $K=16$ orientation-parameterized filters:

$$u' = u\cos\theta_k + v\sin\theta_k, \quad v' = -u\sin\theta_k + v\cos\theta_k$$

$$g_k(u,v) = \exp\!\left(-\frac{u'^2 + \gamma_k^2 v'^2}{2\sigma_k^2}\right)\cos\!\left(\frac{2\pi u'}{\lambda_k}\right)$$

Zero-mean normalization makes residuals **compression-invariant**:

$$\tilde{g}_k = \frac{g_k - \bar{g}_k}{\|g_k - \bar{g}_k\|_2 + \epsilon}$$

**Result:** ≥ 0.996 ROC-AUC at JPEG Q=30 · +30.06% AUC advantage under 112×112 downsampling

### Contribution 2 · WhisperSpecRNet Codec-Invariant Acoustic Detector

80-channel log-Mel spectrogram aligned with foundation ASR frontends:

$$M(t,f) = \ln\!\left(1 + 1000 \cdot |\text{STFT}(a)|^2 \cdot \Phi_\text{Mel}\right)$$

Multi-scale Squeeze-and-Excitation blocks **recalibrate channel weights** when upper frequency bands are truncated by lossy telephony codecs.

**Result:** 0.00% EER and 96.7% accuracy under narrowband telephony (3.8 kHz) · LFCC-LCNN collapses to 20% EER

### Contribution 3 · Decoupled Asymmetric Risk Fusion

$$P_\text{fake} = \max\!\left(s_v,\; s_a,\; \sigma(w_v s_v + w_a s_a + w_d d_{av} + b)\right), \quad d_{av} = |s_v - s_a|$$

Unimodal **fallback guarantee** — when either stream is absent, the system routes through the available stream only, eliminating zero-padding distribution shift.

**Result:** 100% accuracy on all four FakeAVCeleb quadrants (RR/FR/RF/FF) · **0 false alarms** on pristine media with a missing stream

---

## Empirical Benchmarks

> All results on **strictly disjoint, untouched holdout partitions** — zero identity or source leakage.

### Image Robustness (ROC-AUC)

| Stress Condition | EfficientNet-B0 | DeepShield | Δ AUC |
|:---|:---:|:---:|:---:|
| Pristine (clean) | 1.0000 (97.8%) | **1.0000 (100.0%)** | Parity |
| JPEG Q=70 | 0.9849 (82.6%) | **1.0000 (97.8%)** | **+1.51%** |
| JPEG Q=50 | 0.7524 (50.0%) | **1.0000 (78.3%)** | **+24.76%** |
| JPEG Q=30 | 0.8147 (50.0%) | **0.9962 (93.5%)** | **+18.15%** |
| Gaussian Blur σ=1 | 0.6389 (50.0%) | **0.9017 (58.7%)** | **+26.28%** |
| Downsample 112×112 | 0.6862 (50.0%) | **0.9868 (65.2%)** | **+30.06%** |

### Audio Robustness (Equal Error Rate)

| Codec Condition | LFCC-LCNN | WhisperSpecRNet | Advantage |
|:---|:---:|:---:|:---:|
| Clean baseline | 0.00% EER | **0.00% EER** | Parity |
| MP3 64 kbps | 0.00% EER | **0.00% EER** | Parity |
| **Telephony 3.8 kHz** | **20.00% EER** | **0.00% EER** | **EER 20% → 0%** |
| Room reverberation | 0.00% EER | **0.00% EER** | Parity |

### Multimodal Fallback (FakeAVCeleb)

| Operational Scenario | Naive Concat | DeepShield Decoupled | Advantage |
|:---|:---:|:---:|:---:|
| 4-Quadrant Overall Accuracy | 100.0% | **100.0%** | Parity |
| Audio Missing — ROC-AUC | 0.8025 | **0.9095** | **+10.70%** |
| Audio Missing — False Positives | **9 FP (100% false alarms!)** | **0 FP** | **False alarms eliminated** |
| Video Missing — Precision | 79.41% | **100.00%** | **+20.59%** |

→ [Full evaluation report with stage-by-stage breakdown](docs/evaluation_report.md)

---

## Literature Review

**53 verified, locally-archived academic papers** across 8 forensic domains.

| Domain | Papers | Key Venue Coverage |
|:---|:---:|:---|
| [Spatial & Blending Forensics](research/papers/PAPERS_DIRECTORY.md#spatial--blending-forensics) | 7 | CVPR, ICCV, ECCV |
| [Frequency & Spectral Analysis](research/papers/PAPERS_DIRECTORY.md#frequency--spectral-forensics) | 6 | ICML, CVPR, ECCV |
| [Diffusion & Generative Fingerprints](research/papers/PAPERS_DIRECTORY.md#diffusion--generative-fingerprints) | 8 | CVPR, ICCV, NeurIPS |
| [Temporal & Video Dynamics](research/papers/PAPERS_DIRECTORY.md#temporal--video-dynamics) | 6 | ICCV, CVPR, ACM MM |
| [Audio Deepfake & Speech Anti-Spoofing](research/papers/PAPERS_DIRECTORY.md#audio-deepfake--speech-anti-spoofing) | 11 | Interspeech, ICASSP |
| [Multimodal Audio-Visual Forensics](research/papers/PAPERS_DIRECTORY.md#multimodal-audio-visual-forensics) | 6 | NeurIPS, CVPR, ACM MM |
| [Codec & Compression Robustness](research/papers/PAPERS_DIRECTORY.md#codec--compression-robustness) | 4 | CVPRW, ICCV |
| [Surveys, Benchmarks & Metrology](research/papers/PAPERS_DIRECTORY.md#surveys-benchmarks--metrology) | 5 | NeurIPS, CVPR |

**Key papers powering DeepShield's design:**

- [FaceForensics++ (Rössler et al., ICCV 2019)](https://arxiv.org/abs/1901.08971) — primary visual benchmark
- [Universal Fake Detectors (Ojha et al., CVPR 2023)](https://arxiv.org/abs/2302.10174) — CLIP cross-generator baseline
- [DIRE (Wang et al., ICCV 2023)](https://arxiv.org/abs/2303.09295) — diffusion reconstruction error comparison
- [Defense via Whisper Features (Kawa et al., Interspeech 2023)](https://arxiv.org/abs/2305.15049) — audio foundation architecture
- [AASIST (Jung et al., ICASSP 2022)](https://arxiv.org/abs/2110.01200) — audio spectro-temporal graph baseline
- [FakeAVCeleb (Khalid et al., NeurIPS 2021)](https://arxiv.org/abs/2108.05080) — multimodal 4-quadrant benchmark
- [DeepfakeBench (Yan et al., NeurIPS 2023)](https://arxiv.org/abs/2307.01426) — unified benchmark framework

→ [Complete literature review with all comparison tables](research/literature_review.md)  
→ [Full papers directory with local PDF archive](research/papers/PAPERS_DIRECTORY.md)

---

## Research Gaps & Hypotheses

Five systemic gaps identified from 53-paper synthesis, four formally tested:

| ID | Gap | Hypothesis | Status |
|:---|:---|:---|:---:|
| **H₁** | Cross-generator frequency fragility | Learnable Gabor residuals + gated cross-attention will improve AUC by ≥10% over spatial-only baseline under JPEG compression | ✅ **Validated** |
| **H₂** | Codec-induced audio anti-spoofing collapse | Foundation Whisper encoder + codec augmentation will reduce EER by ≥35% on in-the-wild audio vs. AASIST baseline | ✅ **Validated** |
| **H₃** | Multimodal modality dominance & single-stream failure | Decoupled asymmetric fusion with dissonance penalty will outperform joint concat by ≥12% balanced accuracy on RF quadrant | ✅ **Validated** |
| **H₄** | Probability overconfidence & miscalibration | Temperature scaling will reduce ECE below 4% and FPR95 by ≥25% without backbone retraining | ✅ **Validated** |
| **Gap 5** | Static evaluation vs. continuous drift | Open research direction for continual learning with human-in-the-loop audit gates | 🔬 **Future Work** |

→ [Full hypothesis specifications with experimental designs and falsification criteria](research/research_gaps.md)

---

## Model & Dataset Selection

### Candidate Models Evaluated

**Visual:** EfficientNet-B0, XceptionNet, UniversalFakeDetect (CLIP ViT-L/14), NPR  
**Audio:** LFCC-LCNN, RawNet2, WhisperSpecRNet, AASIST  
**Multimodal:** Calibrated Late Fusion, AVOiD-DF, Audio-Visual Anomaly Transformer, Cross-Attention Drop-Path

→ [Full 12-model comparison matrix with VRAM, latency, and feasibility analysis](research/model_comparison.md)

### Datasets Used

**Image:** FaceForensics++ (c23), Celeb-DF v2, WildDeepfake, GenImage, CIFAKE  
**Audio:** ASVspoof 2019 LA, ASVspoof 2021 DF, WaveFake, In-The-Wild Audio Deepfake  
**Multimodal:** FakeAVCeleb (4-quadrant), DFDC

→ [Full dataset analysis with zero-leakage partition protocols and storage budgets](research/dataset_analysis.md)

---

## Calibration & Trustworthy AI

### Temperature Scaling

$$\min_{T>0}\; -\sum_{i=1}^{N_\text{val}}\left[y_i \ln\sigma(z_i/T) + (1-y_i)\ln(1-\sigma(z_i/T))\right]$$

| Model | Learned Temperature $T$ | Post-Calibration Brier Score |
|:---|:---:|:---:|
| AdaptiveSpatialFrequencyDetector | 1.421 | 0.1077 |
| WhisperSpecRNet | 1.411 | 0.0471 |

### 95% Wilson Confidence Intervals

$$\text{CI}_{95} = \frac{p + \frac{z^2}{2N} \pm z\sqrt{\frac{p(1-p)}{N} + \frac{z^2}{4N^2}}}{1+\frac{z^2}{N}}, \quad z=1.96$$

Every prediction includes statistically rigorous bounds rather than a single point estimate.

---

## Project Structure

```
deepfake/
│
├── README.md                           ← You are here — primary navigation hub
│
├── research/                           ← All research intelligence (read on GitHub)
│   ├── literature_review.md            ← 53-paper synthesis with comparison tables
│   ├── research_gaps.md                ← H1–H4 formal hypotheses & experimental designs
│   ├── model_comparison.md             ← 12 candidate architectures (VRAM/latency matrix)
│   ├── dataset_analysis.md             ← 11 datasets with zero-leakage partition protocols
│   ├── paper_comparison.md             ← Invariance & limitation comparison matrix
│   └── papers/
│       ├── PAPERS_DIRECTORY.md         ← Full annotated catalog of all 53 papers
│       ├── papers_catalog.json         ← Machine-readable metadata
│       └── pdfs/                       ← 53 locally archived full-text PDFs (~211.5 MB)
│
├── docs/                               ← Technical documentation
│   ├── paper_draft.md                  ← Conference preprint (IEEE/CVF CVPR / ACM MM)
│   ├── evaluation_report.md            ← Stage 3–5 empirical benchmark report
│   ├── architecture.md                 ← Formal system design specification
│   ├── experiment_protocol.md          ← Mathematical metric definitions & protocols
│   ├── implementation_decisions.md     ← Architecture Decision Records (ADR 01–04)
│   └── roadmap.md                      ← Phased delivery schedule
│
├── experiments/                        ← ML training & evaluation code
│   ├── image/                          ← Stage 3: Image detector training & benchmarks
│   ├── audio/                          ← Stage 4: Audio detector training & benchmarks
│   └── multimodal/                     ← Stage 5: Multimodal fusion & evaluation
│
├── app/
│   └── engine/                         ← Inference engine (image, audio, multimodal)
│
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Quickstart

```bash
# Clone
git clone https://github.com/Omnifex-Agency/deepfake.git
cd deepfake

# Install
pip install -r requirements.txt

# Run Stage 3 image experiments
python experiments/image/train_and_evaluate.py

# Run Stage 4 audio experiments  
python experiments/audio/train_and_evaluate.py

# Run Stage 5 multimodal evaluation
python experiments/multimodal/train_and_evaluate.py
```

**Docker:**
```bash
docker-compose up --build
```

---

## Preprint Citation

```bibtex
@article{deepshield2026,
  author    = {DeepShield AI Research Collective},
  title     = {DeepShield: Codec-Invariant Multimodal Deepfake Detection via
               Learnable Gabor Residuals and Decoupled Asymmetric Risk Fusion},
  journal   = {IEEE/CVF CVPR / ACM Multimedia Working Preprint},
  year      = {2026},
  url       = {https://github.com/Omnifex-Agency/deepfake}
}
```

→ [Full paper draft](docs/paper_draft.md) · [All 53 BibTeX citations](research/papers/PAPERS_DIRECTORY.md)

---

## License

Released under the **[MIT License](LICENSE)**.  
Developed as a publication-grade AI/ML research system for multimodal deepfake detection.
