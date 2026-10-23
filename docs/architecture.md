# DeepShield AI — System Architecture Specification

> **Engineering & System Architecture Design Document**  
> **Prepared by:** AI Software Architect, MLOps Engineer, Multimodal Specialist  
> **Date:** October 2026

---

## 1. System Vision & Architectural Philosophy

**DeepShield AI** is an enterprise-grade multimodal media forensics platform designed to detect synthetic, manipulated, and deepfake content across image, audio, and video modalities.

### Core Architectural Principles:
1. **Decoupled Modality Pipelines:** The image, audio, and video pipelines operate as isolated, independently testable micro-services with standardized interfaces.
2. **Asymmetric Multimodal Fallback:** The system must gracefully handle missing, corrupt, or single-stream media (e.g., still image, silent video, audio-only podcast) without throwing runtime exceptions or degrading into undefined behavior.
3. **Calibrated Probabilistic Output:** The system never issues binary absolute claims (e.g., "100% Genuine"). All predictions output calibrated probabilities $P \in [0.0, 1.0]$, Expected Calibration Error (ECE) bounds, and a three-tier decision status:
   - `Authentic / Bonafide` ($P(\text{Fake}) < 0.35$)
   - `Uncertain / Needs Human Review` ($0.35 \le P(\text{Fake}) \le 0.65$)
   - `Synthetic / Manipulated` ($P(\text{Fake}) > 0.65$)
4. **Verifiable Explainability:** High-stakes forensic decisions are accompanied by spatial heatmaps (Grad-CAM), high-frequency residual spectra (DCT/FFT), and temporal synchronization dissonance plots.

---

## 2. End-to-End System Diagram

```
                                  USER INTERFACE (Browser)
                   ┌─────────────────────────────────────────────────────┐
                   │  Drag-and-Drop Upload (Image / Audio / Video)       │
                   │  Real-Time Progress & Modality Inspection           │
                   │  Forensic Report Card & Explainability Visualizer   │
                   └──────────────────────────┬──────────────────────────┘
                                              │ HTTP / Multipart Form
                                              ▼
                                   API GATEWAY (FastAPI)
                   ┌─────────────────────────────────────────────────────┐
                   │  • Strict MIME & Magic Byte Validation              │
                   │  • Rate Limiting & Upload Size Enforcement (≤100MB) │
                   │  • Job Dispatcher & Modality Router                 │
                   └──────┬───────────────────┬───────────────────┬──────┘
                          │ Image             │ Audio             │ Video
                          ▼                   ▼                   ▼
                  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                  │ Image Pre-   │    │ Audio Pre-   │    │ Video De-    │
                  │ processing   │    │ processing   │    │ multiplexer  │
                  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
                         │                   │                   │
                         │                   │            ┌──────┴──────┐
                         │                   │            │ Split Video │
                         │                   │            │ and Audio   │
                         │                   │            └──────┬──────┘
                         │                   │                   │
                         ▼                   ▼                   ▼
                  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                  │ Face Crop &  │    │ 16kHz Resample│   │ Face Tracking│
                  │ Align (224)  │    │ & VAD Filter │    │ & Lip Align  │
                  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
                         │                   │                   │
                         ▼                   ▼                   ▼
                   IMAGE FORENSICS     AUDIO FORENSICS     AV SYNC ENGINE
                  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
                  │ • CLIP ViT   │    │ • Whisper-   │    │ • Cross-Modal│
                  │ • Gabor Freq │    │   SpecRNet   │    │   Dissonance │
                  │ • Efficient- │    │ • AASIST-    │    │ • LipForensic│
                  │   Net-B0     │    │   GNN Head   │    │   Temporal   │
                  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
                         │ f_v, s_v          │ f_a, s_a          │ d_av
                         └─────────────┬─────┴───────────────────┘
                                       ▼
                       DECOUPLED ASYMMETRIC FUSION ENGINE
                   ┌─────────────────────────────────────────┐
                   │  • Unimodal Fallback Check              │
                   │  • Asymmetric Risk Penalty Gate         │
                   │  • Temperature Scaling & Calibration    │
                   └───────────────────┬─────────────────────┘
                                       │
                                       ▼
                             FORENSIC REPORT GENERATOR
                   ┌─────────────────────────────────────────┐
                   │  • Calibrated Risk Score [0.0 - 1.0]    │
                   │  • Spatial Grad-CAM Overlay             │
                   │  • Spectral High-Frequency Heatmap      │
                   │  • Model Version & Provenance Metadata  │
                   └─────────────────────────────────────────┘
```

