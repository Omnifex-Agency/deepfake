# DeepShield AI — Research Gaps, Testable Hypotheses & Contribution Plan

> **Stage 1 Research Deliverable**  
> **Prepared by:** Senior AI/ML Research Scientist, Multimodal Deep Learning Specialist  
> **Methodological Framework:** Structured in accordance with the `hypothesis-generation` and `ai-ml-research-assistant` skills.  
> **Evaluation Date:** October 2026

---

## 1. Overview of Identified Gaps in Current Literature

A rigorous synthesis of the literature (2019–2026) reveals five persistent, systemic failures across deepfake detection systems:

1. **Gap 1: The Cross-Generator Frequency Fragility Gap.**
   Classifiers trained on GANs overfit to periodic grid upsampling artifacts and fail catastrophically on diffusion models (DDPM, LDM, DiT), while diffusion-specific detectors (DIRE) require computationally prohibitive iterative reverse sampling.
2. **Gap 2: The Codec-Induced Audio Anti-Spoofing Collapse.**
   State-of-the-art audio anti-spoofing models (AASIST, RawNet2) achieve <1% EER on clean studio benchmarks (ASVspoof 2019 LA), but their error rate explodes to >15%–30% when subjected to lossy mobile compression (Opus, AAC, MP3) in real-world scenarios.
3. **Gap 3: The Multimodal "Modality Dominance" & Single-Stream Blindness Trap.**
   Standard multimodal networks trained with joint loss functions allow high-dimensional visual embeddings to suppress audio gradients. Consequently, when an attacker introduces a forged voice over authentic video, or when video quality is degraded, the system fails to detect the anomaly.
4. **Gap 4: Severe Probability Overconfidence & Miscalibration.**
   Standard deepfake classifiers trained with cross-entropy loss produce extreme, uncalibrated probabilities ($p > 0.999$) on out-of-distribution real media, leading to unacceptably high false accusation rates in production environments.
5. **Gap 5: The Static Evaluation vs. Continuous Drift Dilemma.**
   New generative tools (e.g., ElevenLabs v3, Flux.1, Sora) alter artifact distributions every few months. Current systems lack a safe, leakage-free continuous improvement loop with human-in-the-loop audit gates.

---

## 2. Formal Hypotheses & Experimental Designs

### Contribution Area 1 (Rank 1): Dual-Domain Spatial-Frequency Invariant Feature Distillation for Cross-Generator Robustness

- **1. Existing Limitation:**
  Classifiers trained exclusively in the spatial domain (e.g., Xception, EfficientNet) overfit to specific facial textures, while classifiers trained purely in the frequency domain (DCT/FFT) are obliterated by standard JPEG recompression. Current models lack an explicit mechanism that decouples generator-specific high-frequency noise from content-agnostic boundary residuals.
- **2. Supporting Literature:**
  - Frank et al. (ICML 2020), *Leveraging Frequency Analysis for Deep Fake Image Recognition*.
  - Wang et al. (CVPR 2020), *CNN-generated images are surprisingly easy to spot... for now*.
  - Tan et al. (CVPR 2024), *Rethinking the Up-Sampling Operations in CNN-based Generative Network*.
  - Yan et al. (NeurIPS 2023), *DeepfakeBench Benchmark*.
- **3. Prior Work Addressing This:**
  SPSL (CVPR 2021) and F3Net (ECCV 2020) combined spatial and frequency streams, but used static frequency band partitions that degrade under varying JPEG quality factors ($Q \in [50, 90]$).
- **4. Testable Hypothesis ($H_1$):**
  *Extracting frequency-filtered high-pass residuals using adaptive, learnable band-pass filtering concatenated with frozen foundation vision features (CLIP ViT) will improve cross-generator generalization on unseen diffusion models by at least 10% ROC-AUC over a spatial-only baseline, while maintaining $<3\%$ performance drop under JPEG compression ($Q=70$).*
- **5. Experimental Design:**
  - *Control Baseline:* Frozen CLIP ViT-L/14 linear probe (Ojha et al.) and standard EfficientNet-B0 trained on ProGAN.
  - *Intervention ($H_1$):* Dual-stream architecture: Branch A receives RGB input processed by a 2D Learnable Gabor Filterbank (LG-Net); Branch B extracts frozen CLIP ViT-L/14 patch embeddings. Features are merged via gated cross-attention before classification.
  - *Training Set:* ProGAN face subset (50k images).
  - *Evaluation Benchmark:* Unseen generators in GenImage (Stable Diffusion v1.5, Midjourney v4) and Celeb-DF v2.
  - *Robustness Perturbations:* JPEG compression ($Q \in \{90, 80, 70, 60\}$) and Gaussian blur ($\sigma \in \{1, 2, 3\}$).
