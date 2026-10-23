/**
 * DeepShield AI — Research & Scientific Paper Platform Client Logic
 * Handles tab routing, dynamic paper filtering, dataset catalog rendering,
 * hypothesis cards, and BibTeX citation copying.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Navigation Tabs
  const navButtons = document.querySelectorAll(".nav-tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  navButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      navButtons.forEach((b) => b.classList.remove("active"));
      tabPanes.forEach((p) => p.classList.remove("active"));

      btn.classList.add("active");
      const targetTab = btn.getAttribute("data-tab");
      const pane = document.getElementById(`pane-${targetTab}`);
      if (pane) {
        pane.classList.add("active");
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    });
  });

  // State Stores
  let allPapers = [];
  let allDatasets = [];
  let allHypotheses = [];

  // DOM Elements
  const papersContainer = document.getElementById("papers-cards-grid");
  const paperSearchInput = document.getElementById("paper-search-input");
  const paperDomainFilters = document.querySelectorAll("#paper-domain-filters .filter-pill");

  const datasetsContainer = document.getElementById("datasets-cards-grid");
  const datasetFilters = document.querySelectorAll("#dataset-domain-filters .filter-pill");

  const hypothesesContainer = document.getElementById("hypotheses-list-container");
  const bibtexDisplayBlock = document.getElementById("bibtex-display-block");
  const btnCopyAllBibtex = document.getElementById("btn-copy-all-bibtex");
  const btnCopyPaperCite = document.getElementById("btn-copy-paper-cite");

  // Fetch and Initialize All Research Data
  initializeResearchPlatform();

  async function initializeResearchPlatform() {
    try {
      const [papersRes, datasetsRes, hypoRes, bibtexRes] = await Promise.all([
        fetch("/api/v1/research/papers").then((r) => r.json()),
        fetch("/api/v1/research/datasets").then((r) => r.json()),
        fetch("/api/v1/research/hypotheses").then((r) => r.json()),
        fetch("/api/v1/research/bibtex").then((r) => r.text()),
      ]);

      allPapers = papersRes;
      allDatasets = datasetsRes;
      allHypotheses = hypoRes;

      renderPapersList(allPapers);
      renderDatasetsList(allDatasets);
      renderHypothesesList(allHypotheses);

      if (bibtexDisplayBlock) {
        bibtexDisplayBlock.textContent = bibtexRes;
      }
    } catch (err) {
      console.error("Failed to load research metadata:", err);
    }
  }

  // --- TAB 2: Papers Rendering & Filtering ---
  let activePaperDomain = "All";
  let paperSearchQuery = "";

  function filterAndRenderPapers() {
    let filtered = allPapers.filter((p) => {
      const cat = (p.category || "").toLowerCase();
      const dom = (p.domain || "").toLowerCase();
      const sub = (p.sub_category || "").toLowerCase();
      const active = activePaperDomain.toLowerCase();

      const matchesDomain =
        active === "all" ||
        cat.includes(active) ||
        dom.includes(active) ||
        sub.includes(active);

      const q = paperSearchQuery.toLowerCase();
      const matchesSearch =
        !q ||
        (p.title && p.title.toLowerCase().includes(q)) ||
        (p.authors && p.authors.toLowerCase().includes(q)) ||
        (p.architecture && p.architecture.toLowerCase().includes(q)) ||
        (p.dataset && p.dataset.toLowerCase().includes(q)) ||
        (p.category && p.category.toLowerCase().includes(q)) ||
        (p.sub_category && p.sub_category.toLowerCase().includes(q)) ||
        (p.venue && p.venue.toLowerCase().includes(q)) ||
        (p.limitations && p.limitations.toLowerCase().includes(q)) ||
        (p.result && p.result.toLowerCase().includes(q));

      return matchesDomain && matchesSearch;
    });

    renderPapersList(filtered);
  }

  function renderPapersList(papers) {
    if (!papersContainer) return;
    papersContainer.innerHTML = "";

    if (papers.length === 0) {
      papersContainer.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 48px; color: var(--text-muted); font-size: 0.95rem;">No research papers matched your search criteria.</div>`;
      return;
    }

    papers.forEach((p) => {
      const card = document.createElement("div");
      card.className = "paper-card";

      const localPdfUrl = p.local_pdf || `/papers/${p.filename || ""}`;
      const fileSizeDisplay = p.file_size_kb ? `${(p.file_size_kb / 1024).toFixed(1)} MB` : "PDF";

      card.innerHTML = `
        <div class="paper-card-top">
          <div class="card-badges-row">
            <span class="domain-badge">${p.category || p.domain}</span>
            <span class="sub-category-badge">${p.sub_category || "Forensic Analysis"}</span>
            <span class="venue-badge">${p.venue} &bull; ${p.year}</span>
            <span class="pdf-size-badge">${fileSizeDisplay} Local</span>
          </div>

          <h3 class="paper-card-title">${p.title}</h3>
          <div class="paper-card-authors">${p.authors}</div>
          
          <div class="paper-spec-row"><strong>Architecture:</strong> ${p.architecture}</div>
          <div class="paper-spec-row"><strong>Target Benchmark:</strong> ${p.dataset}</div>
          <div class="paper-spec-row"><strong>Reported SOTA Result:</strong> <span class="result-highlight">${p.result}</span></div>
          
          <div class="limitation-alert">
            <strong>Identified Research Gap / Limitation:</strong> ${p.limitations}
          </div>
        </div>

        <div class="paper-links-row">
          <a href="${localPdfUrl}" target="_blank" class="paper-link local-pdf-link">
            <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            Read Local PDF
          </a>
          <a href="${p.paper_url}" target="_blank" class="paper-link">arXiv Abstract &rarr;</a>
          <a href="${p.pdf_url}" target="_blank" class="paper-link">Direct arXiv PDF &rarr;</a>
          ${p.code_url ? `<a href="${p.code_url}" target="_blank" class="paper-link">Code &rarr;</a>` : ""}
          <button class="btn btn-sm btn-secondary btn-cite" data-id="${p.id}">Copy BibTeX</button>
        </div>
      `;

      card.querySelector(".btn-cite").addEventListener("click", () => {
        copySinglePaperBibTeX(p);
      });

      papersContainer.appendChild(card);
    });
  }

  if (paperSearchInput) {
    paperSearchInput.addEventListener("input", (e) => {
      paperSearchQuery = e.target.value.trim();
      filterAndRenderPapers();
    });
  }

  paperDomainFilters.forEach((btn) => {
    btn.addEventListener("click", () => {
      paperDomainFilters.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activePaperDomain = btn.getAttribute("data-domain");
      filterAndRenderPapers();
    });
  });

  // --- TAB 4: Datasets Rendering & Filtering ---
  let activeDatasetDomain = "All";

  function renderDatasetsList(datasets) {
    if (!datasetsContainer) return;
    datasetsContainer.innerHTML = "";

    const filtered = datasets.filter((d) => {
      if (activeDatasetDomain === "All") return true;
      return d.domain.toLowerCase().includes(activeDatasetDomain.toLowerCase());
    });

    filtered.forEach((d) => {
      const card = document.createElement("div");
      card.className = "dataset-card";

      card.innerHTML = `
        <div>
          <div class="dataset-header">
            <h3 class="dataset-name">${d.name}</h3>
            <span class="dataset-domain-tag">${d.domain}</span>
          </div>

          <div class="dataset-stat-row"><strong>Total Scale:</strong> ${d.samples} &bull; <span style="font-family: var(--font-mono); color: var(--accent-cyan);">${d.storage}</span></div>
          <div class="dataset-stat-row"><strong>Real vs. Fake Balance:</strong> ${d.real_fake_ratio}</div>
          <div class="dataset-stat-row"><strong>Manipulation Generators:</strong> ${d.manipulation_methods}</div>
          <div class="dataset-stat-row"><strong>Recommended Benchmark Split:</strong> ${d.recommended_splits}</div>
          
          <div class="leakage-box">
            <strong>Leakage Prevention Protocol:</strong> ${d.leakage_risks}
          </div>
          <div class="dataset-stat-row" style="margin-top: 8px;"><strong>Known Limitations:</strong> ${d.limitations}</div>
        </div>

        <div class="dataset-verdict-box">
          &bull; <strong>Forensic Utility:</strong> ${d.verdict}
        </div>
      `;

      datasetsContainer.appendChild(card);
    });
  }

  datasetFilters.forEach((btn) => {
    btn.addEventListener("click", () => {
      datasetFilters.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      activeDatasetDomain = btn.getAttribute("data-filter");
      renderDatasetsList(allDatasets);
    });
  });

  // --- TAB 5: Hypotheses Rendering ---
  function renderHypothesesList(hypotheses) {
    if (!hypothesesContainer) return;
    hypothesesContainer.innerHTML = "";

    hypotheses.forEach((h) => {
      const card = document.createElement("div");
      card.className = "hypothesis-card";

      card.innerHTML = `
        <div class="hypo-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span class="hypo-id-badge">Hypothesis ${h.id} (Rank ${h.rank})</span>
            <span class="hypo-status-badge">&check; ${h.status}</span>
          </div>
          <span style="font-size: 0.8rem; color: var(--text-muted); font-family: var(--font-mono);">${h.gap_name}</span>
        </div>

        <h3 class="hypo-title">${h.title}</h3>
        
        <div class="hypo-gap-box">
          <strong>Identified Research Gap:</strong> ${h.gap_description}
        </div>

        <div class="hypo-claim-box">
          <strong>Formal Testable Claim:</strong> "${h.hypothesis}"
        </div>

        <div class="hypo-falsify-box">
          <strong>Disproving Evidence (Falsification Criteria):</strong> ${h.falsification_condition}
        </div>

        <div class="hypo-outcome-box">
          <strong>Empirical Benchmark Outcome:</strong> ${h.empirical_outcome}
        </div>
      `;

      hypothesesContainer.appendChild(card);
    });
  }

  // --- BibTeX Copy Handlers ---
  function copySinglePaperBibTeX(paper) {
    const bib = `@article{${paper.id},
  author    = {${paper.authors}},
  title     = {${paper.title}},
  journal   = {${paper.venue}},
  year      = {${paper.year}},
  url       = {${paper.paper_url}}
}`;
    navigator.clipboard.writeText(bib).then(() => {
      alert(`BibTeX citation copied for: "${paper.title}"`);
    });
  }

  if (btnCopyAllBibtex) {
    btnCopyAllBibtex.addEventListener("click", () => {
      if (bibtexDisplayBlock) {
        navigator.clipboard.writeText(bibtexDisplayBlock.textContent).then(() => {
          alert("Complete BibTeX Library copied to clipboard!");
        });
      }
    });
  }

  if (btnCopyPaperCite) {
    btnCopyPaperCite.addEventListener("click", () => {
      const cite = `@article{deepshield2026,
  author    = {DeepShield AI Research Collective},
  title     = {DeepShield: Codec-Invariant Multimodal Deepfake Detection via Learnable Gabor Residuals and Decoupled Asymmetric Risk Fusion},
  journal   = {IEEE/CVF CVPR / ACM Multimedia Working Preprint},
  year      = {2026}
}`;
      navigator.clipboard.writeText(cite).then(() => {
        alert("DeepShield Preprint BibTeX citation copied to clipboard!");
      });
    });
  }
});
