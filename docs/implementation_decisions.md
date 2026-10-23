# DeepShield AI — Architectural & Implementation Decision Records (ADR)

> **Architectural Decision Records (ADRs)**  
> **Prepared by:** AI Software Architect, Senior AI/ML Research Scientist  
> **Date:** October 2026

---

## ADR 01: Python Runtime & Environment Strategy
- **Context:** The host machine possesses an MSYS2 Python 3.12 without PyTorch, and a system Python 3.10.11 at `C:\Users\rohan\AppData\Local\Programs\Python\Python310\python.exe` containing PyTorch 2.9.1, Torchvision, Scikit-Learn, OpenCV, Matplotlib, SciPy, FastAPI, and Gradio.
- **Decision:** Utilize Python 3.10.11 for all DeepShield AI experiments.
- **Rationale:** Ensures immediate compatibility with established computer vision libraries, avoiding compilation or compatibility issues common with brand-new Python 3.12 sub-releases.

---

## ADR 02: Hardware Realism (GTX 1650 4 GB VRAM)
- **Context:** The user's GPU has 4 GB dedicated VRAM. Training massive 300M+ parameter Vision Transformers or multi-modal LLMs locally triggers Out-Of-Memory (OOM) crashes.
- **Decision:**
  1. For foundation models (CLIP ViT-L/14, Whisper-Base), freeze the encoder weights and compute embeddings in small batches (batch size 8–16). Train only lightweight classification probes/heads.
  2. For end-to-end training, prioritize compact, highly efficient backbones (EfficientNet-B0, ConvNeXt-Tiny, AASIST, RawNet2) with FP16 automatic mixed precision.
  3. Support seamless cloud export to Google Colab / Kaggle GPU environments for any large-scale experiments.

---

## ADR 03: Decoupled Multimodal Architecture Over Naive Concatenation
- **Context:** Classical multimodal deepfake detectors concatenate audio and visual feature vectors before a shared classifier. This results in visual dominance and catastrophic failure on audio-only voice clones (Real Video + Fake Audio).
- **Decision:** Implement an asymmetric decoupled decision architecture where independent visual and audio risk scores are computed and combined with a cross-modal representation distance metric ($\|f_v - f_a\|_2$).
- **Rationale:** Guarantees graceful single-modality fallback (e.g., still images or silent videos) while maintaining high sensitivity to subtle lip-sync and voice-face discrepancies.

---

## ADR 04: Mandatory Probability Calibration (ECE ≤ 5%)
- **Context:** Deep neural networks trained on binary cross-entropy output overconfident probabilities ($p > 0.999$) that produce unacceptable false alarm rates in production settings.
- **Decision:** Enforce post-hoc Temperature Scaling and Isotonic Regression calibrated exclusively on holdout validation data.
- **Rationale:** Ensures that a predicted probability of 80% corresponds to an empirical 80% likelihood of forgery, providing legally defensible, trustworthy outputs.
