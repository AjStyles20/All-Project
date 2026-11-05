# P011 technology selection (PROJECT_RULES §21)

Follows `ARCHITECTURE_PROPOSAL.md`, with the deviations noted.

| Item | Choice | Note |
|---|---|---|
| Platform | Local web application | As proposed. |
| Backend | Python + FastAPI | As proposed. |
| Frontend | Plain HTML/CSS/JS reading a JSON API | Proposal said server-rendered templates; this matches the other Project OS apps and needs no template engine. |
| Database | SQLite | As proposed. |
| Retrieval | SQLite FTS5 (bm25) only | Semantic embeddings left out: no provider chosen. |
| Ingestion | TXT/MD, DOCX and PPTX via the standard library (zip + XML, DTDs refused); PDF via pypdf (BSD) | Upload limits: 10 MB, 2,000 zip entries, 50 MB expanded. |
| Question generation | Deterministic rules (`analysis.py`, `reviewers.py`) | Proposal assumed an LLM behind a `QuestionGenerator` interface; none is configured, so nothing is described as AI-generated. |
| Answer feedback | Criterion checks marked "source" or "heuristic" | No score (P001-C004 remains unsupported). |
| Speech | Not implemented | FR-007/FR-008 remain unavailable, not simulated. |