- **6. Disproving Evidence (Falsification Criteria):**
  Hypothesis $H_1$ is disproved if the dual-stream model:
  1. Achieves a cross-generator ROC-AUC on unseen Stable Diffusion that is within $\pm 2\%$ of the vanilla CLIP baseline, OR
  2. Exhibits an AUC drop exceeding 8% when JPEG compression ($Q=70$) is applied.

---

### Contribution Area 2 (Rank 2): Codec-Augmented Acoustic Feature Adaptation for In-The-Wild Audio Forensics

- **1. Existing Limitation:**
  End-to-end raw waveform anti-spoofing models (AASIST) learn exact phase and temporal correlation patterns that exist only in pristine, uncompressed 16 kHz WAV/FLAC files. When applied to real-world voice clips transmitted via WhatsApp, Telegram, or YouTube (which re-encode audio using Opus at 16–32 kbps or AAC at 64 kbps), the learned graph structure breaks down, causing EER to surge from $<1\%$ to $>20\%$.
- **2. Supporting Literature:**
  - Jung et al. (Interspeech 2022), *AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks*.
  - Müller et al. (Interspeech 2022), *Does Audio Deepfake Detection Generalize? An In-The-Wild Investigation*.
  - Kawa et al. (Interspeech 2023), *Improved DeepFake Detection Using Whisper Features*.
- **3. Prior Work Addressing This:**
  ASVspoof 2021 DF introduced compression benchmarks, and RawBoost (Tak et al., 2022) proposed linear/non-linear data augmentation, but did not address the semantic speech invariant properties captured by large speech foundation models.
- **4. Testable Hypothesis ($H_2$):**
  *Conditioning a lightweight spectro-temporal classifier on frozen speech foundation representations (Whisper-Base encoder) combined with on-the-fly random lossy codec augmentation (Opus 16-32k, AAC 32-64k, MP3 64k) during training will reduce the Equal Error Rate (EER) on unconstrained real-world audio (In-The-Wild dataset) by at least 35% relative to a vanilla AASIST baseline.*
- **5. Experimental Design:**
  - *Control Baseline:* Standard AASIST trained on ASVspoof 2019 LA.
  - *Intervention ($H_2$):* Whisper-Base encoder extracts 80-channel log-mel features processed through a lightweight SpecRNet back-end. A dynamic audio data loader applies random on-the-fly Torchaudio codec recompression (Opus, AAC, MP3, Vorbis) and additive acoustic room impulse responses.
  - *Training Set:* ASVspoof 2019 LA training partition (25k utterances).
  - *Evaluation Benchmark:* In-The-Wild Audio Deepfake Dataset (31.6 hours) and ASVspoof 2021 DF compressed evaluation set.
- **6. Disproving Evidence (Falsification Criteria):**
  Hypothesis $H_2$ is disproved if the relative EER reduction on the In-The-Wild dataset is less than 15% compared to the baseline, or if clean ASVspoof 2019 LA evaluation EER degrades by more than 3.0 percentage points.

---

### Contribution Area 3 (Rank 3): Asymmetric Cross-Modal Decoupled Fusion with Unimodal Fallback Resilience

- **1. Existing Limitation:**
  Standard multimodal deepfake systems concatenate audio and visual feature vectors into a joint classifier. When trained on datasets with uneven manipulation rates, the classifier exhibits "modality collapse" (overfitting to whichever modality has easier-to-detect artifacts, typically video) and fails when an adversary injects an audio-only deepfake over real video (RF) or when video quality is degraded.
- **2. Supporting Literature:**
  - Khalid et al. (NeurIPS 2021), *FakeAVCeleb: A Novel Audio-Video Multimodal Deepfake Dataset*.
  - Feng et al. (CVPR 2023), *Self-Supervised Video Forensics by Audio-Visual Anomaly Detection*.
  - Oorloff et al. (CVPR 2024), *AVFF: Audio-Visual Feature Fusion for Video Deepfake Detection*.
- **3. Prior Work Addressing This:**
  Multimodal contrastive learning (AVOiD-DF) and complementary masking (AVFF) attempt joint learning, but suffer complete failure when one modality is missing (e.g., audio track absent).
- **4. Testable Hypothesis ($H_3$):**
  *A decoupled decision-level fusion architecture that computes unimodal calibrated risk scores $s_v, s_a \in [0, 1]$ combined with a cross-modal temporal dissonance penalty $d_{av} = \|f_v - f_a\|_2$ will outperform joint concatenation on the Real-Video/Fake-Audio (RF) category of FakeAVCeleb by at least 12% balanced accuracy, while preserving graceful standalone operation when $s_v$ or $s_a$ is unavailable.*
