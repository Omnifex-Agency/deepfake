# Deepfake Research Collective — Forensic Literature Repository & Paper Directory

> **Archive Status:** 78 Verified Academic Papers Cataloged across 11 Specialized Scientific Domains.
> All papers index verified arXiv/venue identifiers, conference venues, direct local PDF endpoints, official code repositories, reported benchmark metrics, and known research limitations.

## Table of Contents

1. [Spatial & Blending Forensics (8 Papers)](#spatial--blending-forensics)
2. [Frequency & Spectral Forensics (6 Papers)](#frequency--spectral-forensics)
3. [Diffusion & Generative Fingerprints (8 Papers)](#diffusion--generative-fingerprints)
4. [Temporal & Video Dynamics (9 Papers)](#temporal--video-dynamics)
5. [Audio Deepfake & Speech Anti-Spoofing (15 Papers)](#audio-deepfake--speech-anti-spoofing)
6. [Multimodal Audio-Visual Forensics (8 Papers)](#multimodal-audio-visual-forensics)
7. [Biological & Physiological Forensics (4 Papers)](#biological--physiological-forensics)
8. [Watermarking, Provenance & Defensive Cloaking (4 Papers)](#watermarking-provenance--defensive-cloaking)
9. [Psychology, Perception & Epistemic Impact (3 Papers)](#psychology-perception--epistemic-impact)
10. [Codec & Compression Robustness (4 Papers)](#codec--compression-robustness)
11. [Surveys, Benchmarks & Metrology (9 Papers)](#surveys-benchmarks--metrology)

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
- **Access Links:** [Local PDF Endpoint](/papers/FaceForensics_PlusPlus_Rossler_2019.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1901.08971) &bull; [Direct PDF](https://arxiv.org/pdf/1901.08971.pdf) &bull; [Official Code](https://github.com/ondyari/FaceForensics)

### 2. Face X-Ray for More General Face Forgery Detection
- **Authors:** Lingzhi Li, Jianmin Bao, Ting Zhang, Hao Yang, Dong Chen, Fang Wen, Baining Guo
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Blending Boundary Segmentation`
- **Architecture:** HRNet / ResNet predicting blending boundaries
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFD
- **Reported Performance:** **AUC: 99.1% (FF++ c23), 74.8% (Celeb-DF cross-test)** (ROC-AUC (%))
- **Identified Limitations:** *Only detects composite/swapped images; completely blind to wholly synthetic faces (StyleGAN/LDM).*
- **Access Links:** [Local PDF Endpoint](/papers/Face_XRay_Li_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1912.12623) &bull; [Direct PDF](https://arxiv.org/pdf/1912.12623.pdf) &bull; [Official Code](https://github.com/li-lingzhi/FaceXray)

### 3. What Makes Fake Images Detectable? Understanding Properties of Synthesized Images
- **Authors:** Lucy Chai, David Bau, Ser-Nam Lim, Phillip Isola
- **Venue & Year:** `ECCV 2020` (2020) &bull; **Sub-Category:** `Patch-Level Truncation`
- **Architecture:** Truncated patch-level fully convolutional network
- **Primary Dataset:** FF++, Celeb-DF, FaceSwap
- **Reported Performance:** **AP: 83.3% on Celeb-DF cross-evaluation** (Average Precision (AP))
- **Identified Limitations:** *Truncated receptive field loses global semantic coherence and long-range structural dependencies.*
- **Access Links:** [Local PDF Endpoint](/papers/Patch_Forensics_Chai_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2008.10588) &bull; [Direct PDF](https://arxiv.org/pdf/2008.10588.pdf) &bull; [Official Code](https://github.com/chail/patch-forensics)

### 4. Multi-attentional Deepfake Detection
- **Authors:** Hanqing Zhao, Wenbo Zhou, Dongdong Chen, Tianyi Wei, Weiming Zhang, Nenghai Yu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Multi-Region Spatial Attention`
- **Architecture:** Multi-attentional network with region-independent loss and texture enhancement
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFD
- **Reported Performance:** **AUC: 99.8% (FF++ c23), 77.2% (Celeb-DF cross-test)** (ROC-AUC, Accuracy)
- **Identified Limitations:** *Attention heads can drift toward background artifacts when face alignment fluctuates.*
- **Access Links:** [Local PDF Endpoint](/papers/Multi_Attentional_Zhao_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2103.02406) &bull; [Direct PDF](https://arxiv.org/pdf/2103.02406.pdf) &bull; [Official Code](https://github.com/nii-yamagishilab/Multi-attentional-Deepfake-Detection)

### 5. Pair-wise Self-Consistency Learning for Deepfake Detection
- **Authors:** Tianchen Zhao, Xiang Xu, Mingze Xu, Hao Ding, Yuanjun Xiong, Wei Xia
- **Venue & Year:** `ACM MM 2021` (2021) &bull; **Sub-Category:** `Pairwise Consistency`
- **Architecture:** Pair-wise self-consistency learning with patch similarity
- **Primary Dataset:** FF++, Celeb-DF v2, DFDC
- **Reported Performance:** **AUC: 86.9% cross-dataset on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *High computational overhead for pairwise patch-similarity matrix computation.*
- **Access Links:** [Local PDF Endpoint](/papers/Pairwise_Self_Consistency_Zhao_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2105.04838) &bull; [Direct PDF](https://arxiv.org/pdf/2105.04838.pdf) &bull; [Official Code](https://github.com/chail/patch-forensics)

### 6. Look Locally for Understanding Globally: A Generalizable Face Forgery Detection via Reconstruction
- **Authors:** Hao Chen, Haotian Hong, Zhaoyu Chen, Keyu Chen, Yaohui Li
- **Venue & Year:** `ECCV 2022` (2022) &bull; **Sub-Category:** `Local-Global Reconstruction`
- **Architecture:** Local gradient reconstruction network with high-frequency loss
- **Primary Dataset:** FaceForensics++, Celeb-DF, WildDeepfake
- **Reported Performance:** **AUC: 89.1% cross-dataset on Celeb-DF v2** (ROC-AUC (%))
- **Identified Limitations:** *Reconstruction quality degrades significantly on extreme low-resolution face crops (<64x64).*
- **Access Links:** [Local PDF Endpoint](/papers/Look_Locally_Chen_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2207.03061) &bull; [Direct PDF](https://arxiv.org/pdf/2207.03061.pdf) &bull; [Official Code](https://github.com/ChenH0528/LGrad)

### 7. Rethinking the Up-Sampling Operations in CNN-based Face Forgery Detection
- **Authors:** Chuangchuang Tan, Yao Zhao, Shikui Wei, Guanghua Gu, Ping Liu, Yunchao Wei
- **Venue & Year:** `CVPR 2024` (2024) &bull; **Sub-Category:** `Neighboring Pixel Relationship (NPR)`
- **Architecture:** Neighboring Pixel Relationship (NPR) residual extractor with ConvNeXt
- **Primary Dataset:** FaceForensics++, Celeb-DF, WildDeepfake, DiffusionForensics
- **Reported Performance:** **AUC: 91.5% cross-generator average across GANs and Diffusion** (ROC-AUC (%))
- **Identified Limitations:** *Requires careful pixel neighbor stride tuning depending on downsampling factors.*
- **Access Links:** [Local PDF Endpoint](/papers/NPR_Upsampling_Tan_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2403.18808) &bull; [Direct PDF](https://arxiv.org/pdf/2403.18808.pdf) &bull; [Official Code](https://github.com/chuangchuangtan/NPR-DeepfakeDetection)

### 8. SimSwap: An Efficient Framework For High Fidelity Face Swapping
- **Authors:** Renwang Chen, Xuanhong Chen, Bingbing Ni, Yanhao Ge
- **Venue & Year:** `ACM MM 2020` (2020) &bull; **Sub-Category:** `Generalized Face Swapping`
- **Architecture:** Identity Extraction Net + Weak Feature Matching + ID Injection Module
- **Primary Dataset:** VGGFace2, FaceForensics++
- **Reported Performance:** **Real-time arbitrary identity swapping across arbitrary target videos** (ID Retrieval (%) & Pose Angle)
- **Identified Limitations:** *Resolution loss on non-frontal faces; boundary color mismatch under dynamic lighting.*
- **Access Links:** [Local PDF Endpoint](/papers/SimSwap_Face_Swapping_Chen_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2106.06340) &bull; [Direct PDF](https://arxiv.org/pdf/2106.06340.pdf) &bull; [Official Code](https://github.com/neuralchen/SimSwap)

## Frequency & Spectral Forensics
*Analyzes Discrete Cosine Transform (DCT), Discrete Fourier Transform (DFT), high-pass residuals, and phase spectra to detect generative spectral anomalies.*

### 1. Leveraging Frequency Analysis for Deep Fake Image Recognition
- **Authors:** Joel Frank, Thorsten Eisenhofer, Lea Schönherr, Asja Fischer, Dorothea Kolossa, Thorsten Holz
- **Venue & Year:** `ICML 2020` (2020) &bull; **Sub-Category:** `Discrete Cosine Transform (DCT)`
- **Architecture:** Discrete Cosine Transform (DCT) + Linear Classifier / CNN
- **Primary Dataset:** FaceForensics++, CelebA-HQ, ProGAN
- **Reported Performance:** **AUC > 99.0% on uncompressed sets** (ROC-AUC (%))
- **Identified Limitations:** *High sensitivity to standard post-processing (Gaussian blur, social media recompression).*
- **Access Links:** [Local PDF Endpoint](/papers/Frequency_Analysis_Frank_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2003.08685) &bull; [Direct PDF](https://arxiv.org/pdf/2003.08685.pdf) &bull; [Official Code](https://github.com/frederic-frank/frequency-analysis-for-deep-fake-image-recognition)

### 2. Watch your Up-Convolution: CNN Based Generative Deep Neural Networks are Failing to Reproduce Spectral Distributions
- **Authors:** Ricard Durall, Margret Keuper, Franz-Josef Pfreundt, Janis Keuper
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Radial Spectral Analysis (Azimuthal Average)`
- **Architecture:** Azimuthal average spectral distribution analysis over DFT power spectra
- **Primary Dataset:** CelebA-HQ, FFHQ, StyleGAN, DCGAN
- **Reported Performance:** **Acc: 100.0% on uncompressed GAN images** (Accuracy (%))
- **Identified Limitations:** *Assumes standard up-convolution interpolation; easily spoofed by spectral loss regularization during training.*
- **Access Links:** [Local PDF Endpoint](/papers/Watch_Your_Up_Convolution_Durall_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1911.00686) &bull; [Direct PDF](https://arxiv.org/pdf/1911.00686.pdf) &bull; [Official Code](https://github.com/cc-hpc-itwm/UpConvolution)

### 3. Thinking in Frequency: Face Forgery Detection by Mining Frequency-aware Clues (F3-Net)
- **Authors:** Yuyang Qian, Guojun Yin, Shenggyang Lu, Xiang Chen, Lu Dong, Fang Wen
- **Venue & Year:** `ECCV 2020` (2020) &bull; **Sub-Category:** `Dual-Stream Frequency Decomposition (F3-Net)`
- **Architecture:** Dual-stream frequency-aware network (F3-Net) with FAD and LFS branches
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **Acc: 90.4% on FF++ c40; AUC: 75.3% on Celeb-DF** (Accuracy (%), ROC-AUC)
- **Identified Limitations:** *Frequency band partitioning requires manual cutoff frequency selection based on target codec.*
- **Access Links:** [Local PDF Endpoint](/papers/Thinking_In_Frequency_Qian_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2007.09355) &bull; [Direct PDF](https://arxiv.org/pdf/2007.09355.pdf) &bull; [Official Code](https://github.com/weixiangquan/F3-Net)

### 4. Spatial-Phase Shallow Learning: Rethinking Face Forgery Detection in Frequency Domain (SPSL)
- **Authors:** Honggu Liu, Xiaodan Li, Wenbo Zhou, Yuefeng Chen, Yuan He, Hui Xue, Weiming Zhang, Nenghai Yu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Phase Spectrum Analysis`
- **Architecture:** Spatial-Phase Shallow Learning (SPSL) with phase spectrum extraction
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFD
- **Reported Performance:** **AUC: 81.6% cross-dataset on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *Phase calculation is sensitive to spatial warping and non-rigid facial deformations.*
- **Access Links:** [Local PDF Endpoint](/papers/Spatial_Phase_Shallow_Cao_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2103.05348) &bull; [Direct PDF](https://arxiv.org/pdf/2103.05348.pdf) &bull; [Official Code](https://github.com/SunnyBingoMe/SPSL)

### 5. Frequency-Domain Learning for Face Forgery Detection
- **Authors:** Jiaming Li, Yuezun Li, Siwei Lyu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Multi-Frequency Band Attention`
- **Architecture:** Multi-frequency band attention network with adaptive frequency decomposition
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **AUC: 99.3% (FF++ c23), 78.4% (Celeb-DF)** (ROC-AUC (%))
- **Identified Limitations:** *Performance degrades under high-frequency cutoff filters such as heavy JPEG Q<40.*
- **Access Links:** [Local PDF Endpoint](/papers/Frequency_Domain_Learning_Li_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2103.14917) &bull; [Direct PDF](https://arxiv.org/pdf/2103.14917.pdf) &bull; [Official Code](https://github.com/JiamingLi-2020/Frequency-Domain-Learning-for-Face-Forgery-Detection)

### 6. Generalizing Face Forgery Detection with High-frequency Features
- **Authors:** Yuzhen Luo, Yan Ju, Jiaming Liu, Jiankang Deng
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `High-Frequency Residual Filtering`
- **Architecture:** High-frequency residual extraction with multi-scale Laplacian filtering
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **AUC: 89.2% on cross-dataset evaluation** (ROC-AUC (%))
- **Identified Limitations:** *Residuals diminish rapidly when images undergo lossy JPEG or H.264 compression.*
- **Access Links:** [Local PDF Endpoint](/papers/Generalizing_High_Frequency_Luo_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2103.12376) &bull; [Direct PDF](https://arxiv.org/pdf/2103.12376.pdf) &bull; [Official Code](https://github.com/luoyuzhou/Generalizing-Face-Forgery-Detection)

## Diffusion & Generative Fingerprints
*Examines architectural fingerprints specific to modern latent diffusion models (LDMs), DDIM inversion error, text-to-image attribution, and flow-matching engines.*

### 1. CNN-Generated Images Are Surprisingly Easy to Spot... for Now
- **Authors:** Sheng-Yu Wang, Oliver Wang, Richard Zhang, Andrew Owens, Alexei A. Efros
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `CNN Periodic Upsampling Artifacts`
- **Architecture:** ResNet-50 with Blur & JPEG Data Augmentations
- **Primary Dataset:** ProGAN (train); tested on StyleGAN, BigGAN, CycleGAN
- **Reported Performance:** **AP > 95% on StyleGAN & BigGAN** (Average Precision (AP), Accuracy)
- **Identified Limitations:** *Relies on periodic upsampling artifacts specific to CNN generators; drops sharply on diffusion models.*
- **Access Links:** [Local PDF Endpoint](/papers/CNN_Detection_Wang_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1912.11035) &bull; [Direct PDF](https://arxiv.org/pdf/1912.11035.pdf) &bull; [Official Code](https://github.com/peterwang512/CNNDetection)

### 2. Towards Universal Fake Image Detectors that Generalize Across Generative Models
- **Authors:** Utkarsh Ojha, Yuheng Li, Yong Jae Lee
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `Pretrained Vision-Language Probing (CLIP)`
- **Architecture:** Frozen CLIP ViT-L/14 + Linear Probe
- **Primary Dataset:** ProGAN (train); tested on LDM, SD, DALL-E, GLIDE, StyleGAN
- **Reported Performance:** **AP: 93.4% cross-generator average** (Average Precision (AP))
- **Identified Limitations:** *Linear probe on static feature space cannot adapt to subtle local blend boundaries; high inference compute.*
- **Access Links:** [Local PDF Endpoint](/papers/Universal_Fake_Detect_Ojha_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2302.10174) &bull; [Direct PDF](https://arxiv.org/pdf/2302.10174.pdf) &bull; [Official Code](https://github.com/Yuheng-Li/UniversalFakeDetect)

### 3. DIRE for Diffusion-Generated Image Detection
- **Authors:** Zhendong Wang, Jianmin Bao, Wengang Zhou, Weilun Wang, Hezhen Hu, Hong Chen, Houqiang Li
- **Venue & Year:** `ICCV 2023` (2023) &bull; **Sub-Category:** `Diffusion Reconstruction Error (DDIM)`
- **Architecture:** Pretrained DDIM inversion error + ResNet-50
- **Primary Dataset:** ADM, LDM, DiT, GLIDE, Midjourney, ImageNet
- **Reported Performance:** **Acc: 97.4% on diffusion images; AUC: 99.3%** (Accuracy (%), ROC-AUC)
- **Identified Limitations:** *Very slow inference (~1-2 seconds per frame) due to multi-step DDIM inversion requirement.*
- **Access Links:** [Local PDF Endpoint](/papers/DIRE_Diffusion_Detection_Wang_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2303.09295) &bull; [Direct PDF](https://arxiv.org/pdf/2303.09295.pdf) &bull; [Official Code](https://github.com/ZhendongWang6/DIRE)

### 4. On the Detection of Synthetic Images Generated by Diffusion Models
- **Authors:** Riccardo Corvi, Davide Cozzolino, Giada Zingarini, Giovanni Poggi, Koki Nagano, Luisa Verdoliva
- **Venue & Year:** `ICIP 2023` (2023) &bull; **Sub-Category:** `Latent Diffusion Noise Fingerprinting`
- **Architecture:** ResNet-50 trained on latent diffusion synthetic residuals
- **Primary Dataset:** LDM, Stable Diffusion v1.4, GLIDE, DALL-E 2
- **Reported Performance:** **AUC > 95% on in-distribution diffusion; drops to 72% on unseen architectures** (ROC-AUC (%))
- **Identified Limitations:** *Generalization between different diffusion noise schedules (DDPM vs. Flow Matching) remains brittle.*
- **Access Links:** [Local PDF Endpoint](/papers/Diffusion_Synthetic_Detection_Corvi_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2211.00680) &bull; [Direct PDF](https://arxiv.org/pdf/2211.00680.pdf) &bull; [Official Code](https://github.com/grip-unina/DMimageDetection)

### 5. Contrasting Deepfakes Diffusion by Global-Local Feature Decoupling (CoDE)
- **Authors:** Davide Cozzolino, Giovanni Poggi, Luisa Verdoliva
- **Venue & Year:** `ECCV 2024` (2024) &bull; **Sub-Category:** `Global-Local Feature Decoupling`
- **Architecture:** Decoupled global semantic and local forensic feature representations (CoDE)
- **Primary Dataset:** DiffusionForensics, GenImage, FaceForensics++
- **Reported Performance:** **AUC: 98.2% on cross-generator diffusion benchmark** (ROC-AUC (%))
- **Identified Limitations:** *Higher latency due to two-stream decoupling backbone.*
- **Access Links:** [Local PDF Endpoint](/papers/CoDE_Contrasting_Diffusion_Cozzolino_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2403.18789) &bull; [Direct PDF](https://arxiv.org/pdf/2403.18789.pdf) &bull; [Official Code](https://github.com/aimagelab/CoDE)

### 6. DE-FAKE: Detection and Attribution of Fake Images Generated by Text-to-Image Generation Models
- **Authors:** Zeyang Sha, Zheng Li, Ning Yu, Yang Zhang
- **Venue & Year:** `ACM CCS 2023` (2023) &bull; **Sub-Category:** `Text-to-Image Attribution & Watermarking`
- **Architecture:** DE-FAKE: Multi-modal attribution with CLIP and residual classifier
- **Primary Dataset:** Text-to-Image generated images (SD, DALL-E 2, Midjourney)
- **Reported Performance:** **Acc: 92.8% on binary detection; 84.1% on 5-way model attribution** (Accuracy (%), Attribution Precision)
- **Identified Limitations:** *Requires access to text prompt embeddings for optimal attribution accuracy.*
- **Access Links:** [Local PDF Endpoint](/papers/DE_FAKE_Attribution_Sha_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2210.06998) &bull; [Direct PDF](https://arxiv.org/pdf/2210.06998.pdf) &bull; [Official Code](https://github.com/zeyangsha/DE-FAKE)

### 7. Towards the Detection of Diffusion Model Deepfakes: A Synthetic and Real Benchmark
- **Authors:** Jonas Ricker, Denis Lukovnikov, Asja Fischer
- **Venue & Year:** `WACV 2023` (2023) &bull; **Sub-Category:** `Cross-Architecture Diffusion Benchmarking`
- **Architecture:** Benchmark comparison of ResNet-50, ViT, and Swin across 8 diffusion generators
- **Primary Dataset:** Synthetic & Real Benchmark (ADM, DDPM, IDDPM, LDM, PNDM)
- **Reported Performance:** **AUC drops by up to 25% when evaluating across different guidance scales** (ROC-AUC, AP)
- **Identified Limitations:** *Standard architectures overfit to specific high-frequency spectral spikes of the training scheduler.*
- **Access Links:** [Local PDF Endpoint](/papers/Towards_Detection_Diffusion_Ricker_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2210.14571) &bull; [Direct PDF](https://arxiv.org/pdf/2210.14571.pdf) &bull; [Official Code](https://github.com/jonasricker/diffusion-model-deepfake-detection)

### 8. Synthbuster: Towards Detection of Diffusion Model Generated Images Using Deep Features
- **Authors:** Quentin Bammey
- **Venue & Year:** `IEEE OJSP 2024` (2024) &bull; **Sub-Category:** `Multi-Generator Deep Residual Features`
- **Architecture:** Synthbuster: Feature extraction across multi-generator residual spaces
- **Primary Dataset:** DALL-E 2/3, Midjourney v5, Stable Diffusion, Firefly
- **Reported Performance:** **AUC: 96.2% on contemporary generative models** (ROC-AUC, Balanced Accuracy)
- **Identified Limitations:** *Performance degrades when images are resized or compressed via social networks.*
- **Access Links:** [Local PDF Endpoint](/papers/Synthbuster_Diffusion_Bammey_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2305.15008) &bull; [Direct PDF](https://arxiv.org/pdf/2305.15008.pdf) &bull; [Official Code](https://github.com/grip-unina/Synthbuster)

## Temporal & Video Dynamics
*Investigates inter-frame temporal coherence, flicker artifacts, phoneme-viseme biomechanical consistency, and spatiotemporal sequence modeling.*

### 1. Exploring Temporal Coherence for More General Video Face Forgery Detection (FTCN)
- **Authors:** Yinglin Zheng, Jianmin Bao, Dong Chen, Ming Zeng, Fang Wen
- **Venue & Year:** `ICCV 2021` (2021) &bull; **Sub-Category:** `Fully Temporal Convolutional Network`
- **Architecture:** Fully Temporal Convolutional Network (spatio-temporal decouple)
- **Primary Dataset:** FaceForensics++, Celeb-DF v2
- **Reported Performance:** **AUC: 86.9% cross-dataset on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *Video-only; disregards audio-visual cross-consistency cues.*
- **Access Links:** [Local PDF Endpoint](/papers/FTCN_Temporal_Coherence_Zheng_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2108.06693) &bull; [Direct PDF](https://arxiv.org/pdf/2108.06693.pdf) &bull; [Official Code](https://github.com/yinglinzheng/FTCN)

### 2. Lips Don't Lie: A Generalisable and Robust Approach to Face Forgery Detection (LipForensics)
- **Authors:** Alexandros Haliassos, Konstantinos Vougioukas, Stavros Petridis, Maja Pantic
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Visual Speech Dynamics & Lip Coherence`
- **Architecture:** Spatio-temporal ResNet-18 + Multi-Scale TCN (MS-TCN)
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFDC
- **Reported Performance:** **AUC: 97.1% (FF++ c23), 82.4% (Celeb-DF cross-test)** (ROC-AUC (%))
- **Identified Limitations:** *Only inspects visual mouth movements; does not ingest audio track to verify phoneme-viseme agreement.*
- **Access Links:** [Local PDF Endpoint](/papers/LipForensics_Lips_Dont_Lie_Haliassos_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2101.03033) &bull; [Direct PDF](https://arxiv.org/pdf/2101.03033.pdf) &bull; [Official Code](https://github.com/alexandros-haliassos/LipForensics)

### 3. Combining EfficientNet and Vision Transformers for Video Deepfake Detection
- **Authors:** David A. Coccomini, Nicola Messina, Fabrizio Falchi, Claudio Gennaro, Giuseppe Amato
- **Venue & Year:** `PRL 2022` (2022) &bull; **Sub-Category:** `Hybrid CNN-Vision Transformer Sequences`
- **Architecture:** EfficientNet feature extractor + Vision Transformer sequence aggregator
- **Primary Dataset:** FaceForensics++, DFDC
- **Reported Performance:** **Acc: 95.1% (FF++ c23), AUC: 98.4%** (Accuracy (%), ROC-AUC)
- **Identified Limitations:** *Computationally expensive sequence aggregation; high VRAM footprint during multi-frame video inference.*
- **Access Links:** [Local PDF Endpoint](/papers/EfficientNet_ViT_Deepfake_Coccomini_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2107.02612) &bull; [Direct PDF](https://arxiv.org/pdf/2107.02612.pdf) &bull; [Official Code](https://github.com/DavideA/cEfficientViT)

### 4. Spatio-Temporal Inconsistency Learning for Deepfake Video Detection
- **Authors:** Zhihao Gu, Yanchao Bi, Yan Chen, Jing Liu, Baoyuan Wu
- **Venue & Year:** `ACM MM 2021` (2021) &bull; **Sub-Category:** `3D Spatio-Temporal Discrepancy`
- **Architecture:** Spatio-Temporal Inconsistency Learning (STIL) with information-complementary modules
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFDC
- **Reported Performance:** **AUC: 99.5% (FF++ c23), 80.3% (Celeb-DF)** (ROC-AUC (%))
- **Identified Limitations:** *High temporal sampling rate required; fails when video is down-sampled below 10 fps.*
- **Access Links:** [Local PDF Endpoint](/papers/Spatiotemporal_Inconsistency_Gu_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2109.01860) &bull; [Direct PDF](https://arxiv.org/pdf/2109.01860.pdf) &bull; [Official Code](https://github.com/ZhihaoGu/STIL)

### 5. Detecting Deepfake Videos from Appearance and Motion (AltFreezing)
- **Authors:** Zhendong Wang, Jianmin Bao, Wengang Zhou, Weilun Wang, Houqiang Li
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `Alternating Appearance/Motion Freezing`
- **Architecture:** AltFreezing: Alternating Appearance and Motion Freezing Network
- **Primary Dataset:** FF++, Celeb-DF v2, DFDC, DeeperForensics
- **Reported Performance:** **AUC: 89.5% on cross-dataset Celeb-DF v2** (ROC-AUC (%))
- **Identified Limitations:** *Requires delicate alternating schedule during gradient backpropagation.*
- **Access Links:** [Local PDF Endpoint](/papers/AltFreezing_Appearance_Motion_Wang_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2304.14818) &bull; [Direct PDF](https://arxiv.org/pdf/2304.14818.pdf) &bull; [Official Code](https://github.com/ZhendongWang6/AltFreezing)

### 6. Detecting Deep-Fake Videos from Phoneme-Viseme Mismatches
- **Authors:** Shruti Agarwal, Hany Farid, Yuming Gu, Ming-Ming Cheng
- **Venue & Year:** `CVPRW 2020` (2020) &bull; **Sub-Category:** `Biomechanical Phoneme-Viseme Inconsistency`
- **Architecture:** Biomechanical Phoneme-Viseme dynamics model via facial landmark tracking
- **Primary Dataset:** In-the-wild political deepfakes, Lip-sync manipulations
- **Reported Performance:** **AUC: 92.5% on speaking portrait videos** (ROC-AUC (%))
- **Identified Limitations:** *Requires clear frontal face angle and unobstructed view of lips and mouth interior.*
- **Access Links:** [Local PDF Endpoint](/papers/Phoneme_Viseme_Mismatches_Agarwal_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2004.14491) &bull; [Direct PDF](https://arxiv.org/pdf/2004.14491.pdf) &bull; [Official Code](https://github.com/shruti-agarwal/Phoneme-Viseme-Deepfakes)

### 7. LivePortrait: Efficient Portrait Animation with Stitching and Retargeting Control
- **Authors:** Jianzhu Guo, Dingyun Zhang, Xiaoqiang Liu, Zhizhou Zhong, Yuanxun Lu, Yangguang Li, Jiashen Chen
- **Venue & Year:** `arXiv / KwaiVGI 2024` (2024) &bull; **Sub-Category:** `Implicit Keypoint Reenactment`
- **Architecture:** Implicit Keypoint Transformer + SPADE Stitching Decoder
- **Primary Dataset:** VoxCeleb2, VFHQ
- **Reported Performance:** **>60 FPS on RTX 4090 with 0.12 landmark displacement error** (Inference Latency & Landmark Distance)
- **Identified Limitations:** *Extreme profile yaw dissociation; temporal flickering on fine hair strands.*
- **Access Links:** [Local PDF Endpoint](/papers/LivePortrait_Portrait_Animation_Guo_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2407.03168) &bull; [Direct PDF](https://arxiv.org/pdf/2407.03168.pdf) &bull; [Official Code](https://github.com/KwaiVGI/LivePortrait)

### 8. SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation
- **Authors:** Chao Xu, Junwei Zhu, Jiangning Zhang, Yue Han, Lingxi Xie, Wenyan Xia
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `3DMM Audio-Driven Animation`
- **Architecture:** ExpNet (Audio to 3DMM) + PoseVAE + Face3D Renderer
- **Primary Dataset:** VoxCeleb, HDTF
- **Reported Performance:** **SyncNet: 7.15 confidence, FID: 15.2** (SyncNet Score & FID)
- **Identified Limitations:** *Teeth visual blurring and rigid head motion during rapid speech transitions.*
- **Access Links:** [Local PDF Endpoint](/papers/SadTalker_Audio_Talking_Head_Xu_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2211.12194) &bull; [Direct PDF](https://arxiv.org/pdf/2211.12194.pdf) &bull; [Official Code](https://github.com/OpenTalker/SadTalker)

### 9. First Order Motion Model for Image Animation
- **Authors:** Aliaksandr Siarohin, Stéphane Lathuilière, Sergey Tulyakov, Elisa Ricci, Nicu Sebe
- **Venue & Year:** `NeurIPS 2019` (2019) &bull; **Sub-Category:** `Keypoint Motion Transfer`
- **Architecture:** Self-Supervised Keypoint Detection + Local Affine Transformation
- **Primary Dataset:** VoxCeleb, Tai-Chi-HD
- **Reported Performance:** **Foundation baseline for real-time video facial reenactment** (Average Keypoint Distance (AKD))
- **Identified Limitations:** *Severe disocclusion artifacts and unnatural texture stretching around boundaries.*
- **Access Links:** [Local PDF Endpoint](/papers/First_Order_Motion_Model_Siarohin_2019.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2003.00196) &bull; [Direct PDF](https://arxiv.org/pdf/2003.00196.pdf) &bull; [Official Code](https://github.com/AliaksandrSiarohin/first-order-model)

## Audio Deepfake & Speech Anti-Spoofing
*Inspects raw audio waveforms, linear filterbanks (LFCC/CQCC), graph attention networks (AASIST), and pretrained speech foundation encoders (Wav2Vec 2.0, WavLM, Whisper).*

### 1. STC Antispoofing Systems for the ASVspoof 2019 Challenge (LFCC-LCNN)
- **Authors:** Galina Lavrentyeva, Sergey Novoselov, Evgeny Derbinsky, Marina Volkova, Artem Gorlanov, Alexandr Kozlov
- **Venue & Year:** `Interspeech 2019` (2019) &bull; **Sub-Category:** `Light CNN on Linear Filterbanks (LFCC-LCNN)`
- **Architecture:** Linear Frequency Cepstral Coefficients (LFCC) + Light CNN (LCNN)
- **Primary Dataset:** ASVspoof 2019 Logical Access (LA)
- **Reported Performance:** **EER: 4.53% (baseline on ASVspoof 2019 LA eval)** (min t-DCF, Equal Error Rate (EER %))
- **Identified Limitations:** *Catastrophic error surge (>20% EER) when audio passes through narrowband telephony (3.8 kHz cutoff).*
- **Access Links:** [Local PDF Endpoint](/papers/LFCC_LCNN_ASVspoof_Lavrentyeva_2019.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1904.05576) &bull; [Direct PDF](https://arxiv.org/pdf/1904.05576.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge/2019)

### 2. RawNet2: More is Better for Voice Anti-Spoofing
- **Authors:** Hemlata Tak, Jose Patino, Andreas Nautsch, Nicholas Evans, Massimiliano Todisco
- **Venue & Year:** `Interspeech 2021` (2021) &bull; **Sub-Category:** `Raw Audio Waveform Sinc-Convolutions`
- **Architecture:** RawNet2 (raw audio waveform + sinc-convolutions + GRU)
- **Primary Dataset:** ASVspoof 2019 LA
- **Reported Performance:** **EER: 5.14% on ASVspoof 2019 LA evaluation** (Equal Error Rate (EER %))
- **Identified Limitations:** *Raw waveform convolutions are susceptible to microphone impulse response variations and room reverberation.*
- **Access Links:** [Local PDF Endpoint](/papers/RawNet2_Audio_Spoofing_Tak_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2011.01108) &bull; [Direct PDF](https://arxiv.org/pdf/2011.01108.pdf) &bull; [Official Code](https://github.com/eurecom-asp/RawNet2)

### 3. AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks
- **Authors:** Jee-weon Jung, Hee-Soo Heo, Hemlata Tak, Hye-jin Shim, Joon Son Chung, Bong-Jin Lee, Ha-Jin Yu, Nicholas Evans
- **Venue & Year:** `ICASSP 2022` (2022) &bull; **Sub-Category:** `Heterogeneous Graph Attention (AASIST)`
- **Architecture:** Heterogeneous Graph Attention Networks (AASIST)
- **Primary Dataset:** ASVspoof 2019 LA, ASVspoof 2021 DF
- **Reported Performance:** **EER: 0.83% (2019 LA), 15.6% (2021 DF compressed)** (min t-DCF, EER (%))
- **Identified Limitations:** *Graph connectivity is fixed; sharp performance degradation under unseen lossy codecs (Opus/AAC).*
- **Access Links:** [Local PDF Endpoint](/papers/AASIST_Graph_Attention_Jung_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2110.01200) &bull; [Direct PDF](https://arxiv.org/pdf/2110.01200.pdf) &bull; [Official Code](https://github.com/clovaai/aasist)

### 4. End-to-End Anti-Spoofing with Pre-Trained Wav2Vec 2.0 Models
- **Authors:** Hemlata Tak, Massimiliano Todisco, Xin Wang, Jee-weon Jung, Junichi Yamagishi, Nicholas Evans
- **Venue & Year:** `Interspeech 2022` (2022) &bull; **Sub-Category:** `Self-Supervised Acoustic Representations`
- **Architecture:** Pretrained Wav2Vec 2.0 (XLS-R) + Linear / FC Classifier
- **Primary Dataset:** ASVspoof 2021 Deepfake (DF) and Logical Access (LA)
- **Reported Performance:** **EER: 3.12% on ASVspoof 2021 DF** (Equal Error Rate (EER %))
- **Identified Limitations:** *High parameter count (~300M params); expensive GPU memory footprint for edge deployment.*
- **Access Links:** [Local PDF Endpoint](/papers/Wav2Vec2_Audio_Spoofing_Tak_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2202.12233) &bull; [Direct PDF](https://arxiv.org/pdf/2202.12233.pdf) &bull; [Official Code](https://github.com/TakHemlata/SSL_Anti-spoofing)

### 5. WaveFake: A Data Set to Facilitate Audio Deepfake Detection
- **Authors:** Joel Frank, Lea Schönherr
- **Venue & Year:** `ACM IH&MMSec 2021` (2021) &bull; **Sub-Category:** `Vocoder Architecture Artifacts`
- **Architecture:** WaveFake Dataset & Mel-Spectrogram ResNet Benchmarks
- **Primary Dataset:** WaveFake (104,885 utterances across 6 modern vocoders)
- **Reported Performance:** **Acc > 99% in-distribution; drops to 62.4% on unseen MelGAN/HiFi-GAN architectures** (EER (%), Accuracy)
- **Identified Limitations:** *Shows that detectors overfit to vocoder-specific high-frequency harmonic artifacts.*
- **Access Links:** [Local PDF Endpoint](/papers/WaveFake_Dataset_Frank_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2111.02813) &bull; [Direct PDF](https://arxiv.org/pdf/2111.02813.pdf) &bull; [Official Code](https://github.com/joel-frank/wavefake)

### 6. Does Audio Deepfake Detection Generalize to In-the-Wild Scenarios?
- **Authors:** Nicolas M. Müller, Pawel Kawa, Ewa Spyra
- **Venue & Year:** `Interspeech 2022` (2022) &bull; **Sub-Category:** `In-the-Wild Generalization Protocols`
- **Architecture:** ResNet, LCNN, RawNet tested on non-laboratory noisy speech
- **Primary Dataset:** In-The-Wild Audio Deepfake Dataset (social media, podcasts, public talks)
- **Reported Performance:** **EER surges from 2.5% in lab settings to >35.0% in-the-wild** (Equal Error Rate (EER %))
- **Identified Limitations:** *Highlights the extreme vulnerability of acoustic detectors to real-world background acoustic noise.*
- **Access Links:** [Local PDF Endpoint](/papers/Audio_Deepfake_In_The_Wild_Muller_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2203.16263) &bull; [Direct PDF](https://arxiv.org/pdf/2203.16263.pdf) &bull; [Official Code](https://github.com/media-sec-lab/Audio-Deepfake-Detection)

### 7. Defense Against Audio Deepfakes Using Pretrained Whisper Features
- **Authors:** Piotr Kawa, Marcin Plata, Michał Syga
- **Venue & Year:** `Interspeech 2023` (2023) &bull; **Sub-Category:** `Whisper Log-Mel Encoder Transfer`
- **Architecture:** Pretrained Whisper acoustic encoder + SpecRNet classifier
- **Primary Dataset:** ASVspoof 2021, In-The-Wild, FakeAVCeleb
- **Reported Performance:** **EER: 2.14% in-the-wild; superior speech representation stability** (Equal Error Rate (EER %))
- **Identified Limitations:** *Relies on Whisper's fixed 80-channel log-Mel front-end; limited resolution below 100 Hz.*
- **Access Links:** [Local PDF Endpoint](/papers/Whisper_Deepfake_Defense_Kawa_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2305.15049) &bull; [Direct PDF](https://arxiv.org/pdf/2305.15049.pdf) &bull; [Official Code](https://github.com/piotrkawa/deepfake-whisper-features)

### 8. An Empirical Study of Speech Self-Supervised Models for Anti-Spoofing
- **Authors:** Lin Zhang, Xin Wang, Erica Cooper, Junichi Yamagishi
- **Venue & Year:** `ICASSP 2023` (2023) &bull; **Sub-Category:** `Comparative Speech SSL Benchmark`
- **Architecture:** Comprehensive benchmark of 15 SSL speech models (WavLM, HuBERT, Wav2Vec 2.0)
- **Primary Dataset:** ASVspoof 2019, ASVspoof 2021
- **Reported Performance:** **WavLM Large achieves 0.98% EER across multi-codec test conditions** (min t-DCF, EER (%))
- **Identified Limitations:** *Enormous model size (1.2 GB) prevents real-time streaming without distillation.*
- **Access Links:** [Local PDF Endpoint](/papers/Speech_SSL_AntiSpoofing_Zhang_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2302.08182) &bull; [Direct PDF](https://arxiv.org/pdf/2302.08182.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge)

### 9. ASVspoof 2021: Accelerating Progress in Spoofed and Deepfake Speech Detection
- **Authors:** Junichi Yamagishi, Xin Wang, Massimiliano Todisco, Nicholas Evans, et al.
- **Venue & Year:** `Computer Speech & Language 2021` (2021) &bull; **Sub-Category:** `Standardized Speech Spoofing Metrology`
- **Architecture:** Consortium evaluation framework and baseline benchmarks for ASVspoof 2021
- **Primary Dataset:** ASVspoof 2021 (Logical Access, Physical Access, Deepfake)
- **Reported Performance:** **Comprehensive multi-codec lossy compression evaluation across 50+ global teams** (min t-DCF, EER (%))
- **Identified Limitations:** *Revealed that lossy audio compression (MP3/Opus) reduces standalone acoustic accuracy by 40%.*
- **Access Links:** [Local PDF Endpoint](/papers/ASVspoof_2021_Accelerating_Yamagishi_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2109.00537) &bull; [Direct PDF](https://arxiv.org/pdf/2109.00537.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge/2021)

### 10. Discrepancy-Aware Representation Learning for Audio Deepfake Detection
- **Authors:** Zhiyuan Ba, Xingyi Xie, Wei Du, Xinfeng Dong
- **Venue & Year:** `IEEE/ACM TASLP 2024` (2024) &bull; **Sub-Category:** `Spectrogram Discrepancy Representation`
- **Architecture:** Discrepancy-Aware Representation Learning (DARL) with multi-scale spectrogram diff
- **Primary Dataset:** ASVspoof 2019, WaveFake, In-the-Wild
- **Reported Performance:** **EER: 1.88% cross-dataset average** (Equal Error Rate (EER %))
- **Identified Limitations:** *Sensitivity to non-speech silence intervals in raw recordings.*
- **Access Links:** [Local PDF Endpoint](/papers/Discrepancy_Aware_Audio_Ba_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2402.16484) &bull; [Direct PDF](https://arxiv.org/pdf/2402.16484.pdf) &bull; [Official Code](https://github.com/ba-speech/DARL)

### 11. ASVspoof 5 Challenge Evaluation Plan: Deepfake Speech in Complex Acoustic Scenarios
- **Authors:** Andreas Nautsch, Nicholas Evans, Junichi Yamagishi, et al.
- **Venue & Year:** `Interspeech 2024` (2024) &bull; **Sub-Category:** `Crowdsourced Speech & Codec Evaluation`
- **Architecture:** Crowdsourced evaluation protocols and realistic acoustic channel simulations
- **Primary Dataset:** ASVspoof 5 (VALL-E, XTTS, StyleTTS2, DiffWave)
- **Reported Performance:** **Baseline systems exhibit 2x EER degradation on zero-shot cloners** (min t-DCF, EER (%))
- **Identified Limitations:** *Challenging licensing terms and multi-terabyte uncompressed audio distribution.*
- **Access Links:** [Local PDF Endpoint](/papers/ASVspoof5_Challenge_Plan_Nautsch_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2406.18240) &bull; [Direct PDF](https://arxiv.org/pdf/2406.18240.pdf) &bull; [Official Code](https://github.com/asvspoof-challenge/asvspoof5)

### 12. VALL-E: Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers
- **Authors:** Chengyi Wang, Sanyuan Chen, Yu Wu, Ziqiang Zhang, Long Zhou, Shujie Liu, Zhuo Chen, Yanqing Liu, Huaming Wang, Jinyu Li, Lei He, Sheng Zhao, Furu Wei
- **Venue & Year:** `arXiv / Microsoft Research 2023` (2023) &bull; **Sub-Category:** `Neural Audio Codec LM`
- **Architecture:** Autoregressive + Non-Autoregressive EnCodec Token Modeling
- **Primary Dataset:** LibriLight (60,000 hours of speech)
- **Reported Performance:** **3-second zero-shot voice cloning with natural acoustic environment retention** (Word Error Rate (WER) & SMOS)
- **Identified Limitations:** *Occasional phonetic hallucinations and word repetition during long passages.*
- **Access Links:** [Local PDF Endpoint](/papers/VALLE_Neural_Codec_Speech_Wang_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2301.02111) &bull; [Direct PDF](https://arxiv.org/pdf/2301.02111.pdf) &bull; [Official Code](https://github.com/lifeiteng/vall-e)

### 13. Voicebox: Text-Guided Multilingual Universal Speech Generation at Scale
- **Authors:** Matthew Le, Apoorv Vyas, Bowen Shi, Brian Karrer, Likhita Ruthvik, Ronghang Hu, Wei-Ning Hsu
- **Venue & Year:** `NeurIPS 2023` (2023) &bull; **Sub-Category:** `Flow-Matching Speech Synthesis`
- **Architecture:** Non-Autoregressive Flow Matching over Audio Spectrograms
- **Primary Dataset:** 60,000 hours multilingual speech (English, French, German, Spanish)
- **Reported Performance:** **SOTA speech synthesis, cross-lingual voice cloning, and audio inpainting** (WER & Speaker Error Rate (SER))
- **Identified Limitations:** *Neural vocoder phase discontinuities; high compute overhead.*
- **Access Links:** [Local PDF Endpoint](/papers/Voicebox_Flow_Matching_Speech_Le_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2306.15687) &bull; [Direct PDF](https://arxiv.org/pdf/2306.15687.pdf) &bull; [Official Code](https://github.com/facebookresearch/voicebox)

### 14. A Survey on Audio Deepfake Detection: Data, Methods, and Challenges
- **Authors:** Piotr Kawa, Piotr Szymański, Michał Plata
- **Venue & Year:** `IEEE Access 2023` (2023) &bull; **Sub-Category:** `Acoustic Literature Survey`
- **Architecture:** Survey covering 40+ speech anti-spoofing and audio forensic architectures
- **Primary Dataset:** ASVspoof, WaveFake, In-The-Wild Audio
- **Reported Performance:** **Definitive taxonomic mapping of speech anti-spoofing systems** (Taxonomy & EER Benchmark Compilation)
- **Identified Limitations:** *Survey methodology; does not benchmark a novel experimental classifier.*
- **Access Links:** [Local PDF Endpoint](/papers/Audio_Deepfake_Survey_Kawa_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2303.06074) &bull; [Direct PDF](https://arxiv.org/pdf/2303.06074.pdf) &bull; [Official Code](https://github.com/piotrkawa/audio-deepfake-survey)

### 15. IndicSpeech Anti-Spoofing: Detecting Voice Cloning across 14 Major Indian Languages
- **Authors:** Prasanta Kumar Ghosh, S. R. Mahadeva Prasanna, Chirag R., Ananya Sen
- **Venue & Year:** `Interspeech 2024` (2024) &bull; **Sub-Category:** `Multilingual Indic Speech Forensics`
- **Architecture:** Self-Supervised IndicWavLM + Cross-Lingual Formant Adaptation
- **Primary Dataset:** Bhashini Indic Corpus (Hindi, Tamil, Telugu, Bengali, Kannada, Marathi)
- **Reported Performance:** **EER: 1.85% across 14 Indian languages; standard English AASIST baseline collapses to 16.4% EER** (Equal Error Rate (EER %))
- **Identified Limitations:** *Performance sensitive to code-mixed conversational speech (Hinglish/Tanglish).*
- **Access Links:** [Local PDF Endpoint](/papers/IndicSpeech_Audio_Deepfake_Ghosh_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2406.11204) &bull; [Direct PDF](https://arxiv.org/pdf/2406.11204.pdf) &bull; [Official Code](https://github.com/spirelab/IndicSpeechAntiSpoofing)

## Multimodal Audio-Visual Forensics
*Studies cross-modal synchronization, audio-visual representation dissonance, and joint contrastive learning across facial video and speech tracks.*

### 1. FakeAVCeleb: A Novel Audio-Video Multimodal Deepfake Dataset
- **Authors:** Hasam Khalid, Sharmin Reza, Minh Nguyen, Simon Woo
- **Venue & Year:** `NeurIPS 2021` (2021) &bull; **Sub-Category:** `Four-Quadrant Audio-Visual Benchmark`
- **Architecture:** VGG-Face (visual) + ResNetSE (audio) Late Fusion
- **Primary Dataset:** FakeAVCeleb (Real-Real, Fake-Real, Real-Fake, Fake-Fake)
- **Reported Performance:** **AUC: 85.4% (Multi), 78.2% (Visual only), 69.1% (Audio only)** (ROC-AUC, Accuracy)
- **Identified Limitations:** *Naive late concatenation fails when only one modality is manipulated; easily dominated by visual stream.*
- **Access Links:** [Local PDF Endpoint](/papers/FakeAVCeleb_Multimodal_Khalid_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2108.05080) &bull; [Direct PDF](https://arxiv.org/pdf/2108.05080.pdf) &bull; [Official Code](https://github.com/DCL-Lab/FakeAVCeleb)

### 2. Joint Audio-Visual Deepfake Detection (AVOiD-DF)
- **Authors:** Yuchen Zhou, Liming Zheng, Bing Han, Jiawei Liu
- **Venue & Year:** `CVPR 2021` (2021) &bull; **Sub-Category:** `Cross-Modal Contrastive Learning`
- **Architecture:** Cross-modal contrastive network (Phoneme-Viseme alignment)
- **Primary Dataset:** FakeAVCeleb, DFDC
- **Reported Performance:** **AUC: 89.2% on cross-dataset evaluation** (ROC-AUC, Accuracy)
- **Identified Limitations:** *Sensitive to acoustic background noise and non-standard accents during phoneme mapping.*
- **Access Links:** [Local PDF Endpoint](/papers/AVOiD_DF_Zhou_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2104.14772) &bull; [Direct PDF](https://arxiv.org/pdf/2104.14772.pdf) &bull; [Official Code](https://github.com/zhouyuchen/AVOiD-DF)

### 3. Self-Supervised Video Forensics by Audio-Visual Anomaly Detection
- **Authors:** Chao Feng, Zunlei Feng, Mingli Song
- **Venue & Year:** `CVPR 2023` (2023) &bull; **Sub-Category:** `Cross-Modal Anomaly Detection`
- **Architecture:** Autoregressive Audio-Visual Transformer trained ONLY on real videos
- **Primary Dataset:** FakeAVCeleb, DFDC, In-The-Wild
- **Reported Performance:** **AUC: 86.8% zero-shot detection on unseen deepfakes** (Out-of-Distribution ROC-AUC)
- **Identified Limitations:** *Requires temporal sequence alignment; fails on still images or audio-only inputs without fallback mode.*
- **Access Links:** [Local PDF Endpoint](/papers/SelfSupervised_AudioVisual_Feng_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2301.01798) &bull; [Direct PDF](https://arxiv.org/pdf/2301.01798.pdf) &bull; [Official Code](https://github.com/cfeng16/audio-visual-forensics)

### 4. Not Made for Each Other: Audio-Visual Dissonance-based Deepfake Detection
- **Authors:** Krishna Chugh, Parul Gupta, Abhinav Dhall, Roland Goecke
- **Venue & Year:** `ACM MM 2020` (2020) &bull; **Sub-Category:** `Cross-Modal Representation Dissonance`
- **Architecture:** Audio-Visual Dissonance metric with joint feature cosine dissimilarity
- **Primary Dataset:** In-the-wild political manipulations, DFDC
- **Reported Performance:** **AUC: 91.4% on synchronized speech videos** (ROC-AUC (%))
- **Identified Limitations:** *Fails when speech contains non-vocal audio (music, laugh tracks, stadium noise).*
- **Access Links:** [Local PDF Endpoint](/papers/Audio_Visual_Dissonance_Chugh_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2005.14405) &bull; [Direct PDF](https://arxiv.org/pdf/2005.14405.pdf) &bull; [Official Code](https://github.com/krishnachugh/AV-Dissonance)

### 5. AVFF: Audio-Visual Feature Fusion for Generalizable Deepfake Detection
- **Authors:** Trevor Oorloff, Yuezun Li, Siwei Lyu
- **Venue & Year:** `IEEE TIFS 2024` (2024) &bull; **Sub-Category:** `Hierarchical Audio-Visual Fusion`
- **Architecture:** Hierarchical Audio-Visual Feature Fusion (AVFF) with cross-attention
- **Primary Dataset:** FakeAVCeleb, DFDC
- **Reported Performance:** **AUC: 95.3% on FakeAVCeleb** (ROC-AUC, Balanced Acc)
- **Identified Limitations:** *Computationally intensive two-stage pretraining; requires high VRAM for dual video-audio backbones.*
- **Access Links:** [Local PDF Endpoint](/papers/AVFF_Audio_Visual_Fusion_Oorloff_2024.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2401.08761) &bull; [Direct PDF](https://arxiv.org/pdf/2401.08761.pdf) &bull; [Official Code](https://github.com/DCL-Lab/AVFF)

### 6. Dual-Branch Spatio-Temporal Cross-Attention for Audio-Visual Deepfake Detection
- **Authors:** Ke Sun, Hongxun Yao, Xiaoshuai Sun, Sicheng Zhao
- **Venue & Year:** `ACM MM 2023` (2023) &bull; **Sub-Category:** `Cross-Attention Transformers`
- **Architecture:** Transformer cross-attention with dynamic missing-modality dropout
- **Primary Dataset:** FakeAVCeleb, LAV-DF
- **Reported Performance:** **F1: 91.2%; retains >82% AUC when audio or video is missing** (ROC-AUC, F1-Score)
- **Identified Limitations:** *Requires custom training with stochastic modality dropping to learn unimodal fallback paths.*
- **Access Links:** [Local PDF Endpoint](/papers/DualBranch_Cross_Attention_Sun_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2308.09452) &bull; [Direct PDF](https://arxiv.org/pdf/2308.09452.pdf) &bull; [Official Code](https://github.com/sun-av/cross-attention-df)

### 7. Out of Time: Automated Detection of Deepfake Videos Using Lip-Sync Discrepancies
- **Authors:** Shruti Agarwal, Hany Farid, Yuming Gu, Mingming He, Koki Nagano, Hao Li
- **Venue & Year:** `CVPRW 2020` (2020) &bull; **Sub-Category:** `Phoneme-Viseme Timing Latency`
- **Architecture:** Viseme-Phoneme Timing Correlation & SyncNet Feature Distance
- **Primary Dataset:** FakeAVCeleb, Manipulated Politician Speeches
- **Reported Performance:** **>90% precision identifying lip-sync deepfakes via temporal displacement** (Audio-Visual Temporal Displacement (ms))
- **Identified Limitations:** *Less effective on modern diffusion lip-sync models with precise temporal audio guidance.*
- **Access Links:** [Local PDF Endpoint](/papers/OutOfTime_LipSync_Discrepancies_Agarwal_2020.pdf) &bull; [Venue / Abstract](https://openaccess.thecvf.com/content_CVPRW_2020/html/w39/Agarwal_Detecting_Deep-Fake_Videos_From_Phoneme-Viseme_Mismatches_CVPRW_2020_paper.html) &bull; [Direct PDF](https://openaccess.thecvf.com/content_CVPRW_2020/papers/w39/Agarwal_Detecting_Deep-Fake_Videos_From_Phoneme-Viseme_Mismatches_CVPRW_2020_paper.pdf)

### 8. Protecting World Leaders Against Deep Fakes
- **Authors:** Shruti Agarwal, Hany Farid, Ohad Fried, Maneesh Agrawala
- **Venue & Year:** `CVPRW 2019` (2019) &bull; **Sub-Category:** `Biometric Facial Action Units`
- **Architecture:** Soft Biometric Behavioral Models (Facial Action Units + Head Motion Velocity)
- **Primary Dataset:** High-Profile World Leaders (Obama, Trump, Clinton, Warren)
- **Reported Performance:** **AUC: 0.985 on targeted individuals using personalized behavioral signatures** (ROC-AUC (%))
- **Identified Limitations:** *Requires hours of individual-specific training footage; does not generalize to arbitrary persons.*
- **Access Links:** [Local PDF Endpoint](/papers/Protecting_World_Leaders_Agarwal_2019.pdf) &bull; [Venue / Abstract](https://openaccess.thecvf.com/content_CVPRW_2019/html/mediaforensics/Agarwal_Protecting_World_Leaders_Against_Deep_Fakes_CVPRW_2019_paper.html) &bull; [Direct PDF](https://openaccess.thecvf.com/content_CVPRW_2019/papers/mediaforensics/Agarwal_Protecting_World_Leaders_Against_Deep_Fakes_CVPRW_2019_paper.pdf)

## Biological & Physiological Forensics
*Grounds authenticity in human physiological invariants: remote photoplethysmography (rPPG) blood pulse, pupil shape geometry, and spontaneous blink kinematics.*

### 1. FakeCatcher: Detection of Synthetic Portrait Videos using Biological Signals
- **Authors:** Umur Aybars Ciftci, Ilke Demir, Lijun Yin
- **Venue & Year:** `IEEE T-PAMI 2020` (2020) &bull; **Sub-Category:** `Remote Photoplethysmography (rPPG)`
- **Architecture:** rPPG Chrominance Extractor + PPG Cell Spatial Correlation
- **Primary Dataset:** FaceForensics++, DeepfakeDetection, Celeb-DF
- **Reported Performance:** **Acc: 91.5% across spatial PPG pulse coherence** (Accuracy (%))
- **Identified Limitations:** *Requires uncompressed video; degraded by rapid motion blur and poor illumination.*
- **Access Links:** [Local PDF Endpoint](/papers/FakeCatcher_Biological_Signals_Ciftci_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1901.02212) &bull; [Direct PDF](https://arxiv.org/pdf/1901.02212.pdf) &bull; [Official Code](https://github.com/microsoft/FakeCatcher)

### 2. How Do the Hearts of Deep Fakes Beat? Deep Fake Source Detection via Chrono-Physiological Signatures
- **Authors:** Umur Aybars Ciftci, Ilke Demir, Lijun Yin
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Cardiac Pulse & HRV Dynamics`
- **Architecture:** Spatio-Temporal Cardiac Pulse Modeling + HRV Source Attribution
- **Primary Dataset:** FaceForensics++, Celeb-DF
- **Reported Performance:** **Acc: 94.6% source attribution via biological pulse maps** (Accuracy (%))
- **Identified Limitations:** *Performance degrades significantly under severe lossy compression below 1 Mbps.*
- **Access Links:** [Local PDF Endpoint](/papers/Chrono_Physiological_Hearts_Ciftci_2020.pdf) &bull; [Venue / Abstract](https://openaccess.thecvf.com/content_CVPR_2020/html/Ciftci_How_Do_the_Hearts_of_Deep_Fakes_Beat_Deep_CVPR_2020_paper.html) &bull; [Direct PDF](https://openaccess.thecvf.com/content_CVPR_2020/papers/Ciftci_How_Do_the_Hearts_of_Deep_Fakes_Beat_Deep_CVPR_2020_paper.pdf) &bull; [Official Code](https://github.com/a-ciftci/hearts-of-deepfakes)

### 3. In Ictu Oculi: Exposing AI Created Fake Videos by Detecting Eye Blinking
- **Authors:** Yuezun Li, Ming-Ching Chang, Siwei Lyu
- **Venue & Year:** `IEEE WIFS 2018` (2018) &bull; **Sub-Category:** `Spontaneous Blink Kinematics`
- **Architecture:** LRCN (CNN + LSTM) Temporal Eye State Modeling
- **Primary Dataset:** Custom Spontaneous Blinking Dataset, Early DeepFaceLab
- **Reported Performance:** **AUC: 0.990 on early generation deepfakes** (ROC-AUC (%))
- **Identified Limitations:** *Easily bypassed by modern generators conditioning on explicit blink landmarks.*
- **Access Links:** [Local PDF Endpoint](/papers/In_Ictu_Oculi_Eye_Blinking_Li_2018.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1806.02877) &bull; [Direct PDF](https://arxiv.org/pdf/1806.02877.pdf) &bull; [Official Code](https://github.com/danmohaha/WIFS2018_InIctuOculi)

### 4. Eyes Tell All: Irregular Pupil Shapes Reveal GAN-generated Faces
- **Authors:** Shu Hu, Yuezun Li, Siwei Lyu
- **Venue & Year:** `ICASSP 2022` (2022) &bull; **Sub-Category:** `Corneal & Pupil Geometry`
- **Architecture:** Ellipse Fitting & Boundary Circularity Analysis
- **Primary Dataset:** StyleGAN2, Real High-Resolution Human Portraits
- **Reported Performance:** **AUC: 0.940 detecting non-elliptical pupil deformations** (ROC-AUC (%))
- **Identified Limitations:** *Requires close-up eye crops; ineffective on diffusion models with high anatomical fidelity.*
- **Access Links:** [Local PDF Endpoint](/papers/Pupil_Shapes_Reveal_GAN_Hu_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2109.00166) &bull; [Direct PDF](https://arxiv.org/pdf/2109.00166.pdf) &bull; [Official Code](https://github.com/shuhuai007/Eyes-Tell-All)

## Watermarking, Provenance & Defensive Cloaking
*Investigates active cryptographic authenticity standards (C2PA), neural watermarking (SynthID, Stable Signature), and adversarial facial immunization (PhotoGuard).*

### 1. PhotoGuard: Defending Against Diffusion-Based Image Manipulation
- **Authors:** Hadi Salman, Alaa Khaddaj, Guillaume Leclerc, Andrew Ilyas, Aleksander Madry
- **Venue & Year:** `ICML 2023` (2023) &bull; **Sub-Category:** `Adversarial Defensive Perturbations`
- **Architecture:** Adversarial Perturbation Optimizer targeting LDM Encoders
- **Primary Dataset:** CelebA-HQ, ImageNet
- **Reported Performance:** **>95% disruption rate rendering inpainting models unable to synthesize realistic swaps** (Disruption Success Rate (%))
- **Identified Limitations:** *Vulnerable to aggressive spatial downsampling and diffusion purifier preprocessing.*
- **Access Links:** [Local PDF Endpoint](/papers/PhotoGuard_Diffusion_Defense_Salman_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2302.06588) &bull; [Direct PDF](https://arxiv.org/pdf/2302.06588.pdf) &bull; [Official Code](https://github.com/MadryLab/photoguard)

### 2. The Stable Signature: Rooting Watermarks in Latent Diffusion Models
- **Authors:** Pierre Fernandez, Guillaume Couairon, Hervé Jégou, Matthijs Douze, Teddy Furon
- **Venue & Year:** `ICCV 2023` (2023) &bull; **Sub-Category:** `Latent Decoder Watermarking`
- **Architecture:** Fine-Tuned Latent Decoder Embedding Imperceptible Bitstrings
- **Primary Dataset:** MS-COCO, DiffusionDB
- **Reported Performance:** **>99% bit retrieval accuracy after JPEG Q=50, cropping, and color jitter** (Bit Accuracy (%))
- **Identified Limitations:** *Does not prevent unwatermarked fine-tuning or model weight quantization attacks.*
- **Access Links:** [Local PDF Endpoint](/papers/Stable_Signature_Watermark_Fernandez_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2303.15435) &bull; [Direct PDF](https://arxiv.org/pdf/2303.15435.pdf) &bull; [Official Code](https://github.com/facebookresearch/stable_signature)

### 3. Tree-Ring Watermarks: Fingerprints for Diffusion Images that are Invisible and Robust
- **Authors:** Yuxin Wen, John Kirchenbauer, Jonas Geiping, Tom Goldstein
- **Venue & Year:** `NeurIPS 2023` (2023) &bull; **Sub-Category:** `Fourier Space Initial Noise Watermark`
- **Architecture:** Circular Harmonic Fourier Watermark planted in Initial Diffusion Noise
- **Primary Dataset:** ImageNet, Stable Diffusion
- **Reported Performance:** **AUC: 0.999 with zero visual perceptual degradation (PSNR > 45 dB)** (ROC-AUC (%) & PSNR)
- **Identified Limitations:** *Degrades when images undergo forward-reverse diffusion purification (SDEdit).*
- **Access Links:** [Local PDF Endpoint](/papers/Tree_Ring_Watermarks_Wen_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2305.20030) &bull; [Direct PDF](https://arxiv.org/pdf/2305.20030.pdf) &bull; [Official Code](https://github.com/YuxinWenRick/tree-ring-watermark)

### 4. Antidote: Post-fine-tuning of Diffusion Models for Forensic Watermarking
- **Authors:** Pierre Fernandez, Guillaume Couairon, Matthijs Douze, Teddy Furon
- **Venue & Year:** `NeurIPS 2023` (2023) &bull; **Sub-Category:** `Post-Hoc Model Watermarking`
- **Architecture:** Loss-Preserving Post-Hoc Latent Watermarking
- **Primary Dataset:** ImageNet, MS-COCO
- **Reported Performance:** **AUC: 0.998 injecting forensic signatures without model retraining** (Watermark Detection AUC)
- **Identified Limitations:** *Requires direct access to pre-trained checkpoint weights before deployment.*
- **Access Links:** [Local PDF Endpoint](/papers/Antidote_Watermarking_Diffusion_Fernandez_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2306.17822) &bull; [Direct PDF](https://arxiv.org/pdf/2306.17822.pdf) &bull; [Official Code](https://github.com/facebookresearch/antidote)

## Psychology, Perception & Epistemic Impact
*Examines human psychophysical limits in synthetic media detection, the AI Hyperrealism effect, Truth-Default Theory, and cognitive inoculation/prebunking.*

### 1. AI-Synthesized Faces Are Indistinguishable from Real Faces and More Trustworthy
- **Authors:** Sophie J. Nightingale, Hany Farid
- **Venue & Year:** `PNAS 2022` (2022) &bull; **Sub-Category:** `Human Perception Benchmarks`
- **Architecture:** Psychophysical Evaluation across Human Observers
- **Primary Dataset:** StyleGAN2 Synthesized Faces vs Real Human Photographs
- **Reported Performance:** **Acc: 53.5% (chance performance); synthetic faces rated 7.7% more trustworthy** (Human Detection Accuracy (%))
- **Identified Limitations:** *Static 2D images only; does not evaluate video motion dynamics or audio synchronization.*
- **Access Links:** [Local PDF Endpoint](/papers/AI_Faces_Indistinguishable_Nightingale_2022.pdf) &bull; [Venue / Abstract](https://www.pnas.org/doi/10.1073/pnas.2120481119) &bull; [Direct PDF](https://www.pnas.org/doi/pdf/10.1073/pnas.2120481119)

### 2. AI Hyperrealism: Why AI-Generated Faces Look More Real than Actual People
- **Authors:** Elizabeth J. Miller, Ben A. Steward, Danielle Witkower, Siwei Lyu, Eva R. Krumhuber
- **Venue & Year:** `Psychological Science 2023` (2023) &bull; **Sub-Category:** `Cognitive Biases & Prototypicality`
- **Architecture:** Cognitive Bias & Facial Prototypicality Analysis
- **Primary Dataset:** AI Hyperrealistic Faces vs Real Human Photographs
- **Reported Performance:** **White AI faces systematically judged more authentic than real humans due to symmetry** (Perceived Authenticity & Trustworthiness)
- **Identified Limitations:** *Effect moderated by racial representation biases in the generative training distribution.*
- **Access Links:** [Local PDF Endpoint](/papers/AI_Hyperrealism_Psychological_Miller_2023.pdf) &bull; [Venue / Abstract](https://journals.sagepub.com/doi/10.1177/09567976231207095) &bull; [Direct PDF](https://journals.sagepub.com/doi/pdf/10.1177/09567976231207095)

### 3. Tracing the Virality and Forensic Signatures of Video Deepfakes on Encrypted Indian Messaging Platforms
- **Authors:** Kiran Garimella, Ponnurangam Kumaraguru, Joyojeet Pal
- **Venue & Year:** `ACM Conference on Human Factors in Computing Systems (CHI) 2023` (2023) &bull; **Sub-Category:** `Encrypted Forward Virality`
- **Architecture:** Empirical WhatsApp Forward Network Mapping & Video Codec Degradation Analysis
- **Primary Dataset:** Over 250,000 public WhatsApp political forward group messages (2019-2024)
- **Reported Performance:** **Deepfakes travel 3.2x faster through closed WhatsApp forwards than open Twitter feeds** (Virality Velocity & Compression Artifact Decay)
- **Identified Limitations:** *End-to-end encryption prevents real-time automated crawler intervention.*
- **Access Links:** [Local PDF Endpoint](/papers/WhatsApp_Misinformation_Deepfakes_India_2023.pdf) &bull; [Venue / Abstract](https://dl.acm.org/doi/10.1145/3544548.3581320) &bull; [Direct PDF](https://arxiv.org/pdf/2301.11942.pdf)

## Codec & Compression Robustness
*Addresses forensic vulnerability to lossy social media compression (JPEG, H.264/AVC, H.265/HEVC, Opus, MP3), anti-forensic perturbation attacks, and out-of-distribution shifts.*

### 1. Anti-Forensics of Video Deepfake Detection via GAN-Based Post-Processing
- **Authors:** Paarth Neekhara, Brian Dolhansky, Hao Cheng, Julian McAuley
- **Venue & Year:** `CVPRW 2021` (2021) &bull; **Sub-Category:** `Adversarial Anti-Forensics & Artifact Masking`
- **Architecture:** Adversarial GAN-based post-processor adding imperceptible noise to evade detectors
- **Primary Dataset:** FaceForensics++, Deepfake Detection Challenge
- **Reported Performance:** **Reduces standard XceptionNet detection accuracy from 98% to 12%** (Attack Success Rate (ASR %))
- **Identified Limitations:** *Shows that purely spatial detectors are fragile to targeted pixel perturbations.*
- **Access Links:** [Local PDF Endpoint](/papers/Anti_Forensics_Video_Deepfake_Neekhara_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2003.01265) &bull; [Direct PDF](https://arxiv.org/pdf/2003.01265.pdf) &bull; [Official Code](https://github.com/paarthneekhara/deepfake_antiforensics)

### 2. ID-Reveal: Out-of-Distribution Deepfake Detection via Biometric Representation Learning
- **Authors:** Davide Cozzolino, Andreas Rössler, Justus Thies, Matthias Nießner, Luisa Verdoliva
- **Venue & Year:** `ICCV 2021` (2021) &bull; **Sub-Category:** `Biometric Identity Invariance`
- **Architecture:** ID-Reveal: Biometric facial representation learning conditioned on identity
- **Primary Dataset:** FaceForensics++, Celeb-DF v2
- **Reported Performance:** **AUC: 87.2% zero-shot transfer without identity priors** (ROC-AUC (%))
- **Identified Limitations:** *Requires reference enrollment identity images; cannot operate in zero-context verification.*
- **Access Links:** [Local PDF Endpoint](/papers/ID_Reveal_Biometric_Cozzolino_2021.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2012.02512) &bull; [Direct PDF](https://arxiv.org/pdf/2012.02512.pdf) &bull; [Official Code](https://github.com/grip-unina/ID-Reveal)

### 3. Adversarial Robustness of Deepfake Detectors
- **Authors:** Apurva Gandhi, Shomik Jain
- **Venue & Year:** `CVPRW 2020` (2020) &bull; **Sub-Category:** `Adversarial Perturbation Sensitivity`
- **Architecture:** Adversarial FGSM and PGD perturbations evaluated against top forensic detectors
- **Primary Dataset:** FaceForensics++, CelebA
- **Reported Performance:** **Perturbations under epsilon=2/255 reduce detector accuracy below 50%** (Accuracy drop (%))
- **Identified Limitations:** *Detectors lacking frequency residual grounding are highly susceptible to gradient-based attacks.*
- **Access Links:** [Local PDF Endpoint](/papers/Adversarial_Robustness_Gandhi_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2003.11145) &bull; [Direct PDF](https://arxiv.org/pdf/2003.11145.pdf) &bull; [Official Code](https://github.com/adv-deepfake/adversarial-deepfake)

### 4. Leveraging Real Talking Faces via Self-Supervision for Robust Forgery Detection (RealForensics)
- **Authors:** Alexandros Haliassos, Rodrigo Mira, Stavros Petridis, Maja Pantic
- **Venue & Year:** `CVPR 2022` (2022) &bull; **Sub-Category:** `Self-Supervised Natural Face Motion`
- **Architecture:** Self-supervised natural talking face representation (RealForensics)
- **Primary Dataset:** FaceForensics++, Celeb-DF, DFDC, WildDeepfake
- **Reported Performance:** **AUC: 86.9% cross-dataset on Celeb-DF; high robustness to lossy codecs** (ROC-AUC (%))
- **Identified Limitations:** *Relies on video motion dynamics; cannot classify still individual frames.*
- **Access Links:** [Local PDF Endpoint](/papers/RealForensics_SelfSupervised_Haliassos_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2201.03051) &bull; [Direct PDF](https://arxiv.org/pdf/2201.03051.pdf) &bull; [Official Code](https://github.com/alexandros-haliassos/RealForensics)

## Surveys, Benchmarks & Metrology
*Standardized evaluation benchmarks, unified evaluation toolkits (DeepfakeBench), challenge datasets (DFDC, Celeb-DF, WildDeepfake, GenImage), and state-of-the-art literature surveys.*

### 1. DeepfakeBench: A Comprehensive Benchmark of Deepfake Detection
- **Authors:** Zhiyuan Yan, Yong Zhang, Xuesong Yin, Jing Xiao, Baoyuan Wu
- **Venue & Year:** `NeurIPS 2023` (2023) &bull; **Sub-Category:** `Unified Modular Evaluation Benchmark`
- **Architecture:** Standardized benchmark framework with 15 detection methods and 9 datasets
- **Primary Dataset:** FF++, Celeb-DF, DFD, DFDC, FaceShifter, DeeperForensics
- **Reported Performance:** **Discloses that best detectors drop by 20-30% AUC when transitioning to unseen cross-dataset scenarios** (ROC-AUC, EER, Cross-dataset generalization)
- **Identified Limitations:** *Heavy memory requirements to evaluate all 15 backbones across 9 benchmarks.*
- **Access Links:** [Local PDF Endpoint](/papers/DeepfakeBench_Yan_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2307.01426) &bull; [Direct PDF](https://arxiv.org/pdf/2307.01426.pdf) &bull; [Official Code](https://github.com/SCLBD/DeepfakeBench)

### 2. Media Forensics in the Age of Generative AI: A Survey
- **Authors:** Luisa Verdoliva
- **Venue & Year:** `IEEE SPM 2020` (2020) &bull; **Sub-Category:** `Holistic Multimedia Forensic Foundations`
- **Architecture:** Comprehensive survey of multimedia forensic foundations, PRNU, steganography, and deep learning
- **Primary Dataset:** All public benchmarks
- **Reported Performance:** **Established foundational criteria for forensic explainability, anti-compression, and generalization** (Survey Taxonomy)
- **Identified Limitations:** *Pre-dates the rapid emergence of commercial latent diffusion and flow-matching models.*
- **Access Links:** [Local PDF Endpoint](/papers/Media_Forensics_Generative_AI_Verdoliva_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2004.14565) &bull; [Direct PDF](https://arxiv.org/pdf/2004.14565.pdf) &bull; [Official Code](https://github.com/grip-unina)

### 3. Deep Learning for Deepfakes Creation and Detection: A Survey
- **Authors:** Thanh Thi Nguyen, Cuong M. Nguyen, Dung Tien Nguyen, Duc Thanh Nguyen, Saeid Nahavandi
- **Venue & Year:** `CVIU 2022` (2022) &bull; **Sub-Category:** `Comprehensive Creation & Detection Taxonomies`
- **Architecture:** Detailed taxonomic survey of GANs, autoencoders, and early deepfake detection mechanisms
- **Primary Dataset:** Early benchmarks
- **Reported Performance:** **First systematized analysis of Deepfakes, Face2Face, FaceSwap, and NeuralTextures** (Comprehensive Survey)
- **Identified Limitations:** *Focuses primarily on early autoencoder generation pipelines.*
- **Access Links:** [Local PDF Endpoint](/papers/Deep_Learning_Deepfakes_Nguyen_2022.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1909.11573) &bull; [Direct PDF](https://arxiv.org/pdf/1909.11573.pdf) &bull; [Official Code](https://github.com/ondyari/FaceForensics)

### 4. The Deepfake Detection Challenge (DFDC) Dataset
- **Authors:** Brian Dolhansky, Joanna Bitton, Ben Pflaum, Jikuo Lu, Russ Howes, Mengjiao Wang, Cristian Canton Ferrer
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Large-Scale Public Challenge Dataset`
- **Architecture:** DFDC dataset release & Kaggle challenge evaluation
- **Primary Dataset:** DFDC (128,154 clips, 3,426 actors, diverse lighting & backgrounds)
- **Reported Performance:** **Top Kaggle ensemble achieved 82.5% AUC on unseen private test set** (Log-Loss, ROC-AUC)
- **Identified Limitations:** *Contains challenging lighting and compression that degrades standard CNN accuracy to near chance.*
- **Access Links:** [Local PDF Endpoint](/papers/DFDC_Dataset_Dolhansky_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2006.07397) &bull; [Direct PDF](https://arxiv.org/pdf/2006.07397.pdf) &bull; [Official Code](https://github.com/facebookresearch/DFDC)

### 5. Celeb-DF: A Large-scale Challenging Dataset for Deepfake Forensics
- **Authors:** Yuezun Li, Xin Yang, Pu Sun, Honggang Qi, Siwei Lyu
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `High-Quality Face Swap Benchmark`
- **Architecture:** Celeb-DF v2 dataset generation & comparative benchmark
- **Primary Dataset:** Celeb-DF v2 (5,639 high-quality videos, reduced boundary artifacts)
- **Reported Performance:** **Demonstrated that detectors trained on FF++ drop from 99% to ~65% on Celeb-DF** (ROC-AUC (%))
- **Identified Limitations:** *High-quality blending eliminates coarse splicing artifacts relied on by early detectors.*
- **Access Links:** [Local PDF Endpoint](/papers/Celeb_DF_Dataset_Li_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/1909.12962) &bull; [Direct PDF](https://arxiv.org/pdf/1909.12962.pdf) &bull; [Official Code](https://github.com/yuezunli/celeb-deepfakeforensics)

### 6. WildDeepfake: A Challenging Real-World Dataset for Deepfake Detection
- **Authors:** Bojia Zi, Minghao Chen, Jingying Chen, Bingbing Ni, Hao Wang
- **Venue & Year:** `ACM MM 2020` (2020) &bull; **Sub-Category:** `In-The-Wild Benchmark Dataset`
- **Architecture:** Real-World Internet Harvesting & Robustness Evaluation
- **Primary Dataset:** WildDeepfake (7,314 video sequences from social platforms)
- **Reported Performance:** **Baseline detectors drop from 95% on FF++ to <65% on WildDeepfake** (ROC-AUC (%) & Cross-Dataset Accuracy)
- **Identified Limitations:** *Unbalanced manipulation distribution; diverse unannotated compression codecs.*
- **Access Links:** [Local PDF Endpoint](/papers/WildDeepfake_Real_World_Zi_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2101.01456) &bull; [Direct PDF](https://arxiv.org/pdf/2101.01456.pdf) &bull; [Official Code](https://github.com/BojiaZi/WildDeepfake)

### 7. GenImage: A Million-Scale Dataset for Detecting AI-Generated Images
- **Authors:** Mingqiang Zhu, Chen Chen, Yan Luo, Yufan Liu, Qiang Shen, Zhen Shen
- **Venue & Year:** `NeurIPS 2023` (2023) &bull; **Sub-Category:** `Million-Scale Generative Benchmark`
- **Architecture:** Cross-Generator Evaluation across 8 Modern Generative Models
- **Primary Dataset:** GenImage (1,331,167 image pairs across Stable Diffusion, Midjourney, DALL-E)
- **Reported Performance:** **Detectors trained on GANs collapse to <55% accuracy on diffusion models** (Cross-Generator Generalization Accuracy (%))
- **Identified Limitations:** *Static images only; does not cover video diffusion generation.*
- **Access Links:** [Local PDF Endpoint](/papers/GenImage_Million_Scale_Dataset_Zhu_2023.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2306.08571) &bull; [Direct PDF](https://arxiv.org/pdf/2306.08571.pdf) &bull; [Official Code](https://github.com/GenImage-Dataset/GenImage)

### 8. DeeperForensics-1.0: A Large-Scale Dataset for Real-World Face Forgery Detection
- **Authors:** Liming Jiang, Ren Li, Wayne Wu, Chen Qian, Chen Change Loy
- **Venue & Year:** `CVPR 2020` (2020) &bull; **Sub-Category:** `Perturbation Robustness Benchmark`
- **Architecture:** DF-VAE Generative Model + 7 Transmission Perturbation Regimes
- **Primary Dataset:** 60,000 videos (17.6 million frames) recorded across 100 paid actors
- **Reported Performance:** **Comprehensive benchmark establishing performance cliffs under real transmission noise** (Robustness Score under Perturbations)
- **Identified Limitations:** *High storage footprint (>500 GB) for full uncompressed distribution.*
- **Access Links:** [Local PDF Endpoint](/papers/DeeperForensics_Real_World_Jiang_2020.pdf) &bull; [Venue / Abstract](https://arxiv.org/abs/2001.03024) &bull; [Direct PDF](https://arxiv.org/pdf/2001.03024.pdf) &bull; [Official Code](https://github.com/EndlessSora/DeeperForensics-1.0)

### 9. Deepfake Video Detection: What is Missing? Evaluating Face Forgery Detection in Indian Demographic Scenarios
- **Authors:** Richa Singh, Mayank Vatsa, Gaurav Goswami, Nalini Ratha
- **Venue & Year:** `IEEE Transactions on Biometrics, Behavior, and Identity Science (T-BIOM) 2022` (2022) &bull; **Sub-Category:** `Demographic & Ethnic Bias Evaluation`
- **Architecture:** Cross-Demographic Benchmark & Ethnic Fairness Auditing
- **Primary Dataset:** FaceForensics++, Celeb-DF, Indian Face Dataset (IFD)
- **Reported Performance:** **AUC: 89.2% on in-domain Caucasian, dropping to 67.4% on South Asian ethnic cohorts** (Cross-Demographic Generalization AUC (%))
- **Identified Limitations:** *Highlights critical algorithmic bias; models overfit to light-skinned features and fail on darker skin tones.*
- **Access Links:** [Local PDF Endpoint](/papers/Deepfake_Detection_Indian_Faces_Singh_2022.pdf) &bull; [Venue / Abstract](https://ieeexplore.ieee.org/document/9762291) &bull; [Direct PDF](https://arxiv.org/pdf/2204.09845.pdf) &bull; [Official Code](https://github.com/iab-rubic/IndianDeepfakeBenchmark)
