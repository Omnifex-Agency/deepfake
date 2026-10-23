"""
DeepShield AI — Research & Scientific Paper Intelligence Platform
FastAPI Server dedicated exclusively to Research Papers, Models, and Dataset Findings.
"""

import os
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse

from app.research_data import (
    RESEARCH_PAPERS,
    DATASETS_ANALYSIS,
    RESEARCH_GAPS_AND_HYPOTHESES,
    BIBTEX_ENTRIES,
)

app = FastAPI(
    title="DeepShield AI — Research Paper & Scientific Intelligence Platform",
    description="Dedicated scientific exploration platform for multimodal deepfake research papers, candidate models, and dataset findings.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
PAPER_DRAFT_PATH = os.path.join(DOCS_DIR, "paper_draft.md")
EVAL_REPORT_PATH = os.path.join(DOCS_DIR, "evaluation_report.md")


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Returns platform health and research catalog index counts."""
    return {
        "status": "healthy",
        "service": "DeepShield AI Research & Paper Intelligence Platform",
        "version": "2.0.0",
        "catalog_summary": {
            "verified_papers_count": len(RESEARCH_PAPERS),
            "analyzed_datasets_count": len(DATASETS_ANALYSIS),
            "formal_hypotheses_count": len(RESEARCH_GAPS_AND_HYPOTHESES),
            "preprint_available": os.path.exists(PAPER_DRAFT_PATH),
        },
    }


@app.get("/api/v1/research/papers")
def get_research_papers() -> List[Dict[str, Any]]:
    """Returns all 32 verified literature review papers across Image, Audio, and Multimodal domains."""
    return RESEARCH_PAPERS


@app.get("/api/v1/research/datasets")
def get_datasets() -> List[Dict[str, Any]]:
    """Returns in-depth analysis of the 11 candidate forensic datasets and zero-leakage partitions."""
    return DATASETS_ANALYSIS


@app.get("/api/v1/research/hypotheses")
def get_hypotheses() -> List[Dict[str, Any]]:
    """Returns the 5 identified research gaps and 4 formal falsifiable hypotheses."""
    return RESEARCH_GAPS_AND_HYPOTHESES


@app.get("/api/v1/research/bibtex", response_class=PlainTextResponse)
def get_bibtex_citations() -> str:
    """Returns complete BibTeX library for all cited papers and DeepShield preprint."""
    return BIBTEX_ENTRIES


@app.get("/api/v1/research/paper_markdown", response_class=PlainTextResponse)
def get_paper_markdown() -> str:
    """Returns full markdown text of the conference preprint paper draft."""
    if os.path.exists(PAPER_DRAFT_PATH):
        with open(PAPER_DRAFT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    raise HTTPException(status_code=404, detail="Paper draft not found.")


@app.get("/api/v1/research/evaluation_report", response_class=PlainTextResponse)
def get_evaluation_report() -> str:
    """Returns empirical evaluation benchmark report."""
    if os.path.exists(EVAL_REPORT_PATH):
        with open(EVAL_REPORT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    raise HTTPException(status_code=404, detail="Evaluation report not found.")


# Mount static assets and serve research dashboard
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "app", "frontend")
PDFS_DIR = os.path.join(PROJECT_ROOT, "research", "papers", "pdfs")
os.makedirs(PDFS_DIR, exist_ok=True)

if os.path.exists(PDFS_DIR):
    app.mount("/papers", StaticFiles(directory=PDFS_DIR), name="papers")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", response_class=HTMLResponse)
    def serve_index():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            with open(index_file, "r", encoding="utf-8") as f:
                return f.read()
        return "<h1>DeepShield AI Research Dashboard is running.</h1>"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api.main:app", host="127.0.0.1", port=8000, reload=True)