- **5. Experimental Design:**
  - *Control Baseline:* End-to-end concatenated feature fusion (VGG-Face + ResNetSE as implemented in FakeAVCeleb paper).
  - *Intervention ($H_3$):* The visual stream outputs calibrated confidence $P(\text{Fake}_v)$ and visual embedding $f_v$; the audio stream outputs $P(\text{Fake}_a)$ and audio embedding $f_a$. A lightweight fusion gate computes:
    $$\hat{y} = \max\left(P(\text{Fake}_v), P(\text{Fake}_a), \sigma(W [f_v \odot f_a; |f_v - f_a|] + b)\right)$$
    with explicit drop-modality regularization ($p=0.2$ during training).
  - *Evaluation Benchmark:* FakeAVCeleb test split evaluated independently across all 4 quadrants: RR, FR, RF, FF.
- **6. Disproving Evidence (Falsification Criteria):**
  Hypothesis $H_3$ is disproved if balanced accuracy on the RF quadrant does not improve by at least 8% over the joint concatenation baseline, or if unimodal performance degrades when the other stream is artificially masked with zeros.

---

### Contribution Area 4 (Rank 4): Post-Hoc Confidence Calibration for Low False-Alarm Deployment

- **1. Existing Limitation:**
  Most deepfake detection papers report only ROC-AUC or binary accuracy at a fixed 0.5 threshold. However, under realistic deployment where 99% of uploaded media is genuine, uncalibrated neural networks exhibit high Expected Calibration Error (ECE > 15%), producing extreme confidence on false positives and destroying user trust.
- **2. Supporting Literature:**
  - Guo et al. (ICML 2017), *On Calibration of Modern Neural Networks*.
  - Yan et al. (NeurIPS 2023), *DeepfakeBench* (documents calibration degradation across 15 detectors).
- **3. Testable Hypothesis ($H_4$):**
  *Applying Temperature Scaling and Isotonic Regression calibrated on a held-out validation set will reduce Expected Calibration Error (ECE) below 4% on out-of-distribution test sets while reducing the False Positive Rate at 95% Recall (FPR95) by at least 25% without retraining model backbones.*
- **4. Experimental Design:**
  - Evaluate uncalibrated vs. Temperature Scaled vs. Isotonic Calibrated logits on FF++ c23 and Celeb-DF v2. Measure ECE, Brier score, and FPR95 across reliability diagrams with 15 bins.
- **5. Disproving Evidence (Falsification Criteria):**
  Disproved if ECE on out-of-distribution Celeb-DF remains $>8\%$ after temperature scaling.

---

## 3. Prioritized Research Contribution Ranking Matrix

| Rank | Research Contribution Area | Novelty Potential | Feasibility on Host (GTX 1650) | Scientific / Research Value | Implementation Complexity | Primary Target Venue / Output |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | **Adaptive Spatial-Frequency Gated Fusion for Cross-Generator Generalization** | **High** | **High** (frozen CLIP + lightweight Gabor branch fits in 2.5 GB VRAM) | **Very High** (addresses the critical GAN-to-Diffusion generalization bottleneck) | Moderate (PyTorch custom filterbank + cross-attention) | Conference paper candidate (WACV / CVPR Workshop / IEEE TIFS) |
| **2** | **Codec-Augmented Foundation Speech Representation for Real-World Audio Forensics** | **Medium-High** | **Very High** (frozen Whisper-Base + SpecRNet uses <2 GB VRAM) | **High** (solves real-world social media codec brittleness) | Low-Moderate (Torchaudio codec pipelines + SpecRNet) | Audio research candidate (Interspeech / ICASSP) |
| **3** | **Decoupled Asymmetric Multimodal Fusion with Unimodal Fallback Resilience** | **High** | **High** (trains lightweight fusion gate on extracted embeddings) | **Very High** (solves modality dominance and missing-modality failures) | Moderate (FakeAVCeleb multi-task evaluation harness) | Multimodal forensics contribution (ACM Multimedia / IEEE TIFS) |
| **4** | **Post-Hoc Temperature Calibration & Risk-Bounded Uncertainty Bounds** | **Moderate** | **Extreme** (CPU / lightweight post-processing in seconds) | **High** (vital for real-world deployment credibility and portfolio quality) | Low (Scikit-Learn isotonic regression & calibration plots) | Core MLOps engineering contribution |
| **5** | **Closed-Loop Active Learning & Continual Adaptation with Drift Guardrails** | **Moderate** | **Moderate** (requires caching and selective retraining) | **Moderate-High** (addresses real-world temporal generator drift) | High (pipeline infrastructure and human review gate) | Systems / MLOps engineering contribution |

---

## 4. Next Step Recommendation

Following our strict execution rules:
We recommend focusing **Stage 3 (Image POC)** directly on validating **Contribution Area 1** (Adaptive Spatial-Frequency Gated Fusion), comparing it rigorously against **EfficientNet-B0**, **XceptionNet**, and **UniversalFakeDetect (CLIP)** on FaceForensics++ and Celeb-DF v2.
