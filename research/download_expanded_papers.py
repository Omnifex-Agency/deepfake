"""
DeepShield AI — Batch Downloader for Expanded Forensic Research Paper Corpus
Downloads newly cataloged open-access research papers from arXiv with rate-limiting.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
from pathlib import Path

PDF_DIR = Path(__file__).resolve().parent / "papers" / "pdfs"
PDF_DIR.mkdir(parents=True, exist_ok=True)

# Master list of expanded papers
EXPANDED_PAPERS = [
    # Category 1: Spatial & Blending Forensics
    {
        "id": "1901.08971",
        "filename": "FaceForensics_PlusPlus_Rossler_2019.pdf",
        "title": "FaceForensics++: Learning to Detect Manipulated Facial Images",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Boundary Artifacts & Face Splicing",
        "domain": "Spatial & Blending",
        "year": 2019,
        "venue": "ICCV 2019",
        "pdf_url": "https://arxiv.org/pdf/1901.08971.pdf",
        "arxiv_url": "https://arxiv.org/abs/1901.08971",
        "code_url": "https://github.com/ondyari/FaceForensics"
    },
    {
        "id": "1912.12623",
        "filename": "Face_XRay_Li_2020.pdf",
        "title": "Face X-Ray for More General Face Forgery Detection",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Blending Boundary Segmentation",
        "domain": "Spatial & Blending",
        "year": 2020,
        "venue": "CVPR 2020",
        "pdf_url": "https://arxiv.org/pdf/1912.12623.pdf",
        "arxiv_url": "https://arxiv.org/abs/1912.12623",
        "code_url": "https://github.com/li-lingzhi/FaceXray"
    },
    {
        "id": "2008.10588",
        "filename": "Patch_Forensics_Chai_2020.pdf",
        "title": "What Makes Fake Images Detectable? Understanding Properties of Synthesized Images",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Patch-Level Truncation",
        "domain": "Spatial & Blending",
        "year": 2020,
        "venue": "ECCV 2020",
        "pdf_url": "https://arxiv.org/pdf/2008.10588.pdf",
        "arxiv_url": "https://arxiv.org/abs/2008.10588",
        "code_url": "https://github.com/chail/patch-forensics"
    },
    {
        "id": "2103.02406",
        "filename": "Multi_Attentional_Zhao_2021.pdf",
        "title": "Multi-attentional Deepfake Detection",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Multi-Region Spatial Attention",
        "domain": "Spatial & Blending",
        "year": 2021,
        "venue": "CVPR 2021",
        "pdf_url": "https://arxiv.org/pdf/2103.02406.pdf",
        "arxiv_url": "https://arxiv.org/abs/2103.02406",
        "code_url": "https://github.com/nii-yamagishilab/Multi-attentional-Deepfake-Detection"
    },
    {
        "id": "2105.04838",
        "filename": "Pairwise_Self_Consistency_Zhao_2021.pdf",
        "title": "Pair-wise Self-Consistency Learning for Deepfake Detection",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Pairwise Consistency",
        "domain": "Spatial & Blending",
        "year": 2021,
        "venue": "ACM MM 2021",
        "pdf_url": "https://arxiv.org/pdf/2105.04838.pdf",
        "arxiv_url": "https://arxiv.org/abs/2105.04838",
        "code_url": "https://github.com/chail/patch-forensics"
    },
    {
        "id": "2207.03061",
        "filename": "Look_Locally_Chen_2022.pdf",
        "title": "Look Locally for Understanding Globally: A Generalizable Face Forgery Detection via Reconstruction",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Local-Global Reconstruction",
        "domain": "Spatial & Blending",
        "year": 2022,
        "venue": "ECCV 2022",
        "pdf_url": "https://arxiv.org/pdf/2207.03061.pdf",
        "arxiv_url": "https://arxiv.org/abs/2207.03061",
        "code_url": "https://github.com/ChenH0528/LGrad"
    },
    {
        "id": "2403.18808",
        "filename": "NPR_Upsampling_Tan_2024.pdf",
        "title": "Rethinking the Up-Sampling Operations in CNN-based Face Forgery Detection",
        "category": "Spatial & Blending Forensics",
        "sub_category": "Neighboring Pixel Relationship (NPR)",
        "domain": "Spatial & Blending",
        "year": 2024,
        "venue": "CVPR 2024",
        "pdf_url": "https://arxiv.org/pdf/2403.18808.pdf",
        "arxiv_url": "https://arxiv.org/abs/2403.18808",
        "code_url": "https://github.com/chuangchuangtan/NPR-DeepfakeDetection"
    },

    # Category 2: Frequency & Spectral Forensics
    {
        "id": "2003.08685",
        "filename": "Frequency_Analysis_Frank_2020.pdf",
        "title": "Leveraging Frequency Analysis for Deep Fake Image Recognition",
        "category": "Frequency & Spectral Forensics",
        "sub_category": "Discrete Cosine Transform (DCT)",
        "domain": "Frequency & Spectral",
        "year": 2020,
        "venue": "ICML 2020",
        "pdf_url": "https://arxiv.org/pdf/2003.08685.pdf",
        "arxiv_url": "https://arxiv.org/abs/2003.08685",
        "code_url": "https://github.com/frederic-frank/frequency-analysis-for-deep-fake-image-recognition"
    },
    {
        "id": "1911.00686",
        "filename": "Watch_Your_Up_Convolution_Durall_2020.pdf",
        "title": "Watch your Up-Convolution: CNN Based Generative Deep Neural Networks are Failing to Reproduce Spectral Distributions",
        "category": "Frequency & Spectral Forensics",
        "sub_category": "Radial Spectral Analysis (Azimuthal Average)",
        "domain": "Frequency & Spectral",
        "year": 2020,
        "venue": "CVPR 2020",
        "pdf_url": "https://arxiv.org/pdf/1911.00686.pdf",
        "arxiv_url": "https://arxiv.org/abs/1911.00686",
        "code_url": "https://github.com/cc-hpc-itwm/UpConvolution"
    },
    {
        "id": "2007.09355",
        "filename": "Thinking_In_Frequency_Qian_2020.pdf",
        "title": "Thinking in Frequency: Face Forgery Detection by Mining Frequency-aware Clues (F3-Net)",
        "category": "Frequency & Spectral Forensics",
        "sub_category": "Dual-Stream Frequency Decomposition (F3-Net)",
        "domain": "Frequency & Spectral",
        "year": 2020,
        "venue": "ECCV 2020",
        "pdf_url": "https://arxiv.org/pdf/2007.09355.pdf",
        "arxiv_url": "https://arxiv.org/abs/2007.09355",
        "code_url": "https://github.com/weixiangquan/F3-Net"
    },
    {
        "id": "2103.05348",
        "filename": "Spatial_Phase_Shallow_Cao_2021.pdf",
        "title": "Spatial-Phase Shallow Learning: Rethinking Face Forgery Detection in Frequency Domain (SPSL)",
        "category": "Frequency & Spectral Forensics",
        "sub_category": "Phase Spectrum Analysis",
        "domain": "Frequency & Spectral",
        "year": 2021,
        "venue": "CVPR 2021",
        "pdf_url": "https://arxiv.org/pdf/2103.05348.pdf",
        "arxiv_url": "https://arxiv.org/abs/2103.05348",
        "code_url": "https://github.com/SunnyBingoMe/SPSL"
    },
    {
        "id": "2103.14917",
        "filename": "Frequency_Domain_Learning_Li_2021.pdf",
        "title": "Frequency-Domain Learning for Face Forgery Detection",
        "category": "Frequency & Spectral Forensics",
        "sub_category": "Multi-Frequency Band Attention",
        "domain": "Frequency & Spectral",
        "year": 2021,
        "venue": "CVPR 2021",
        "pdf_url": "https://arxiv.org/pdf/2103.14917.pdf",
        "arxiv_url": "https://arxiv.org/abs/2103.14917",
        "code_url": "https://github.com/JiamingLi-2020/Frequency-Domain-Learning-for-Face-Forgery-Detection"
    },
    {
        "id": "2103.12376",
        "filename": "Generalizing_High_Frequency_Luo_2021.pdf",
        "title": "Generalizing Face Forgery Detection with High-frequency Features",
        "category": "Frequency & Spectral Forensics",
        "sub_category": "High-Frequency Residual Filtering",
        "domain": "Frequency & Spectral",
        "year": 2021,
        "venue": "CVPR 2021",
        "pdf_url": "https://arxiv.org/pdf/2103.12376.pdf",
        "arxiv_url": "https://arxiv.org/abs/2103.12376",
        "code_url": "https://github.com/luoyuzhou/Generalizing-Face-Forgery-Detection"
    },

    # Category 3: Diffusion & Generative Fingerprints
    {
        "id": "1912.11035",
        "filename": "CNN_Detection_Wang_2020.pdf",
        "title": "CNN-Generated Images Are Surprisingly Easy to Spot... for Now",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "CNN Periodic Upsampling Artifacts",
        "domain": "Diffusion & Generative",
        "year": 2020,
        "venue": "CVPR 2020",
        "pdf_url": "https://arxiv.org/pdf/1912.11035.pdf",
        "arxiv_url": "https://arxiv.org/abs/1912.11035",
        "code_url": "https://github.com/peterwang512/CNNDetection"
    },
    {
        "id": "2302.10174",
        "filename": "Universal_Fake_Detect_Ojha_2023.pdf",
        "title": "Towards Universal Fake Image Detectors that Generalize Across Generative Models",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Pretrained Vision-Language Probing (CLIP)",
        "domain": "Diffusion & Generative",
        "year": 2023,
        "venue": "CVPR 2023",
        "pdf_url": "https://arxiv.org/pdf/2302.10174.pdf",
        "arxiv_url": "https://arxiv.org/abs/2302.10174",
        "code_url": "https://github.com/Yuheng-Li/UniversalFakeDetect"
    },
    {
        "id": "2303.09295",
        "filename": "DIRE_Diffusion_Detection_Wang_2023.pdf",
        "title": "DIRE for Diffusion-Generated Image Detection",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Diffusion Reconstruction Error (DDIM)",
        "domain": "Diffusion & Generative",
        "year": 2023,
        "venue": "ICCV 2023",
        "pdf_url": "https://arxiv.org/pdf/2303.09295.pdf",
        "arxiv_url": "https://arxiv.org/abs/2303.09295",
        "code_url": "https://github.com/ZhendongWang6/DIRE"
    },
    {
        "id": "2211.00680",
        "filename": "Diffusion_Synthetic_Detection_Corvi_2023.pdf",
        "title": "On the Detection of Synthetic Images Generated by Diffusion Models",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Latent Diffusion Noise Fingerprinting",
        "domain": "Diffusion & Generative",
        "year": 2023,
        "venue": "ICIP 2023",
        "pdf_url": "https://arxiv.org/pdf/2211.00680.pdf",
        "arxiv_url": "https://arxiv.org/abs/2211.00680",
        "code_url": "https://github.com/grip-unina/DMimageDetection"
    },
    {
        "id": "2403.18789",
        "filename": "CoDE_Contrasting_Diffusion_Cozzolino_2024.pdf",
        "title": "Contrasting Deepfakes Diffusion by Global-Local Feature Decoupling (CoDE)",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Global-Local Feature Decoupling",
        "domain": "Diffusion & Generative",
        "year": 2024,
        "venue": "ECCV 2024",
        "pdf_url": "https://arxiv.org/pdf/2403.18789.pdf",
        "arxiv_url": "https://arxiv.org/abs/2403.18789",
        "code_url": "https://github.com/aimagelab/CoDE"
    },
    {
        "id": "2210.06998",
        "filename": "DE_FAKE_Attribution_Sha_2023.pdf",
        "title": "DE-FAKE: Detection and Attribution of Fake Images Generated by Text-to-Image Generation Models",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Text-to-Image Attribution & Watermarking",
        "domain": "Diffusion & Generative",
        "year": 2023,
        "venue": "ACM CCS 2023",
        "pdf_url": "https://arxiv.org/pdf/2210.06998.pdf",
        "arxiv_url": "https://arxiv.org/abs/2210.06998",
        "code_url": "https://github.com/zeyangsha/DE-FAKE"
    },
    {
        "id": "2210.14571",
        "filename": "Towards_Detection_Diffusion_Ricker_2023.pdf",
        "title": "Towards the Detection of Diffusion Model Deepfakes: A Synthetic and Real Benchmark",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Cross-Architecture Diffusion Benchmarking",
        "domain": "Diffusion & Generative",
        "year": 2023,
        "venue": "WACV 2023",
        "pdf_url": "https://arxiv.org/pdf/2210.14571.pdf",
        "arxiv_url": "https://arxiv.org/abs/2210.14571",
        "code_url": "https://github.com/jonasricker/diffusion-model-deepfake-detection"
    },
    {
        "id": "2305.15008",
        "filename": "Synthbuster_Diffusion_Bammey_2024.pdf",
        "title": "Synthbuster: Towards Detection of Diffusion Model Generated Images Using Deep Features",
        "category": "Diffusion & Generative Fingerprints",
        "sub_category": "Multi-Generator Deep Residual Features",
        "domain": "Diffusion & Generative",
        "year": 2024,
        "venue": "IEEE OJSP 2024",
        "pdf_url": "https://arxiv.org/pdf/2305.15008.pdf",
        "arxiv_url": "https://arxiv.org/abs/2305.15008",
        "code_url": "https://github.com/grip-unina/Synthbuster"
    },

    # Category 4: Temporal & Video Dynamics
    {
        "id": "2108.06693",
        "filename": "FTCN_Temporal_Coherence_Zheng_2021.pdf",
        "title": "Exploring Temporal Coherence for More General Video Face Forgery Detection (FTCN)",
        "category": "Temporal & Video Dynamics",
        "sub_category": "Fully Temporal Convolutional Network",
        "domain": "Temporal & Video",
        "year": 2021,
        "venue": "ICCV 2021",
        "pdf_url": "https://arxiv.org/pdf/2108.06693.pdf",
        "arxiv_url": "https://arxiv.org/abs/2108.06693",
        "code_url": "https://github.com/yinglinzheng/FTCN"
    },
    {
        "id": "2101.03033",
        "filename": "LipForensics_Lips_Dont_Lie_Haliassos_2021.pdf",
        "title": "Lips Don't Lie: A Generalisable and Robust Approach to Face Forgery Detection (LipForensics)",
        "category": "Temporal & Video Dynamics",
        "sub_category": "Visual Speech Dynamics & Lip Coherence",
        "domain": "Temporal & Video",
        "year": 2021,
        "venue": "CVPR 2021",
        "pdf_url": "https://arxiv.org/pdf/2101.03033.pdf",
        "arxiv_url": "https://arxiv.org/abs/2101.03033",
        "code_url": "https://github.com/alexandros-haliassos/LipForensics"
    },
    {
        "id": "2107.02612",
        "filename": "EfficientNet_ViT_Deepfake_Coccomini_2022.pdf",
        "title": "Combining EfficientNet and Vision Transformers for Video Deepfake Detection",
        "category": "Temporal & Video Dynamics",
        "sub_category": "Hybrid CNN-Vision Transformer Sequences",
        "domain": "Temporal & Video",
        "year": 2022,
        "venue": "PRL 2022",
        "pdf_url": "https://arxiv.org/pdf/2107.02612.pdf",
        "arxiv_url": "https://arxiv.org/abs/2107.02612",
        "code_url": "https://github.com/DavideA/cEfficientViT"
    },
    {
        "id": "2109.01860",
        "filename": "Spatiotemporal_Inconsistency_Gu_2021.pdf",
        "title": "Spatio-Temporal Inconsistency Learning for Deepfake Video Detection",
        "category": "Temporal & Video Dynamics",
        "sub_category": "3D Spatio-Temporal Discrepancy",
        "domain": "Temporal & Video",
        "year": 2021,
        "venue": "ACM MM 2021",
        "pdf_url": "https://arxiv.org/pdf/2109.01860.pdf",
        "arxiv_url": "https://arxiv.org/abs/2109.01860",
        "code_url": "https://github.com/ZhihaoGu/STIL"
    },
    {
        "id": "2304.14818",
        "filename": "AltFreezing_Appearance_Motion_Wang_2023.pdf",
        "title": "Detecting Deepfake Videos from Appearance and Motion (AltFreezing)",
        "category": "Temporal & Video Dynamics",
        "sub_category": "Alternating Appearance/Motion Freezing",
        "domain": "Temporal & Video",
        "year": 2023,
        "venue": "CVPR 2023",
        "pdf_url": "https://arxiv.org/pdf/2304.14818.pdf",
        "arxiv_url": "https://arxiv.org/abs/2304.14818",
        "code_url": "https://github.com/ZhendongWang6/AltFreezing"
    },
    {
        "id": "2004.14491",
        "filename": "Phoneme_Viseme_Mismatches_Agarwal_2020.pdf",
        "title": "Detecting Deep-Fake Videos from Phoneme-Viseme Mismatches",
        "category": "Temporal & Video Dynamics",
        "sub_category": "Biomechanical Phoneme-Viseme Inconsistency",
        "domain": "Temporal & Video",
        "year": 2020,
        "venue": "CVPRW 2020",
        "pdf_url": "https://arxiv.org/pdf/2004.14491.pdf",
        "arxiv_url": "https://arxiv.org/abs/2004.14491",
        "code_url": "https://github.com/shruti-agarwal/Phoneme-Viseme-Deepfakes"
    },

    # Category 5: Audio Deepfake & Speech Anti-Spoofing
    {
        "id": "1904.05576",
        "filename": "LFCC_LCNN_ASVspoof_Lavrentyeva_2019.pdf",
        "title": "STC Antispoofing Systems for the ASVspoof 2019 Challenge (LFCC-LCNN)",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Light CNN on Linear Filterbanks (LFCC-LCNN)",
        "domain": "Audio Anti-Spoofing",
        "year": 2019,
        "venue": "Interspeech 2019",
        "pdf_url": "https://arxiv.org/pdf/1904.05576.pdf",
        "arxiv_url": "https://arxiv.org/abs/1904.05576",
        "code_url": "https://github.com/asvspoof-challenge/2019"
    },
    {
        "id": "2011.01108",
        "filename": "RawNet2_Audio_Spoofing_Tak_2021.pdf",
        "title": "RawNet2: More is Better for Voice Anti-Spoofing",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Raw Audio Waveform Sinc-Convolutions",
        "domain": "Audio Anti-Spoofing",
        "year": 2021,
        "venue": "Interspeech 2021",
        "pdf_url": "https://arxiv.org/pdf/2011.01108.pdf",
        "arxiv_url": "https://arxiv.org/abs/2011.01108",
        "code_url": "https://github.com/eurecom-asp/RawNet2"
    },
    {
        "id": "2110.01200",
        "filename": "AASIST_Graph_Attention_Jung_2022.pdf",
        "title": "AASIST: Audio Anti-Spoofing Using Integrated Spectro-Temporal Graph Attention Networks",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Heterogeneous Graph Attention (AASIST)",
        "domain": "Audio Anti-Spoofing",
        "year": 2022,
        "venue": "ICASSP 2022",
        "pdf_url": "https://arxiv.org/pdf/2110.01200.pdf",
        "arxiv_url": "https://arxiv.org/abs/2110.01200",
        "code_url": "https://github.com/clovaai/aasist"
    },
    {
        "id": "2202.12233",
        "filename": "Wav2Vec2_Audio_Spoofing_Tak_2022.pdf",
        "title": "End-to-End Anti-Spoofing with Pre-Trained Wav2Vec 2.0 Models",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Self-Supervised Acoustic Representations",
        "domain": "Audio Anti-Spoofing",
        "year": 2022,
        "venue": "Interspeech 2022",
        "pdf_url": "https://arxiv.org/pdf/2202.12233.pdf",
        "arxiv_url": "https://arxiv.org/abs/2202.12233",
        "code_url": "https://github.com/TakHemlata/SSL_Anti-spoofing"
    },
    {
        "id": "2111.02813",
        "filename": "WaveFake_Dataset_Frank_2021.pdf",
        "title": "WaveFake: A Data Set to Facilitate Audio Deepfake Detection",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Vocoder Architecture Artifacts",
        "domain": "Audio Anti-Spoofing",
        "year": 2021,
        "venue": "ACM IH&MMSec 2021",
        "pdf_url": "https://arxiv.org/pdf/2111.02813.pdf",
        "arxiv_url": "https://arxiv.org/abs/2111.02813",
        "code_url": "https://github.com/joel-frank/wavefake"
    },
    {
        "id": "2203.16263",
        "filename": "Audio_Deepfake_In_The_Wild_Muller_2022.pdf",
        "title": "Does Audio Deepfake Detection Generalize to In-the-Wild Scenarios?",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "In-the-Wild Generalization Protocols",
        "domain": "Audio Anti-Spoofing",
        "year": 2022,
        "venue": "Interspeech 2022",
        "pdf_url": "https://arxiv.org/pdf/2203.16263.pdf",
        "arxiv_url": "https://arxiv.org/abs/2203.16263",
        "code_url": "https://github.com/media-sec-lab/Audio-Deepfake-Detection"
    },
    {
        "id": "2305.15049",
        "filename": "Whisper_Deepfake_Defense_Kawa_2023.pdf",
        "title": "Defense Against Audio Deepfakes Using Pretrained Whisper Features",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Whisper Log-Mel Encoder Transfer",
        "domain": "Audio Anti-Spoofing",
        "year": 2023,
        "venue": "Interspeech 2023",
        "pdf_url": "https://arxiv.org/pdf/2305.15049.pdf",
        "arxiv_url": "https://arxiv.org/abs/2305.15049",
        "code_url": "https://github.com/piotrkawa/deepfake-whisper-features"
    },
    {
        "id": "2302.08182",
        "filename": "Speech_SSL_AntiSpoofing_Zhang_2023.pdf",
        "title": "An Empirical Study of Speech Self-Supervised Models for Anti-Spoofing",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Comparative Speech SSL Benchmark",
        "domain": "Audio Anti-Spoofing",
        "year": 2023,
        "venue": "ICASSP 2023",
        "pdf_url": "https://arxiv.org/pdf/2302.08182.pdf",
        "arxiv_url": "https://arxiv.org/abs/2302.08182",
        "code_url": "https://github.com/asvspoof-challenge"
    },
    {
        "id": "2109.00537",
        "filename": "ASVspoof_2021_Accelerating_Yamagishi_2021.pdf",
        "title": "ASVspoof 2021: Accelerating Progress in Spoofed and Deepfake Speech Detection",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Standardized Speech Spoofing Metrology",
        "domain": "Audio Anti-Spoofing",
        "year": 2021,
        "venue": "Computer Speech & Language 2021",
        "pdf_url": "https://arxiv.org/pdf/2109.00537.pdf",
        "arxiv_url": "https://arxiv.org/abs/2109.00537",
        "code_url": "https://github.com/asvspoof-challenge/2021"
    },
    {
        "id": "2402.16484",
        "filename": "Discrepancy_Aware_Audio_Ba_2024.pdf",
        "title": "Discrepancy-Aware Representation Learning for Audio Deepfake Detection",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Spectrogram Discrepancy Representation",
        "domain": "Audio Anti-Spoofing",
        "year": 2024,
        "venue": "IEEE/ACM TASLP 2024",
        "pdf_url": "https://arxiv.org/pdf/2402.16484.pdf",
        "arxiv_url": "https://arxiv.org/abs/2402.16484",
        "code_url": "https://github.com/ba-speech/DARL"
    },
    {
        "id": "2406.18240",
        "filename": "ASVspoof5_Challenge_Plan_Nautsch_2024.pdf",
        "title": "ASVspoof 5 Challenge Evaluation Plan: Deepfake Speech in Complex Acoustic Scenarios",
        "category": "Audio Deepfake & Speech Anti-Spoofing",
        "sub_category": "Crowdsourced Speech & Codec Evaluation",
        "domain": "Audio Anti-Spoofing",
        "year": 2024,
        "venue": "Interspeech 2024",
        "pdf_url": "https://arxiv.org/pdf/2406.18240.pdf",
        "arxiv_url": "https://arxiv.org/abs/2406.18240",
        "code_url": "https://github.com/asvspoof-challenge/asvspoof5"
    },

    # Category 6: Multimodal Audio-Visual Forensics
    {
        "id": "2108.05080",
        "filename": "FakeAVCeleb_Multimodal_Khalid_2021.pdf",
        "title": "FakeAVCeleb: A Novel Audio-Video Multimodal Deepfake Dataset",
        "category": "Multimodal Audio-Visual Forensics",
        "sub_category": "Four-Quadrant Audio-Visual Benchmark",
        "domain": "Multimodal Forensics",
        "year": 2021,
        "venue": "NeurIPS 2021",
        "pdf_url": "https://arxiv.org/pdf/2108.05080.pdf",
        "arxiv_url": "https://arxiv.org/abs/2108.05080",
        "code_url": "https://github.com/DCL-Lab/FakeAVCeleb"
    },
    {
        "id": "2104.14772",
        "filename": "AVOiD_DF_Zhou_2021.pdf",
        "title": "Joint Audio-Visual Deepfake Detection (AVOiD-DF)",
        "category": "Multimodal Audio-Visual Forensics",
        "sub_category": "Cross-Modal Contrastive Learning",
        "domain": "Multimodal Forensics",
        "year": 2021,
        "venue": "CVPR 2021",
        "pdf_url": "https://arxiv.org/pdf/2104.14772.pdf",
        "arxiv_url": "https://arxiv.org/abs/2104.14772",
        "code_url": "https://github.com/zhouyuchen/AVOiD-DF"
    },
    {
        "id": "2301.01798",
        "filename": "SelfSupervised_AudioVisual_Feng_2023.pdf",
        "title": "Self-Supervised Video Forensics by Audio-Visual Anomaly Detection",
        "category": "Multimodal Audio-Visual Forensics",
        "sub_category": "Cross-Modal Anomaly Detection",
        "domain": "Multimodal Forensics",
        "year": 2023,
        "venue": "CVPR 2023",
        "pdf_url": "https://arxiv.org/pdf/2301.01798.pdf",
        "arxiv_url": "https://arxiv.org/abs/2301.01798",
        "code_url": "https://github.com/cfeng16/audio-visual-forensics"
    },
    {
        "id": "2005.14405",
        "filename": "Audio_Visual_Dissonance_Chugh_2020.pdf",
        "title": "Not Made for Each Other: Audio-Visual Dissonance-based Deepfake Detection",
        "category": "Multimodal Audio-Visual Forensics",
        "sub_category": "Cross-Modal Representation Dissonance",
        "domain": "Multimodal Forensics",
        "year": 2020,
        "venue": "ACM MM 2020",
        "pdf_url": "https://arxiv.org/pdf/2005.14405.pdf",
        "arxiv_url": "https://arxiv.org/abs/2005.14405",
        "code_url": "https://github.com/krishnachugh/AV-Dissonance"
    },
    {
        "id": "2401.08761",
        "filename": "AVFF_Audio_Visual_Fusion_Oorloff_2024.pdf",
        "title": "AVFF: Audio-Visual Feature Fusion for Generalizable Deepfake Detection",
        "category": "Multimodal Audio-Visual Forensics",
        "sub_category": "Hierarchical Audio-Visual Fusion",
        "domain": "Multimodal Forensics",
        "year": 2024,
        "venue": "IEEE TIFS 2024",
        "pdf_url": "https://arxiv.org/pdf/2401.08761.pdf",
        "arxiv_url": "https://arxiv.org/abs/2401.08761",
        "code_url": "https://github.com/DCL-Lab/AVFF"
    },
    {
        "id": "2308.09452",
        "filename": "DualBranch_Cross_Attention_Sun_2023.pdf",
        "title": "Dual-Branch Spatio-Temporal Cross-Attention for Audio-Visual Deepfake Detection",
        "category": "Multimodal Audio-Visual Forensics",
        "sub_category": "Cross-Attention Transformers",
        "domain": "Multimodal Forensics",
        "year": 2023,
        "venue": "ACM MM 2023",
        "pdf_url": "https://arxiv.org/pdf/2308.09452.pdf",
        "arxiv_url": "https://arxiv.org/abs/2308.09452",
        "code_url": "https://github.com/sun-av/cross-attention-df"
    },

    # Category 7: Codec & Compression Robustness
    {
        "id": "2003.01265",
        "filename": "Anti_Forensics_Video_Deepfake_Neekhara_2021.pdf",
        "title": "Anti-Forensics of Video Deepfake Detection via GAN-Based Post-Processing",
        "category": "Codec & Compression Robustness",
        "sub_category": "Adversarial Anti-Forensics & Artifact Masking",
        "domain": "Codec Robustness",
        "year": 2021,
        "venue": "CVPRW 2021",
        "pdf_url": "https://arxiv.org/pdf/2003.01265.pdf",
        "arxiv_url": "https://arxiv.org/abs/2003.01265",
        "code_url": "https://github.com/paarthneekhara/deepfake_antiforensics"
    },
    {
        "id": "2012.02512",
        "filename": "ID_Reveal_Biometric_Cozzolino_2021.pdf",
        "title": "ID-Reveal: Out-of-Distribution Deepfake Detection via Biometric Representation Learning",
        "category": "Codec & Compression Robustness",
        "sub_category": "Biometric Identity Invariance",
        "domain": "Codec Robustness",
        "year": 2021,
        "venue": "ICCV 2021",
        "pdf_url": "https://arxiv.org/pdf/2012.02512.pdf",
        "arxiv_url": "https://arxiv.org/abs/2012.02512",
        "code_url": "https://github.com/grip-unina/ID-Reveal"
    },
    {
        "id": "2003.11145",
        "filename": "Adversarial_Robustness_Gandhi_2020.pdf",
        "title": "Adversarial Robustness of Deepfake Detectors",
        "category": "Codec & Compression Robustness",
        "sub_category": "Adversarial Perturbation Sensitivity",
        "domain": "Codec Robustness",
        "year": 2020,
        "venue": "CVPRW 2020",
        "pdf_url": "https://arxiv.org/pdf/2003.11145.pdf",
        "arxiv_url": "https://arxiv.org/abs/2003.11145",
        "code_url": "https://github.com/adv-deepfake/adversarial-deepfake"
    },
    {
        "id": "2201.03051",
        "filename": "RealForensics_SelfSupervised_Haliassos_2022.pdf",
        "title": "Leveraging Real Talking Faces via Self-Supervision for Robust Forgery Detection (RealForensics)",
        "category": "Codec & Compression Robustness",
        "sub_category": "Self-Supervised Natural Face Motion",
        "domain": "Codec Robustness",
        "year": 2022,
        "venue": "CVPR 2022",
        "pdf_url": "https://arxiv.org/pdf/2201.03051.pdf",
        "arxiv_url": "https://arxiv.org/abs/2201.03051",
        "code_url": "https://github.com/alexandros-haliassos/RealForensics"
    },

    # Category 8: Surveys, Benchmarks & Metrology
    {
        "id": "2307.01426",
        "filename": "DeepfakeBench_Yan_2023.pdf",
        "title": "DeepfakeBench: A Comprehensive Benchmark of Deepfake Detection",
        "category": "Surveys, Benchmarks & Metrology",
        "sub_category": "Unified Modular Evaluation Benchmark",
        "domain": "Surveys & Benchmarks",
        "year": 2023,
        "venue": "NeurIPS 2023",
        "pdf_url": "https://arxiv.org/pdf/2307.01426.pdf",
        "arxiv_url": "https://arxiv.org/abs/2307.01426",
        "code_url": "https://github.com/SCLBD/DeepfakeBench"
    },
    {
        "id": "2004.14565",
        "filename": "Media_Forensics_Generative_AI_Verdoliva_2020.pdf",
        "title": "Media Forensics in the Age of Generative AI: A Survey",
        "category": "Surveys, Benchmarks & Metrology",
        "sub_category": "Holistic Multimedia Forensic Foundations",
        "domain": "Surveys & Benchmarks",
        "year": 2020,
        "venue": "IEEE SPM 2020",
        "pdf_url": "https://arxiv.org/pdf/2004.14565.pdf",
        "arxiv_url": "https://arxiv.org/abs/2004.14565",
        "code_url": "https://github.com/grip-unina"
    },
    {
        "id": "1909.11573",
        "filename": "Deep_Learning_Deepfakes_Nguyen_2022.pdf",
        "title": "Deep Learning for Deepfakes Creation and Detection: A Survey",
        "category": "Surveys, Benchmarks & Metrology",
        "sub_category": "Comprehensive Creation & Detection Taxonomies",
        "domain": "Surveys & Benchmarks",
        "year": 2022,
        "venue": "CVIU 2022",
        "pdf_url": "https://arxiv.org/pdf/1909.11573.pdf",
        "arxiv_url": "https://arxiv.org/abs/1909.11573",
        "code_url": "https://github.com/ondyari/FaceForensics"
    },
    {
        "id": "2006.07397",
        "filename": "DFDC_Dataset_Dolhansky_2020.pdf",
        "title": "The Deepfake Detection Challenge (DFDC) Dataset",
        "category": "Surveys, Benchmarks & Metrology",
        "sub_category": "Large-Scale Public Challenge Dataset",
        "domain": "Surveys & Benchmarks",
        "year": 2020,
        "venue": "CVPR 2020",
        "pdf_url": "https://arxiv.org/pdf/2006.07397.pdf",
        "arxiv_url": "https://arxiv.org/abs/2006.07397",
        "code_url": "https://github.com/facebookresearch/DFDC"
    },
    {
        "id": "1909.12962",
        "filename": "Celeb_DF_Dataset_Li_2020.pdf",
        "title": "Celeb-DF: A Large-scale Challenging Dataset for Deepfake Forensics",
        "category": "Surveys, Benchmarks & Metrology",
        "sub_category": "High-Quality Face Swap Benchmark",
        "domain": "Surveys & Benchmarks",
        "year": 2020,
        "venue": "CVPR 2020",
        "pdf_url": "https://arxiv.org/pdf/1909.12962.pdf",
        "arxiv_url": "https://arxiv.org/abs/1909.12962",
        "code_url": "https://github.com/yuezunli/celeb-deepfakeforensics"
    }
]

def download_file(url: str, dest_path: Path):
    import ssl
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 DeepShieldAcademicBot/2.0"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=45, context=ctx) as response, open(dest_path, "wb") as out_file:
        data = response.read()
        out_file.write(data)

def main():
    print(f"=== DeepShield AI: Expanded Forensic Paper Downloader ===")
    print(f"Total Papers in Expanded Catalog: {len(EXPANDED_PAPERS)}")
    print(f"PDF Destination Directory: {PDF_DIR}\n")

    catalog = []
    success_count = 0
    skipped_count = 0
    fail_count = 0

    for idx, paper in enumerate(EXPANDED_PAPERS, start=1):
        filename = paper["filename"]
        dest = PDF_DIR / filename
        title_trunc = (paper["title"][:45] + "...") if len(paper["title"]) > 45 else paper["title"]

        print(f"[{idx:02d}/{len(EXPANDED_PAPERS):02d}] {paper['category']} | {title_trunc}")

        if dest.exists() and dest.stat().st_size > 10240:
            sz_kb = round(dest.stat().st_size / 1024)
            print(f"       -> [CACHE] Already downloaded: {sz_kb} KB ({filename})")
            skipped_count += 1
            catalog_entry = {**paper, "local_path": str(dest.relative_to(Path(__file__).resolve().parent)), "downloaded": True, "file_size_kb": sz_kb}
            catalog.append(catalog_entry)
            continue

        print(f"       -> Downloading from arXiv: {paper['pdf_url']}")
        try:
            download_file(paper["pdf_url"], dest)
            sz_kb = round(dest.stat().st_size / 1024)
            print(f"       -> [SUCCESS] Saved {sz_kb} KB")
            success_count += 1
            catalog_entry = {**paper, "local_path": str(dest.relative_to(Path(__file__).resolve().parent)), "downloaded": True, "file_size_kb": sz_kb}
            catalog.append(catalog_entry)
            time.sleep(1.2)  # Polite arXiv rate-limit delay
        except Exception as e:
            print(f"       -> [WARNING] Download failed: {e}")
            fail_count += 1
            catalog_entry = {**paper, "local_path": None, "downloaded": False, "file_size_kb": 0, "error": str(e)}
            catalog.append(catalog_entry)

    # Save updated catalog
    catalog_path = Path(__file__).resolve().parent / "papers" / "papers_catalog.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print("\n=== Download & Verification Summary ===")
    print(f"Newly Downloaded: {success_count}")
    print(f"Already Cached:   {skipped_count}")
    print(f"Failed:           {fail_count}")
    print(f"Total in Catalog: {len(catalog)}")
    print(f"Catalog saved:    {catalog_path}")

if __name__ == "__main__":
    main()