---

## 3. Component Deep Dive

### 3.1 Ingestion & Preprocessing Pipeline
- **Image Pipeline:**
  - Standardized image loader utilizing OpenCV and Pillow.
  - Facial landmark detection and bounding box cropping with a 1.3x margin to capture forehead, ear, and jawline blending boundaries.
  - Resolution standardization to $224 \times 224 \times 3$ with bicubic interpolation.
- **Audio Pipeline:**
  - Audio extraction via `ffmpeg-python` from video containers, converted to 16 kHz mono 16-bit PCM WAV.
  - Voice Activity Detection (VAD) via `webrtcvad` to remove silent lead-in/lead-out periods.
  - Normalization: Peak amplitude normalization to $-1.0 \text{ dBFS}$.
- **Video Multimodal Alignment:**
  - Decouples video container into video frame sequence (sampled at 25 fps) and audio stream.
  - Face tracking to ensure identity consistency across temporal windows (16 frames per window).
  - Audio segmented into matching 640 ms audio chunks (16 frames $\times$ 40 ms per frame).

### 3.2 Model Inference Engines
1. **Phase 1 Image Engine:**
   - Primary: Dual-stream model combining frozen CLIP ViT-L/14 semantic features and a learnable Gabor frequency residual branch.
   - Fallback/Fast-Path: EfficientNet-B0 running on CPU/Edge in $<5\text{ ms}$.
2. **Phase 2 Audio Engine:**
   - Primary: Whisper-Base encoder extracting 80-band log-mel representations feeding a compact SpecRNet classification head.
   - Complementary: AASIST processing raw waveforms to detect phase-based synthesis artifacts.
3. **Phase 3 Multimodal Fusion Engine:**
   - Computes independent calibrated risk scores $s_v, s_a \in [0, 1]$.
   - Computes cross-modal representation distance $d_{av} = \|f_v - f_a\|_2$.
   - Fuses scores through a gating network with dynamic modality dropout:
     $$\hat{y} = \max\left(s_v, s_a, \sigma(W [f_v \odot f_a; |f_v - f_a|] + b)\right)$$

### 3.3 Explainability Module
- **Spatial Explainability:** Layer-CAM / Grad-CAM computed over the final convolutional or attention layer, overlaid as a transparent colormap indicating manipulated facial features (eyes, lips, blending seams).
- **Frequency Explainability:** 2D Discrete Fourier Transform (FFT) magnitude spectrum highlighting unnatural checkerboard artifacts or synthetic high-frequency anomalies.
- **Audio Spectral Decomposition:** Mel-spectrogram difference map comparing the input waveform against expected natural speech harmonics.

---

## 4. Technology Stack Justification

| Layer | Selected Technology | Technical Rationale & Alternatives Rejected |
| :--- | :--- | :--- |
| **Backend API** | **FastAPI (Python 3.10+)** | High-throughput asynchronous async/await support; native Pydantic data validation; automatic OpenAPI documentation. Rejects Flask (lacks async streaming) and Django (unnecessary ORM bloat for an ML inference service). |
| **ML Framework** | **PyTorch 2.x & Torchvision** | De facto industry and research standard; native mixed precision (AMP); broad support for pretrained models in `timm` and Hugging Face. |
| **Audio Processing** | **Torchaudio & SoundFile** | Native GPU tensor operations for audio spectrograms and filterbanks; seamless integration with Whisper and AASIST backbones. |
| **Frontend UI** | **Vanilla HTML5/CSS/JavaScript + Tailwind/Vite (or Gradio for rapid POC)** | Ultra-clean, modern, responsive interface with direct binary blob handling for fast heatmap rendering. |
| **Packaging & MLOps** | **Docker & MLflow** | Containerized CPU/CUDA deployment with pinned CUDA 12.x runtimes; reproducible experiment tracking and model registry. |
