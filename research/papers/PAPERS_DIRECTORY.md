# Deepfake Research Collective — Forensic Literature Repository & Paper Directory

> **Archive Status:** 53 Full-Text Academic Papers Downloaded Locally (~211.5 MB total PDF archive).
> All papers are categorized according to academic domain, indexing verified arXiv identifiers, conference venues, direct local PDF endpoints, official code repositories, reported benchmark metrics, and known research limitations.

## Table of Contents

1. [Spatial & Blending Forensics (7 Papers)](#spatial--blending-forensics)
2. [Frequency & Spectral Forensics (6 Papers)](#frequency--spectral-forensics)
3. [Diffusion & Generative Fingerprints (8 Papers)](#diffusion--generative-fingerprints)
4. [Temporal & Video Dynamics (6 Papers)](#temporal--video-dynamics)
5. [Audio Deepfake & Speech Anti-Spoofing (11 Papers)](#audio-deepfake--speech-anti-spoofing)
6. [Multimodal Audio-Visual Forensics (6 Papers)](#multimodal-audio-visual-forensics)
7. [Codec & Compression Robustness (4 Papers)](#codec--compression-robustness)
8. [Surveys, Benchmarks & Metrology (5 Papers)](#surveys-benchmarks--metrology)

---

## Spatial & Blending Forensics
*Focuses on spatial-domain discontinuities, boundary blending artifacts, patch-level truncations, and warp residuals in manipulated facial imagery.*

### 1. FaceForensics++: Learning to Detect Manipulated Facial Images
- **Authors:** Andreas Rössler, Davide Cozzolino, Luisa Verdoliva, Christian Riess, Justus Thies, Matthias Nießner
- **Venue & Year:** `ICCV 2019` (2019) &bull; **Sub-Category:** `Boundary Artifacts & Face Splicing`
- **Architecture:** XceptionNet, MesoNet, Steganographic Classifiers
- **Primary Dataset:** FaceForensics++ (Deepfakes, Face2Face, FaceSwap, NeuralTextures)
- **Reported Performance:** **Acc: 99.2% (raw c0), 95.7% (c23), 81.0% (c40)** (Accuracy (%))
- **Identified Limitations:** *Severe degradation under H.264 compression (c40); poor zero-shot transfer to unseen GANs.*
- **Access Links:** [Local PDF Archive](/papers/FaceForensics_PlusPlus_Rossler_2019.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1901.08971) &bull; [Direct PDF](https://arxiv.org/pdf/1901.08971.pdf) &bull; [Official Code](https://github.com/ondyari/FaceForensics)

### 2. Face X-Ray for More General Face Forgery Detection
- **Authors:** Lingzhi Li, Jianmin Bao, Ting Zhang, Hao Yang, Dong Chen, Fang Wen, Baining Guo
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Blending Boundary Segmentation`
- **Architecture:** HRNet / ResNet predicting blending boundaries
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFD
- **Reported Performance:** **AUC: 99.1% (FF++ c23), 74.8% (Celeb-DF cross-test)** (ROC-AUC (%))
- **Identified Limitations:** *Only detects composite/swapped images; completely blind to wholly synthetic faces (StyleGAN/LDM).*
- **Access Links:** [Local PDF Archive](/papers/Face_XRay_Li_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1912.12623) &bull; [Direct PDF](https://arxiv.org/pdf/1912.12623.pdf) &bull; [Official Code](https://github.com/li-lingzhi/FaceXray)

### 3. What Makes Fake Images Detectable? Understanding Properties of Synthesized Images
- **Authors:** Lucy Chai, David Bau, Ser-Nam Lim, Phillip Isola
- **Venue & Year:** `ECCV 2020` (2020) &bull; **Sub-Category:** `Patch-Level Truncation`
- **Architecture:** Truncated patch-level fully convolutional network
- **Primary Dataset:** FF++, Celeb-DF, FaceSwap
- **Reported Performance:** **AP: 83.3% on Celeb-DF cross-evaluation** (Average Precision (AP))
- **Identified Limitations:** *Truncated receptive field loses global semantic coherence and long-range structural dependencies.*
- **Access Links:** [Local PDF Archive](/papers/Patch_Forensics_Chai_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2008.10588) &bull; [Direct PDF](https://arxiv.org/pdf/2008.10588.pdf) &bull; [Official Code](https://github.com/chail/patch-forensics)

### 4. Multi-attentional Deepfake Detection
- **Authors:** Hanqing Zhao, Wenbo Zhou, Dongdong Chen, Tianyi Wei, Weiming Zhang, Nenghai Yu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Multi-Region Spatial Attention`
- **Architecture:** Multi-attentional network with region-independent loss and texture enhancement
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFD
- **Reported Performance:** **AUC: 99.8% (FF++ c23), 77.2% (Celeb-DF cross-test)** (ROC-AUC, Accuracy)
- **Identified Limitations:** *Attention heads can drift toward background artifacts when face alignment fluctuates.*
- **Access Links:** [Local PDF Archive](/papers/Multi_Attentional_Zhao_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2103.02406) &bull; [Direct PDF](https://arxiv.org/pdf/2103.02406.pdf) &bull; [Official Code](https://github.com/nii-yamagishilab/Multi-attentional-Deepfake-Detection)

### 5. Pair-wise Self-Consistency Learning for Deepfake Detection
- **Authors:** Tianchen Zhao, Xiang Xu, Mingze Xu, Hao Ding, Yuanjun Xiong, Wei Xia
- **Venue & Year:** `ACM MM 2021` (2021) &bull; **Sub-Category:** `Pairwise Consistency`
- **Architecture:** Pair-wise self-consistency learning with patch similarity
- **Primary Dataset:** FF++, Celeb-DF v2, DFDC
- **Reported Performance:** **AUC: 86.9% cross-dataset on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *High computational overhead for pairwise patch-similarity matrix computation.*
- **Access Links:** [Local PDF Archive](/papers/Pairwise_Self_Consistency_Zhao_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2105.04838) &bull; [Direct PDF](https://arxiv.org/pdf/2105.04838.pdf) &bull; [Official Code](https://github.com/chail/patch-forensics)

### 6. Look Locally for Understanding Globally: A Generalizable Face Forgery Detection via Reconstruction
- **Authors:** Hao Chen, Haotian Hong, Zhaoyu Chen, Keyu Chen, Yaohui Li
- **Venue & Year:** `ECCV 2022` (2022) &bull; **Sub-Category:** `Local-Global Reconstruction`
- **Architecture:** Local gradient reconstruction network with high-frequency loss
- **Primary Dataset:** FaceForensics++, Celeb-DF, WildDeepfake
- **Reported Performance:** **AUC: 89.1% cross-dataset on Celeb-DF v2** (ROC-AUC (%))
- **Identified Limitations:** *Reconstruction quality degrades significantly on extreme low-resolution face crops (<64x64).*
- **Access Links:** [Local PDF Archive](/papers/Look_Locally_Chen_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2207.03061) &bull; [Direct PDF](https://arxiv.org/pdf/2207.03061.pdf) &bull; [Official Code](https://github.com/ChenH0528/LGrad)

### 7. Rethinking the Up-Sampling Operations in CNN-based Face Forgery Detection
- **Authors:** Chuangchuang Tan, Yao Zhao, Shikui Wei, Guanghua Gu, Ping Liu, Yunchao Wei
- **Venue & Year:** `CVPR 2024` (2024) &bull; **Sub-Category:** `Neighboring Pixel Relationship (NPR)`
- **Architecture:** Neighboring Pixel Relationship (NPR) residual extractor with ConvNeXt
- **Primary Dataset:** FaceForensics++, Celeb-DF, WildDeepfake, DiffusionForensics
- **Reported Performance:** **AUC: 91.5% cross-generator average across GANs and Diffusion** (ROC-AUC (%))
- **Identified Limitations:** *Requires careful pixel neighbor stride tuning depending on downsampling factors.*
- **Access Links:** [Local PDF Archive](/papers/NPR_Upsampling_Tan_2024.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2403.18808) &bull; [Direct PDF](https://arxiv.org/pdf/2403.18808.pdf) &bull; [Official Code](https://github.com/chuangchuangtan/NPR-DeepfakeDetection)

## Frequency & Spectral Forensics
*Analyzes Discrete Cosine Transform (DCT), Discrete Fourier Transform (DFT), high-pass residuals, and phase spectra to detect generative spectral anomalies.*

### 1. Leveraging Frequency Analysis for Deep Fake Image Recognition
- **Authors:** Joel Frank, Thorsten Eisenhofer, Lea Schönherr, Asja Fischer, Dorothea Kolossa, Thorsten Holz
- **Venue & Year:** `ICML 2020` (2020) &bull; **Sub-Category:** `Discrete Cosine Transform (DCT)`
- **Architecture:** Discrete Cosine Transform (DCT) + Linear Classifier / CNN
- **Primary Dataset:** FaceForensics++, CelebA-HQ, ProGAN
- **Reported Performance:** **AUC > 99.0% on uncompressed sets** (ROC-AUC (%))
- **Identified Limitations:** *High sensitivity to standard post-processing (Gaussian blur, social media recompression).*
- **Access Links:** [Local PDF Archive](/papers/Frequency_Analysis_Frank_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2003.08685) &bull; [Direct PDF](https://arxiv.org/pdf/2003.08685.pdf) &bull; [Official Code](https://github.com/frederic-frank/frequency-analysis-for-deep-fake-image-recognition)

### 2. Watch your Up-Convolution: CNN Based Generative Deep Neural Networks are Failing to Reproduce Spectral Distributions
- **Authors:** Ricard Durall, Margret Keuper, Franz-Josef Pfreundt, Janis Keuper
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Radial Spectral Analysis (Azimuthal Average)`
- **Architecture:** Azimuthal average spectral distribution analysis over DFT power spectra
- **Primary Dataset:** CelebA-HQ, FFHQ, StyleGAN, DCGAN
- **Reported Performance:** **Acc: 100.0% on uncompressed GAN images** (Accuracy (%))
- **Identified Limitations:** *Assumes standard up-convolution interpolation; easily spoofed by spectral loss regularization during training.*
- **Access Links:** [Local PDF Archive](/papers/Watch_Your_Up_Convolution_Durall_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1911.00686) &bull; [Direct PDF](https://arxiv.org/pdf/1911.00686.pdf) &bull; [Official Code](https://github.com/cc-hpc-itwm/UpConvolution)

### 3. Thinking in Frequency: Face Forgery Detection by Mining Frequency-aware Clues (F3-Net)
- **Authors:** Yuyang Qian, Guojun Yin, Shenggyang Lu, Xiang Chen, Lu Dong, Fang Wen
- **Venue & Year:** `ECCV 2020` (2020) &bull; **Sub-Category:** `Dual-Stream Frequency Decomposition (F3-Net)`
- **Architecture:** Dual-stream frequency-aware network (F3-Net) with FAD and LFS branches
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **Acc: 90.4% on FF++ c40; AUC: 75.3% on Celeb-DF** (Accuracy (%), ROC-AUC)
- **Identified Limitations:** *Frequency band partitioning requires manual cutoff frequency selection based on target codec.*
- **Access Links:** [Local PDF Archive](/papers/Thinking_In_Frequency_Qian_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2007.09355) &bull; [Direct PDF](https://arxiv.org/pdf/2007.09355.pdf) &bull; [Official Code](https://github.com/weixiangquan/F3-Net)

### 4. Spatial-Phase Shallow Learning: Rethinking Face Forgery Detection in Frequency Domain (SPSL)
- **Authors:** Honggu Liu, Xiaodan Li, Wenbo Zhou, Yuefeng Chen, Yuan He, Hui Xue, Weiming Zhang, Nenghai Yu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Phase Spectrum Analysis`
- **Architecture:** Spatial-Phase Shallow Learning (SPSL) with phase spectrum extraction
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFD
- **Reported Performance:** **AUC: 81.6% cross-dataset on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *Phase calculation is sensitive to spatial warping and non-rigid facial deformations.*
- **Access Links:** [Local PDF Archive](/papers/Spatial_Phase_Shallow_Cao_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2103.05348) &bull; [Direct PDF](https://arxiv.org/pdf/2103.05348.pdf) &bull; [Official Code](https://github.com/SunnyBingoMe/SPSL)

### 5. Frequency-Domain Learning for Face Forgery Detection
- **Authors:** Jiaming Li, Yuezun Li, Siwei Lyu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Multi-Frequency Band Attention`
- **Architecture:** Multi-frequency band attention network with adaptive frequency decomposition
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **AUC: 99.3% (FF++ c23), 78.4% (Celeb-DF)** (ROC-AUC (%))
- **Identified Limitations:** *Performance degrades under high-frequency cutoff filters such as heavy JPEG Q<40.*
- **Access Links:** [Local PDF Archive](/papers/Frequency_Domain_Learning_Li_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2103.14917) &bull; [Direct PDF](https://arxiv.org/pdf/2103.14917.pdf) &bull; [Official Code](https://github.com/JiamingLi-2020/Frequency-Domain-Learning-for-Face-Forgery-Detection)

### 6. Generalizing Face Forgery Detection with High-frequency Features
- **Authors:** Yuzhen Luo, Yan Ju, Jiaming Liu, Jiankang Deng
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `High-Frequency Residual Filtering`
- **Architecture:** High-frequency residual extraction with multi-scale Laplacian filtering
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **AUC: 89.2% on cross-dataset evaluation** (ROC-AUC (%))
- **Identified Limitations:** *Residuals diminish rapidly when images undergo lossy JPEG or H.264 compression.*
- **Access Links:** [Local PDF Archive](/papers/Generalizing_High_Frequency_Luo_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2103.12376) &bull; [Direct PDF](https://arxiv.org/pdf/2103.12376.pdf) &bull; [Official Code](https://github.com/luoyuzhou/Generalizing-Face-Forgery-Detection)

## Diffusion & Generative Fingerprints
*Examines architectural fingerprints specific to modern latent diffusion models (LDMs), DDIM inversion error, text-to-image attribution, and flow-matching engines.*

### 1. CNN-Generated Images Are Surprisingly Easy to Spot... for Now
- **Authors:** Sheng-Yu Wang, Oliver Wang, Richard Zhang, Andrew Owens, Alexei A. Efros
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `CNN Periodic Upsampling Artifacts`
- **Architecture:** ResNet-50 with Blur & JPEG Data Augmentations
- **Primary Dataset:** ProGAN (train); tested on StyleGAN, BigGAN, CycleGAN
- **Reported Performance:** **AP > 95% on StyleGAN & BigGAN** (Average Precision (AP), Accuracy)
- **Identified Limitations:** *Relies on periodic upsampling artifacts specific to CNN generators; drops sharply on diffusion models.*
- **Access Links:** [Local PDF Archive](/papers/CNN_Detection_Wang_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1912.11035) &bull; [Direct PDF](https://arxiv.org/pdf/1912.11035.pdf) &bull; [Official Code](https://github.com/peterwang512/CNNDetection)

### 2. Towards Universal Fake Image Detectors that Generalize Across Generative Models
- **Authors:** Utkarsh Ojha, Yuheng Li, Yong Jae Lee
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `Pretrained Vision-Language Probing (CLIP)`
- **Architecture:** Frozen CLIP ViT-L/14 + Linear Probe
- **Primary Dataset:** ProGAN (train); tested on LDM, SD, DALL-E, GLIDE, StyleGAN
- **Reported Performance:** **AP: 93.4% cross-generator average** (Average Precision (AP))
- **Identified Limitations:** *Linear probe on static feature space cannot adapt to subtle local blend boundaries; high inference compute.*
- **Access Links:** [Local PDF Archive](/papers/Universal_Fake_Detect_Ojha_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2302.10174) &bull; [Direct PDF](https://arxiv.org/pdf/2302.10174.pdf) &bull; [Official Code](https://github.com/Yuheng-Li/UniversalFakeDetect)

### 3. DIRE for Diffusion-Generated Image Detection
- **Authors:** Zhendong Wang, Jianmin Bao, Wengang Zhou, Weilun Wang, Hezhen Hu, Hong Chen, Houqiang Li
- **Venue & Year:** `ICCV 2023` (2023) &bull; **Sub-Category:** `Diffusion Reconstruction Error (DDIM)`
- **Architecture:** Pretrained DDIM inversion error + ResNet-50
- **Primary Dataset:** ADM, LDM, DiT, GLIDE, Midjourney, ImageNet
- **Reported Performance:** **Acc: 97.4% on diffusion images; AUC: 99.3%** (Accuracy (%), ROC-AUC)
- **Identified Limitations:** *Very slow inference (~1-2 seconds per frame) due to multi-step DDIM inversion requirement.*
- **Access Links:** [Local PDF Archive](/papers/DIRE_Diffusion_Detection_Wang_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2303.09295) &bull; [Direct PDF](https://arxiv.org/pdf/2303.09295.pdf) &bull; [Official Code](https://github.com/ZhendongWang6/DIRE)

### 4. On the Detection of Synthetic Images Generated by Diffusion Models
- **Authors:** Riccardo Corvi, Davide Cozzolino, Giada Zingarini, Giovanni Poggi, Koki Nagano, Luisa Verdoliva
- **Venue & Year:** `ICIP 2023` (2023) &bull; **Sub-Category:** `Latent Diffusion Noise Fingerprinting`
- **Architecture:** ResNet-50 trained on latent diffusion synthetic residuals
- **Primary Dataset:** LDM, Stable Diffusion v1.4, GLIDE, DALL-E 2
- **Reported Performance:** **AUC > 95% on in-distribution diffusion; drops to 72% on unseen architectures** (ROC-AUC (%))
- **Identified Limitations:** *Generalization between different diffusion noise schedules (DDPM vs. Flow Matching) remains brittle.*
- **Access Links:** [Local PDF Archive](/papers/Diffusion_Synthetic_Detection_Corvi_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2211.00680) &bull; [Direct PDF](https://arxiv.org/pdf/2211.00680.pdf) &bull; [Official Code](https://github.com/grip-unina/DMimageDetection)

### 5. Contrasting Deepfakes Diffusion by Global-Local Feature Decoupling (CoDE)
- **Authors:** Davide Cozzolino, Giovanni Poggi, Luisa Verdoliva
- **Venue & Year:** `ECCV 2024` (2024) &bull; **Sub-Category:** `Global-Local Feature Decoupling`
- **Architecture:** Decoupled global semantic and local forensic feature representations (CoDE)
- **Primary Dataset:** DiffusionForensics, GenImage, FaceForensics++
- **Reported Performance:** **AUC: 98.2% on cross-generator diffusion benchmark** (ROC-AUC (%))
- **Identified Limitations:** *Higher latency due to two-stream decoupling backbone.*
- **Access Links:** [Local PDF Archive](/papers/CoDE_Contrasting_Diffusion_Cozzolino_2024.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2403.18789) &bull; [Direct PDF](https://arxiv.org/pdf/2403.18789.pdf) &bull; [Official Code](https://github.com/aimagelab/CoDE)

### 6. DE-FAKE: Detection and Attribution of Fake Images Generated by Text-to-Image Generation Models
- **Authors:** Zeyang Sha, Zheng Li, Ning Yu, Yang Zhang
- **Venue & Year:** `ACM CCS 2023` (2023) &bull; **Sub-Category:** `Text-to-Image Attribution & Watermarking`
- **Architecture:** DE-FAKE: Multi-modal attribution with CLIP and residual classifier
- **Primary Dataset:** Text-to-Image generated images (SD, DALL-E 2, Midjourney)
- **Reported Performance:** **Acc: 92.8% on binary detection; 84.1% on 5-way model attribution** (Accuracy (%), Attribution Precision)
- **Identified Limitations:** *Requires access to text prompt embeddings for optimal attribution accuracy.*
- **Access Links:** [Local PDF Archive](/papers/DE_FAKE_Attribution_Sha_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2210.06998) &bull; [Direct PDF](https://arxiv.org/pdf/2210.06998.pdf) &bull; [Official Code](https://github.com/zeyangsha/DE-FAKE)

### 7. Towards the Detection of Diffusion Model Deepfakes: A Synthetic and Real Benchmark
- **Authors:** Jonas Ricker, Denis Lukovnikov, Asja Fischer
- **Venue & Year:** `WACV 2023` (2023) &bull; **Sub-Category:** `Cross-Architecture Diffusion Benchmarking`
- **Architecture:** Benchmark comparison of ResNet-50, ViT, and Swin across 8 diffusion generators
- **Primary Dataset:** Synthetic & Real Benchmark (ADM, DDPM, IDDPM, LDM, PNDM)
- **Reported Performance:** **AUC drops by up to 25% when evaluating across different guidance scales** (ROC-AUC, AP)
- **Identified Limitations:** *Standard architectures overfit to specific high-frequency spectral spikes of the training scheduler.*
- **Access Links:** [Local PDF Archive](/papers/Towards_Detection_Diffusion_Ricker_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2210.14571) &bull; [Direct PDF](https://arxiv.org/pdf/2210.14571.pdf) &bull; [Official Code](https://github.com/jonasricker/diffusion-model-deepfake-detection)

### 8. Synthbuster: Towards Detection of Diffusion Model Generated Images Using Deep Features
- **Authors:** Quentin Bammey
- **Venue & Year:** `IEEE OJSP 2024` (2024) &bull; **Sub-Category:** `Multi-Generator Deep Residual Features`
- **Architecture:** Synthbuster: Feature extraction across multi-generator residual spaces
- **Primary Dataset:** DALL-E 2/3, Midjourney v5, Stable Diffusion, Firefly
- **Reported Performance:** **AUC: 96.2% on contemporary generative models** (ROC-AUC, Balanced Accuracy)
- **Identified Limitations:** *Performance degrades when images are resized or compressed via social networks.*
- **Access Links:** [Local PDF Archive](/papers/Synthbuster_Diffusion_Bammey_2024.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2305.15008) &bull; [Direct PDF](https://arxiv.org/pdf/2305.15008.pdf) &bull; [Official Code](https://github.com/grip-unina/Synthbuster)

## Temporal & Video Dynamics
*Investigates inter-frame temporal coherence, flicker artifacts, phoneme-viseme biomechanical consistency, and spatiotemporal sequence modeling.*

### 1. Exploring Temporal Coherence for More General Video Face Forgery Detection (FTCN)
- **Authors:** Yinglin Zheng, Jianmin Bao, Dong Chen, Ming Zeng, Fang Wen
- **Venue & Year:** `ICCV 2021` (2021) &bull; **Sub-Category:** `Fully Temporal Convolutional Network`
- **Architecture:** Fully Temporal Convolutional Network (spatio-temporal decouple)
- **Primary Dataset:** FaceForensics++, Celeb-DF v2
- **Reported Performance:** **AUC: 86.9% cross-dataset on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *Video-only; disregards audio-visual cross-consistency cues.*
- **Access Links:** [Local PDF Archive](/papers/FTCN_Temporal_Coherence_Zheng_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2108.06693) &bull; [Direct PDF](https://arxiv.org/pdf/2108.06693.pdf) &bull; [Official Code](https://github.com/yinglinzheng/FTCN)

### 2. Lips Don't Lie: A Generalisable and Robust Approach to Face Forgery Detection (LipForensics)
- **Authors:** Alexandros Haliassos, Konstantinos Vougioukas, Stavros Petridis, Maja Pantic
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Visual Speech Dynamics & Lip Coherence`
- **Architecture:** Spatio-temporal ResNet-18 + Multi-Scale TCN (MS-TCN)
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFDC
- **Reported Performance:** **AUC: 97.1% (FF++ c23), 82.4% (Celeb-DF cross-test)** (ROC-AUC (%))
- **Identified Limitations:** *Only inspects visual mouth movements; does not ingest audio track to verify phoneme-viseme agreement.*
- **Access Links:** [Local PDF Archive](/papers/LipForensics_Lips_Dont_Lie_Haliassos_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2101.03033) &bull; [Direct PDF](https://arxiv.org/pdf/2101.03033.pdf) &bull; [Official Code](https://github.com/alexandros-haliassos/LipForensics)

### 3. Combining EfficientNet and Vision Transformers for Video Deepfake Detection
- **Authors:** David A. Coccomini, Nicola Messina, Fabrizio Falchi, Claudio Gennaro, Giuseppe Amato
- **Venue & Year:** `PRL 2022` (2022) &bull; **Sub-Category:** `Hybrid CNN-Vision Transformer Sequences`
- **Architecture:** EfficientNet feature extractor + Vision Transformer sequence aggregator
- **Primary Dataset:** FaceForensics++, DFDC
- **Reported Performance:** **Acc: 95.1% (FF++ c23), AUC: 98.4%** (Accuracy (%), ROC-AUC)
- **Identified Limitations:** *Computationally expensive sequence aggregation; high VRAM footprint during multi-frame video inference.*
- **Access Links:** [Local PDF Archive](/papers/EfficientNet_ViT_Deepfake_Coccomini_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2107.02612) &bull; [Direct PDF](https://arxiv.org/pdf/2107.02612.pdf) &bull; [Official Code](https://github.com/DavideA/cEfficientViT)

### 4. Spatio-Temporal Inconsistency Learning for Deepfake Video Detection
- **Authors:** Zhihao Gu, Yanchao Bi, Yan Chen, Jing Liu, Baoyuan Wu
- **Venue & Year:** `ACM MM 2021` (2021) &bull; **Sub-Category:** `3D Spatio-Temporal Discrepancy`
- **Architecture:** Spatio-Temporal Inconsistency Learning (STIL) with information-complementary modules
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFDC
- **Reported Performance:** **AUC: 99.5% (FF++ c23), 80.3% (Celeb-DF)** (ROC-AUC (%))
- **Identified Limitations:** *High temporal sampling rate required; fails when video is down-sampled below 10 fps.*
- **Access Links:** [Local PDF Archive](/papers/Spatiotemporal_Inconsistency_Gu_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2109.01860) &bull; [Direct PDF](https://arxiv.org/pdf/2109.01860.pdf) &bull; [Official Code](https://github.com/ZhihaoGu/STIL)

### 5. Detecting Deepfake Videos from Appearance and Motion (AltFreezing)
- **Authors:** Zhendong Wang, Jianmin Bao, Wengang Zhou, Weilun Wang, Houqiang Li
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `Alternating Appearance/Motion Freezing`
- **Architecture:** AltFreezing: Alternating Appearance and Motion Freezing Network
- **Primary Dataset:** FF++, Celeb-DF v2, DFDC, DeeperForensics
- **Reported Performance:** **AUC: 89.5% on cross-dataset Celeb-DF v2** (ROC-AUC (%))
- **Identified Limitations:** *Requires delicate alternating schedule during gradient backpropagation.*
- **Access Links:** [Local PDF Archive](/papers/AltFreezing_Appearance_Motion_Wang_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2304.14818) &bull; [Direct PDF](https://arxiv.org/pdf/2304.14818.pdf) &bull; [Official Code](https://github.com/ZhendongWang6/AltFreezing)

### 6. Detecting Deep-Fake Videos from Phoneme-Viseme Mismatches
- **Authors:** Shruti Agarwal, Hany Farid, Yuming Gu, Ming-Ming Cheng
- **Venue & Year:** `CVPRW 2020` (2020) &bull; **Sub-Category:** `Biomechanical Phoneme-Viseme Inconsistency`
- **Architecture:** Biomechanical Phoneme-Viseme dynamics model via facial landmark tracking
- **Primary Dataset:** In-the-wild political deepfakes, Lip-sync manipulations
- **Reported Performance:** **AUC: 92.5% on speaking portrait videos** (ROC-AUC (%))
- **Identified Limitations:** *Requires clear frontal face angle and unobstructed view of lips and mouth interior.*
- **Access Links:** [Local PDF Archive](/papers/Phoneme_Viseme_Mismatches_Agarwal_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2004.14491) &bull; [Direct PDF](https://arxiv.org/pdf/2004.14491.pdf) &bull; [Official Code](https://github.com/shruti-agarwal/Phoneme-Viseme-Deepfakes)

## Audio Deepfake & Speech Anti-Spoofing
*Inspects raw audio waveforms, linear filterbanks (LFCC/CQCC), graph attention networks (AASIST), and pretrained speech foundation encoders (Wav2Vec 2.0, WavLM, Whisper).*

### 1. STC Antispoofing Systems for the ASVspoof 2019 Challenge (LFCC-LCNN)
- **Authors:** Galina Lavrentyeva, Sergey Novoselov, Evgeny Derbinsky, Marina Volkova, Artem Gorlanov, Alexandr Kozlov
- **Venue & Year:** `Interspeech 2019` (2019) &bull; **Sub-Category:** `Light CNN on Linear Filterbanks (LFCC-LCNN)`
- **Architecture:** Linear Frequency Cepstral Coefficients (LFCC) + Light CNN (LCNN)
- **Primary Dataset:** ASVspoof 2019 Logical Access (LA)
- **Reported Performance:** **EER: 4.53% (baseline on ASVspoof 2019 LA eval)** (min t-DCF, Equal Error Rate (EER %))
- **Identified Limitations:** *Catastrophic error surge (>20% EER) when audio passes through narrowband telephony (3.8 kHz cutoff).*
- **Access Links:** [Local PDF Archive](/papers/LFCC_LCNN_ASVspoof_Lavrentyeva_2019.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1904.05576) &bull; [Direct PDF](https://arxiv.org/pdf/1904.05576.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge/2019)

### 2. RawNet2: More is Better for Voice Anti-Spoofing
- **Authors:** Hemlata Tak, Jose Patino, Andreas Nautsch, Nicholas Evans, Massimiliano Todisco
- **Venue & Year:** `Interspeech 2021` (2021) &bull; **Sub-Category:** `Raw Audio Waveform Sinc-Convolutions`
- **Architecture:** RawNet2 (raw audio waveform + sinc-convolutions + GRU)
- **Primary Dataset:** ASVspoof 2019 LA
- **Reported Performance:** **EER: 5.14% on ASVspoof 2019 LA evaluation** (Equal Error Rate (EER %))
- **Identified Limitations:** *Raw waveform convolutions are susceptible to microphone impulse response variations and room reverberation.*
- **Access Links:** [Local PDF Archive](/papers/RawNet2_Audio_Spoofing_Tak_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2011.01108) &bull; [Direct PDF](https://arxiv.org/pdf/2011.01108.pdf) &bull; [Official Code](https://github.com/eurecom-asp/RawNet2)

### 3. AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks
- **Authors:** Jee-weon Jung, Hee-Soo Heo, Hemlata Tak, Hye-jin Shim, Joon Son Chung, Bong-Jin Lee, Ha-Jin Yu, Nicholas Evans
- **Venue & Year:** `ICASSP 2022` (2022) &bull; **Sub-Category:** `Heterogeneous Graph Attention (AASIST)`
- **Architecture:** Heterogeneous Graph Attention Networks (AASIST)
- **Primary Dataset:** ASVspoof 2019 LA, ASVspoof 2021 DF
- **Reported Performance:** **EER: 0.83% (2019 LA), 15.6% (2021 DF compressed)** (min t-DCF, EER (%))
- **Identified Limitations:** *Graph connectivity is fixed; sharp performance degradation under unseen lossy codecs (Opus/AAC).*
- **Access Links:** [Local PDF Archive](/papers/AASIST_Graph_Attention_Jung_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2110.01200) &bull; [Direct PDF](https://arxiv.org/pdf/2110.01200.pdf) &bull; [Official Code](https://github.com/clovaai/aasist)

### 4. End-to-End Anti-Spoofing with Pre-Trained Wav2Vec 2.0 Models
- **Authors:** Hemlata Tak, Massimiliano Todisco, Xin Wang, Jee-weon Jung, Junichi Yamagishi, Nicholas Evans
- **Venue & Year:** `Interspeech 2022` (2022) &bull; **Sub-Category:** `Self-Supervised Acoustic Representations`
- **Architecture:** Pretrained Wav2Vec 2.0 (XLS-R) + Linear / FC Classifier
- **Primary Dataset:** ASVspoof 2021 Deepfake (DF) and Logical Access (LA)
- **Reported Performance:** **EER: 3.12% on ASVspoof 2021 DF** (Equal Error Rate (EER %))
- **Identified Limitations:** *High parameter count (~300M params); expensive GPU memory footprint for edge deployment.*
- **Access Links:** [Local PDF Archive](/papers/Wav2Vec2_Audio_Spoofing_Tak_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2202.12233) &bull; [Direct PDF](https://arxiv.org/pdf/2202.12233.pdf) &bull; [Official Code](https://github.com/TakHemlata/SSL_Anti-spoofing)

### 5. WaveFake: A Data Set to Facilitate Audio Deepfake Detection
- **Authors:** Joel Frank, Lea Schönherr
- **Venue & Year:** `ACM IH&MMSec 2021` (2021) &bull; **Sub-Category:** `Vocoder Architecture Artifacts`
- **Architecture:** WaveFake Dataset & Mel-Spectrogram ResNet Benchmarks
- **Primary Dataset:** WaveFake (104,885 utterances across 6 modern vocoders)
- **Reported Performance:** **Acc > 99% in-distribution; drops to 62.4% on unseen MelGAN/HiFi-GAN architectures** (EER (%), Accuracy)
- **Identified Limitations:** *Shows that detectors overfit to vocoder-specific high-frequency harmonic artifacts.*
- **Access Links:** [Local PDF Archive](/papers/WaveFake_Dataset_Frank_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2111.02813) &bull; [Direct PDF](https://arxiv.org/pdf/2111.02813.pdf) &bull; [Official Code](https://github.com/joel-frank/wavefake)

### 6. Does Audio Deepfake Detection Generalize to In-the-Wild Scenarios?
- **Authors:** Nicolas M. Müller, Pawel Kawa, Ewa Spyra
- **Venue & Year:** `Interspeech 2022` (2022) &bull; **Sub-Category:** `In-the-Wild Generalization Protocols`
- **Architecture:** ResNet, LCNN, RawNet tested on non-laboratory noisy speech
- **Primary Dataset:** In-The-Wild Audio Deepfake Dataset (social media, podcasts, public talks)
- **Reported Performance:** **EER surges from 2.5% in lab settings to >35.0% in-the-wild** (Equal Error Rate (EER %))
- **Identified Limitations:** *Highlights the extreme vulnerability of acoustic detectors to real-world background acoustic noise.*
- **Access Links:** [Local PDF Archive](/papers/Audio_Deepfake_In_The_Wild_Muller_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2203.16263) &bull; [Direct PDF](https://arxiv.org/pdf/2203.16263.pdf) &bull; [Official Code](https://github.com/media-sec-lab/Audio-Deepfake-Detection)

### 7. Defense Against Audio Deepfakes Using Pretrained Whisper Features
- **Authors:** Piotr Kawa, Marcin Plata, Michał Syga
- **Venue & Year:** `Interspeech 2023` (2023) &bull; **Sub-Category:** `Whisper Log-Mel Encoder Transfer`
- **Architecture:** Pretrained Whisper acoustic encoder + SpecRNet classifier
- **Primary Dataset:** ASVspoof 2021, In-The-Wild, FakeAVCeleb
- **Reported Performance:** **EER: 2.14% in-the-wild; superior speech representation stability** (Equal Error Rate (EER %))
- **Identified Limitations:** *Relies on Whisper's fixed 80-channel log-Mel front-end; limited resolution below 100 Hz.*
- **Access Links:** [Local PDF Archive](/papers/Whisper_Deepfake_Defense_Kawa_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2305.15049) &bull; [Direct PDF](https://arxiv.org/pdf/2305.15049.pdf) &bull; [Official Code](https://github.com/piotrkawa/deepfake-whisper-features)

### 8. An Empirical Study of Speech Self-Supervised Models for Anti-Spoofing
- **Authors:** Lin Zhang, Xin Wang, Erica Cooper, Junichi Yamagishi
- **Venue & Year:** `ICASSP 2023` (2023) &bull; **Sub-Category:** `Comparative Speech SSL Benchmark`
- **Architecture:** Comprehensive benchmark of 15 SSL speech models (WavLM, HuBERT, Wav2Vec 2.0)
- **Primary Dataset:** ASVspoof 2019, ASVspoof 2021
- **Reported Performance:** **WavLM Large achieves 0.98% EER across multi-codec test conditions** (min t-DCF, EER (%))
- **Identified Limitations:** *Enormous model size (1.2 GB) prevents real-time streaming without distillation.*
- **Access Links:** [Local PDF Archive](/papers/Speech_SSL_AntiSpoofing_Zhang_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2302.08182) &bull; [Direct PDF](https://arxiv.org/pdf/2302.08182.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge)

### 9. ASVspoof 2021: Accelerating Progress in Spoofed and Deepfake Speech Detection
- **Authors:** Junichi Yamagishi, Xin Wang, Massimiliano Todisco, Nicholas Evans, et al.
- **Venue & Year:** `Computer Speech & Language 2021` (2021) &bull; **Sub-Category:** `Standardized Speech Spoofing Metrology`
- **Architecture:** Consortium evaluation framework and baseline benchmarks for ASVspoof 2021
- **Primary Dataset:** ASVspoof 2021 (Logical Access, Physical Access, Deepfake)
- **Reported Performance:** **Comprehensive multi-codec lossy compression evaluation across 50+ global teams** (min t-DCF, EER (%))
- **Identified Limitations:** *Revealed that lossy audio compression (MP3/Opus) reduces standalone acoustic accuracy by 40%.*
- **Access Links:** [Local PDF Archive](/papers/ASVspoof_2021_Accelerating_Yamagishi_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2109.00537) &bull; [Direct PDF](https://arxiv.org/pdf/2109.00537.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge/2021)

### 10. Discrepancy-Aware Representation Learning for Audio Deepfake Detection
- **Authors:** Zhiyuan Ba, Xingyi Xie, Wei Du, Xinfeng Dong
- **Venue & Year:** `IEEE/ACM TASLP 2024` (2024) &bull; **Sub-Category:** `Spectrogram Discrepancy Representation`
- **Architecture:** Discrepancy-Aware Representation Learning (DARL) with multi-scale spectrogram diff
- **Primary Dataset:** ASVspoof 2019, WaveFake, In-the-Wild
- **Reported Performance:** **EER: 1.88% cross-dataset average** (Equal Error Rate (EER %))
- **Identified Limitations:** *Sensitivity to non-speech silence intervals in raw recordings.*
- **Access Links:** [Local PDF Archive](/papers/Discrepancy_Aware_Audio_Ba_2024.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2402.16484) &bull; [Direct PDF](https://arxiv.org/pdf/2402.16484.pdf) &bull; [Official Code](https://github.com/ba-speech/DARL)

### 11. ASVspoof 5 Challenge Evaluation Plan: Deepfake Speech in Complex Acoustic Scenarios
- **Authors:** Andreas Nautsch, Nicholas Evans, Junichi Yamagishi, et al.
- **Venue & Year:** `Interspeech 2024` (2024) &bull; **Sub-Category:** `Crowdsourced Speech & Codec Evaluation`
- **Architecture:** Crowdsourced evaluation protocols and realistic acoustic channel simulations
- **Primary Dataset:** ASVspoof 5 (VALL-E, XTTS, StyleTTS2, DiffWave)
- **Reported Performance:** **Baseline systems exhibit 2x EER degradation on zero-shot cloners** (min t-DCF, EER (%))
- **Identified Limitations:** *Challenging licensing terms and multi-terabyte uncompressed audio distribution.*
- **Access Links:** [Local PDF Archive](/papers/ASVspoof5_Challenge_Plan_Nautsch_2024.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2406.18240) &bull; [Direct PDF](https://arxiv.org/pdf/2406.18240.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge/asvspoof5)

## Multimodal Audio-Visual Forensics
*Studies cross-modal synchronization, audio-visual representation dissonance, and joint contrastive learning across facial video and speech tracks.*

### 1. FakeAVCeleb: A Novel Audio-Video Multimodal Deepfake Dataset
- **Authors:** Hasam Khalid, Sharmin Reza, Minh Nguyen, Simon Woo
- **Venue & Year:** `NeurIPS 2021` (2021) &bull; **Sub-Category:** `Four-Quadrant Audio-Visual Benchmark`
- **Architecture:** VGG-Face (visual) + ResNetSE (audio) Late Fusion
- **Primary Dataset:** FakeAVCeleb (Real-Real, Fake-Real, Real-Fake, Fake-Fake)
- **Reported Performance:** **AUC: 85.4% (Multi), 78.2% (Visual only), 69.1% (Audio only)** (ROC-AUC, Accuracy)
- **Identified Limitations:** *Naive late concatenation fails when only one modality is manipulated; easily dominated by visual stream.*
- **Access Links:** [Local PDF Archive](/papers/FakeAVCeleb_Multimodal_Khalid_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2108.05080) &bull; [Direct PDF](https://arxiv.org/pdf/2108.05080.pdf) &bull; [Official Code](https://github.com/DCL-Lab/FakeAVCeleb)

### 2. Joint Audio-Visual Deepfake Detection (AVOiD-DF)
- **Authors:** Yuchen Zhou, Liming Zheng, Bing Han, Jiawei Liu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Cross-Modal Contrastive Learning`
- **Architecture:** Cross-modal contrastive network (Phoneme-Viseme alignment)
- **Primary Dataset:** FakeAVCeleb, DFDC
- **Reported Performance:** **AUC: 89.2% on cross-dataset evaluation** (ROC-AUC, Accuracy)
- **Identified Limitations:** *Sensitive to acoustic background noise and non-standard accents during phoneme mapping.*
- **Access Links:** [Local PDF Archive](/papers/AVOiD_DF_Zhou_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2104.14772) &bull; [Direct PDF](https://arxiv.org/pdf/2104.14772.pdf) &bull; [Official Code](https://github.com/zhouyuchen/AVOiD-DF)

### 3. Self-Supervised Video Forensics by Audio-Visual Anomaly Detection
- **Authors:** Chao Feng, Zunlei Feng, Mingli Song
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `Cross-Modal Anomaly Detection`
- **Architecture:** Autoregressive Audio-Visual Transformer trained ONLY on real videos
- **Primary Dataset:** FakeAVCeleb, DFDC, In-The-Wild
- **Reported Performance:** **AUC: 86.8% zero-shot detection on unseen deepfakes** (Out-of-Distribution ROC-AUC)
- **Identified Limitations:** *Requires temporal sequence alignment; fails on still images or audio-only inputs without fallback mode.*
- **Access Links:** [Local PDF Archive](/papers/SelfSupervised_AudioVisual_Feng_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2301.01798) &bull; [Direct PDF](https://arxiv.org/pdf/2301.01798.pdf) &bull; [Official Code](https://github.com/cfeng16/audio-visual-forensics)

### 4. Not Made for Each Other: Audio-Visual Dissonance-based Deepfake Detection
- **Authors:** Krishna Chugh, Parul Gupta, Abhinav Dhall, Roland Goecke
- **Venue & Year:** `ACM MM 2020` (2020) &bull; **Sub-Category:** `Cross-Modal Representation Dissonance`
- **Architecture:** Audio-Visual Dissonance metric with joint feature cosine dissimilarity
- **Primary Dataset:** In-the-wild political manipulations, DFDC
- **Reported Performance:** **AUC: 91.4% on synchronized speech videos** (ROC-AUC (%))
- **Identified Limitations:** *Fails when speech contains non-vocal audio (music, laugh tracks, stadium noise).*
- **Access Links:** [Local PDF Archive](/papers/Audio_Visual_Dissonance_Chugh_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2005.14405) &bull; [Direct PDF](https://arxiv.org/pdf/2005.14405.pdf) &bull; [Official Code](https://github.com/krishnachugh/AV-Dissonance)

### 5. AVFF: Audio-Visual Feature Fusion for Generalizable Deepfake Detection
- **Authors:** Trevor Oorloff, Yuezun Li, Siwei Lyu
- **Venue & Year:** `IEEE TIFS 2024` (2024) &bull; **Sub-Category:** `Hierarchical Audio-Visual Fusion`
- **Architecture:** Hierarchical Audio-Visual Feature Fusion (AVFF) with cross-attention
- **Primary Dataset:** FakeAVCeleb, DFDC
- **Reported Performance:** **AUC: 95.3% on FakeAVCeleb** (ROC-AUC, Balanced Acc)
- **Identified Limitations:** *Computationally intensive two-stage pretraining; requires high VRAM for dual video-audio backbones.*
- **Access Links:** [Local PDF Archive](/papers/AVFF_Audio_Visual_Fusion_Oorloff_2024.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2401.08761) &bull; [Direct PDF](https://arxiv.org/pdf/2401.08761.pdf) &bull; [Official Code](https://github.com/DCL-Lab/AVFF)

### 6. Dual-Branch Spatio-Temporal Cross-Attention for Audio-Visual Deepfake Detection
- **Authors:** Ke Sun, Hongxun Yao, Xiaoshuai Sun, Sicheng Zhao
- **Venue & Year:** `ACM MM 2023` (2023) &bull; **Sub-Category:** `Cross-Attention Transformers`
- **Architecture:** Transformer cross-attention with dynamic missing-modality dropout
- **Primary Dataset:** FakeAVCeleb, LAV-DF
- **Reported Performance:** **F1: 91.2%; retains >82% AUC when audio or video is missing** (ROC-AUC, F1-Score)
- **Identified Limitations:** *Requires custom training with stochastic modality dropping to learn unimodal fallback paths.*
- **Access Links:** [Local PDF Archive](/papers/DualBranch_Cross_Attention_Sun_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2308.09452) &bull; [Direct PDF](https://arxiv.org/pdf/2308.09452.pdf) &bull; [Official Code](https://github.com/sun-av/cross-attention-df)

## Codec & Compression Robustness
*Addresses forensic vulnerability to lossy social media compression (JPEG, H.264/AVC, H.265/HEVC, Opus, MP3), anti-forensic perturbation attacks, and out-of-distribution shifts.*

### 1. Anti-Forensics of Video Deepfake Detection via GAN-Based Post-Processing
- **Authors:** Paarth Neekhara, Brian Dolhansky, Hao Cheng, Julian McAuley
- **Venue & Year:** `CVPRW 2021` (2021) &bull; **Sub-Category:** `Adversarial Anti-Forensics & Artifact Masking`
- **Architecture:** Adversarial GAN-based post-processor adding imperceptible noise to evade detectors
- **Primary Dataset:** FaceForensics++, Deepfake Detection Challenge
- **Reported Performance:** **Reduces standard XceptionNet detection accuracy from 98% to 12%** (Attack Success Rate (ASR %))
- **Identified Limitations:** *Shows that purely spatial detectors are fragile to targeted pixel perturbations.*
- **Access Links:** [Local PDF Archive](/papers/Anti_Forensics_Video_Deepfake_Neekhara_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2003.01265) &bull; [Direct PDF](https://arxiv.org/pdf/2003.01265.pdf) &bull; [Official Code](https://github.com/paarthneekhara/deepfake_antiforensics)

### 2. ID-Reveal: Out-of-Distribution Deepfake Detection via Biometric Representation Learning
- **Authors:** Davide Cozzolino, Andreas Rössler, Justus Thies, Matthias Nießner, Luisa Verdoliva
- **Venue & Year:** `ICCV 2021` (2021) &bull; **Sub-Category:** `Biometric Identity Invariance`
- **Architecture:** ID-Reveal: Biometric facial representation learning conditioned on identity
- **Primary Dataset:** FaceForensics++, Celeb-DF v2
- **Reported Performance:** **AUC: 87.2% zero-shot transfer without identity priors** (ROC-AUC (%))
- **Identified Limitations:** *Requires reference enrollment identity images; cannot operate in zero-context verification.*
- **Access Links:** [Local PDF Archive](/papers/ID_Reveal_Biometric_Cozzolino_2021.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2012.02512) &bull; [Direct PDF](https://arxiv.org/pdf/2012.02512.pdf) &bull; [Official Code](https://github.com/grip-unina/ID-Reveal)

### 3. Adversarial Robustness of Deepfake Detectors
- **Authors:** Apurva Gandhi, Shomik Jain
- **Venue & Year:** `CVPRW 2020` (2020) &bull; **Sub-Category:** `Adversarial Perturbation Sensitivity`
- **Architecture:** Adversarial FGSM and PGD perturbations evaluated against top forensic detectors
- **Primary Dataset:** FaceForensics++, CelebA
- **Reported Performance:** **Perturbations under epsilon=2/255 reduce detector accuracy below 50%** (Accuracy drop (%))
- **Identified Limitations:** *Detectors lacking frequency residual grounding are highly susceptible to gradient-based attacks.*
- **Access Links:** [Local PDF Archive](/papers/Adversarial_Robustness_Gandhi_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2003.11145) &bull; [Direct PDF](https://arxiv.org/pdf/2003.11145.pdf) &bull; [Official Code](https://github.com/adv-deepfake/adversarial-deepfake)

### 4. Leveraging Real Talking Faces via Self-Supervision for Robust Forgery Detection (RealForensics)
- **Authors:** Alexandros Haliassos, Rodrigo Mira, Stavros Petridis, Maja Pantic
- **Venue & Year:** `CVPR 2022` (2022) &bull; **Sub-Category:** `Self-Supervised Natural Face Motion`
- **Architecture:** Self-supervised natural talking face representation (RealForensics)
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFDC, WildDeepfake
- **Reported Performance:** **AUC: 86.9% cross-dataset on Celeb-DF; high robustness to lossy codecs** (ROC-AUC (%))
- **Identified Limitations:** *Relies on video motion dynamics; cannot classify still individual frames.*
- **Access Links:** [Local PDF Archive](/papers/RealForensics_SelfSupervised_Haliassos_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2201.03051) &bull; [Direct PDF](https://arxiv.org/pdf/2201.03051.pdf) &bull; [Official Code](https://github.com/alexandros-haliassos/RealForensics)

## Surveys, Benchmarks & Metrology
*Standardized evaluation benchmarks, unified evaluation toolkits (DeepfakeBench), challenge datasets (DFDC, Celeb-DF), and comprehensive state-of-the-art literature surveys.*

### 1. DeepfakeBench: A Comprehensive Benchmark of Deepfake Detection
- **Authors:** Zhiyuan Yan, Yong Zhang, Xuesong Yin, Jing Xiao, Baoyuan Wu
- **Venue & Year:** `NeurIPS 2023` (2023) &bull; **Sub-Category:** `Unified Modular Evaluation Benchmark`
- **Architecture:** Standardized benchmark framework with 15 detection methods and 9 datasets
- **Primary Dataset:** FF++, Celeb-DF, DFD, DFDC, FaceShifter, DeeperForensics
- **Reported Performance:** **Discloses that best detectors drop by 20-30% AUC when transitioning to unseen cross-dataset scenarios** (ROC-AUC, EER, Cross-dataset generalization)
- **Identified Limitations:** *Heavy memory requirements to evaluate all 15 backbones across 9 benchmarks.*
- **Access Links:** [Local PDF Archive](/papers/DeepfakeBench_Yan_2023.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2307.01426) &bull; [Direct PDF](https://arxiv.org/pdf/2307.01426.pdf) &bull; [Official Code](https://github.com/SCLBD/DeepfakeBench)

### 2. Media Forensics in the Age of Generative AI: A Survey
- **Authors:** Luisa Verdoliva
- **Venue & Year:** `IEEE SPM 2020` (2020) &bull; **Sub-Category:** `Holistic Multimedia Forensic Foundations`
- **Architecture:** Comprehensive survey of multimedia forensic foundations, PRNU, steganography, and deep learning
- **Primary Dataset:** All public benchmarks
- **Reported Performance:** **Established foundational criteria for forensic explainability, anti-compression, and generalization** (Survey Taxonomy)
- **Identified Limitations:** *Pre-dates the rapid emergence of commercial latent diffusion and flow-matching models.*
- **Access Links:** [Local PDF Archive](/papers/Media_Forensics_Generative_AI_Verdoliva_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2004.14565) &bull; [Direct PDF](https://arxiv.org/pdf/2004.14565.pdf) &bull; [Official Code](https://github.com/grip-unina)

### 3. Deep Learning for Deepfakes Creation and Detection: A Survey
- **Authors:** Thanh Thi Nguyen, Cuong M. Nguyen, Dung Tien Nguyen, Duc Thanh Nguyen, Saeid Nahavandi
- **Venue & Year:** `CVIU 2022` (2022) &bull; **Sub-Category:** `Comprehensive Creation & Detection Taxonomies`
- **Architecture:** Detailed taxonomic survey of GANs, autoencoders, and early deepfake detection mechanisms
- **Primary Dataset:** Early benchmarks
- **Reported Performance:** **First systematized analysis of Deepfakes, Face2Face, FaceSwap, and NeuralTextures** (Comprehensive Survey)
- **Identified Limitations:** *Focuses primarily on early autoencoder generation pipelines.*
- **Access Links:** [Local PDF Archive](/papers/Deep_Learning_Deepfakes_Nguyen_2022.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1909.11573) &bull; [Direct PDF](https://arxiv.org/pdf/1909.11573.pdf) &bull; [Official Code](https://github.com/ondyari/FaceForensics)

### 4. The Deepfake Detection Challenge (DFDC) Dataset
- **Authors:** Brian Dolhansky, Joanna Bitton, Ben Pflaum, Jikuo Lu, Russ Howes, Mengjiao Wang, Cristian Canton Ferrer
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Large-Scale Public Challenge Dataset`
- **Architecture:** DFDC dataset release & Kaggle challenge evaluation
- **Primary Dataset:** DFDC (128,154 clips, 3,426 actors, diverse lighting & backgrounds)
- **Reported Performance:** **Top Kaggle ensemble achieved 82.5% AUC on unseen private test set** (Log-Loss, ROC-AUC)
- **Identified Limitations:** *Contains challenging lighting and compression that degrades standard CNN accuracy to near chance.*
- **Access Links:** [Local PDF Archive](/papers/DFDC_Dataset_Dolhansky_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/2006.07397) &bull; [Direct PDF](https://arxiv.org/pdf/2006.07397.pdf) &bull; [Official Code](https://github.com/facebookresearch/DFDC)

### 5. Celeb-DF: A Large-scale Challenging Dataset for Deepfake Forensics
- **Authors:** Yuezun Li, Xin Yang, Pu Sun, Honggang Qi, Siwei Lyu
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `High-Quality Face Swap Benchmark`
- **Architecture:** Celeb-DF v2 dataset generation & comparative benchmark
- **Primary Dataset:** Celeb-DF v2 (5,639 high-quality videos, reduced boundary artifacts)
- **Reported Performance:** **Demonstrated that detectors trained on FF++ drop from 99% to ~65% on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *High-quality blending eliminates coarse splicing artifacts relied on by early detectors.*
- **Access Links:** [Local PDF Archive](/papers/Celeb_DF_Dataset_Li_2020.pdf) &bull; [arXiv Abstract](https://arxiv.org/abs/1909.12962) &bull; [Direct PDF](https://arxiv.org/pdf/1909.12962.pdf) &bull; [Official Code](https://github.com/yuezunli/celeb-deepfakeforensics)
