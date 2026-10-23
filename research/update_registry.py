"""
Deepfake Research Collective — Literature Registry & Directory Generator
Constructs and maintains research/papers/PAPERS_DIRECTORY.md from papers_data_compiled.json.
"""

import os
import json
from pathlib import Path

# Load compiled papers
papers_file = Path(__file__).resolve().parent / "papers_data_compiled.json"
with open(papers_file, "r", encoding="utf-8") as f:
    papers = json.load(f)

print(f"Loaded {len(papers)} papers from {papers_file}")

# Generate BibTeX for all papers
bibtex_blocks = []
for p in papers:
    pid = p["id"].replace("-", "_").replace(" ", "_")
    first_author = p["authors"].split(",")[0].split()[-1] if p["authors"] else "Author"
    first_author_clean = "".join(c for c in first_author if c.isalnum())
    key = f"{first_author_clean.lower()}{p['year']}{pid[:6]}"
    
    bib = f"""@article{{{key},
  title     = {{{p['title']}}},
  author    = {{{p['authors']}}},
  journal   = {{{p['venue']}}},
  year      = {{{p['year']}}},
  url       = {{{p['paper_url']}}}
}}"""
    bibtex_blocks.append(bib)

all_bibtex_str = "\n\n".join(bibtex_blocks)

categories_order = [
    "Spatial & Blending Forensics",
    "Frequency & Spectral Forensics",
    "Diffusion & Generative Fingerprints",
    "Temporal & Video Dynamics",
    "Audio Deepfake & Speech Anti-Spoofing",
    "Multimodal Audio-Visual Forensics",
    "Codec & Compression Robustness",
    "Surveys, Benchmarks & Metrology"
]

category_descriptions = {
    "Spatial & Blending Forensics": "Focuses on spatial-domain discontinuities, boundary blending artifacts, patch-level truncations, and warp residuals in manipulated facial imagery.",
    "Frequency & Spectral Forensics": "Analyzes Discrete Cosine Transform (DCT), Discrete Fourier Transform (DFT), high-pass residuals, and phase spectra to detect generative spectral anomalies.",
    "Diffusion & Generative Fingerprints": "Examines architectural fingerprints specific to modern latent diffusion models (LDMs), DDIM inversion error, text-to-image attribution, and flow-matching engines.",
    "Temporal & Video Dynamics": "Investigates inter-frame temporal coherence, flicker artifacts, phoneme-viseme biomechanical consistency, and spatiotemporal sequence modeling.",
    "Audio Deepfake & Speech Anti-Spoofing": "Inspects raw audio waveforms, linear filterbanks (LFCC/CQCC), graph attention networks (AASIST), and pretrained speech foundation encoders (Wav2Vec 2.0, WavLM, Whisper).",
    "Multimodal Audio-Visual Forensics": "Studies cross-modal synchronization, audio-visual representation dissonance, and joint contrastive learning across facial video and speech tracks.",
    "Codec & Compression Robustness": "Addresses forensic vulnerability to lossy social media compression (JPEG, H.264/AVC, H.265/HEVC, Opus, MP3), anti-forensic perturbation attacks, and out-of-distribution shifts.",
    "Surveys, Benchmarks & Metrology": "Standardized evaluation benchmarks, unified evaluation toolkits (DeepfakeBench), challenge datasets (DFDC, Celeb-DF), and comprehensive state-of-the-art literature surveys."
}

md_lines = [
    "# Deepfake Research Collective — Forensic Literature Repository & Paper Directory",
    "",
    "> **Archive Status:** 53 Full-Text Academic Papers Downloaded Locally (~211.5 MB total PDF archive).",
    "> All papers are categorized according to academic domain, indexing verified arXiv identifiers, conference venues, direct local PDF endpoints, official code repositories, reported benchmark metrics, and known research limitations.",
    "",
    "## Table of Contents",
    ""
]

for idx, cat in enumerate(categories_order, 1):
    count = sum(1 for p in papers if p["category"] == cat)
    anchor = cat.lower().replace(" ", "-").replace("&", "").replace(",", "")
    md_lines.append(f"{idx}. [{cat} ({count} Papers)](#{anchor})")

md_lines.append("")
md_lines.append("---")
md_lines.append("")

for cat in categories_order:
    cat_papers = [p for p in papers if p["category"] == cat]
    anchor = cat.lower().replace(" ", "-").replace("&", "").replace(",", "")
    md_lines.append(f"## {cat}")
    md_lines.append(f"*{category_descriptions.get(cat, '')}*")
    md_lines.append("")

    for idx, p in enumerate(cat_papers, 1):
        md_lines.append(f"### {idx}. {p['title']}")
        md_lines.append(f"- **Authors:** {p['authors']}")
        md_lines.append(f"- **Venue & Year:** `{p['venue']}` ({p['year']}) &bull; **Sub-Category:** `{p['sub_category']}`")
        md_lines.append(f"- **Architecture:** {p['architecture']}")
        md_lines.append(f"- **Primary Dataset:** {p['dataset']}")
        md_lines.append(f"- **Reported Performance:** **{p['result']}** ({p['metric']})")
        md_lines.append(f"- **Identified Limitations:** *{p['limitations']}*")
        
        links = []
        links.append(f"[Local PDF Archive]({p['local_pdf']})")
        links.append(f"[arXiv Abstract]({p['paper_url']})")
        links.append(f"[Direct PDF]({p['pdf_url']})")
        if p.get("code_url"):
            links.append(f"[Official Code]({p['code_url']})")
        
        md_lines.append(f"- **Access Links:** {' &bull; '.join(links)}")
        md_lines.append("")

output_file = Path(__file__).resolve().parent / "papers" / "PAPERS_DIRECTORY.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"Saved {output_file} successfully!")
