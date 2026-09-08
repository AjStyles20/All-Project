# Project 001 Implementation Status

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Status: INTEGRATION TESTED + LIVE API VERIFIED IN VERIFIER ENVIRONMENT; NOT USER VERIFIED
- Branch: `p001/feature-document-ingestion-retrieval`
- Pull request: #1
- Scope implemented:
  - FastAPI application skeleton
  - SQLite schema initialization
  - workspace creation
  - UTF-8 TXT/Markdown upload path
  - deterministic paragraph-aware chunking
  - SHA-256 document/chunk hashes
  - chunk provenance metadata
  - SQLite FTS5 lexical retrieval
  - workspace-scoped search
  - automated logic tests
  - FastAPI API integration tests
- Verification evidence:
  - deterministic chunk/hash logic: PASS
  - overlap/provenance regression: PASS
  - repeated SQLite initialization: PASS
  - FTS5 known-query retrieval: PASS
  - workspace isolation: PASS
  - API integration suite: PASS
  - full verifier-environment suite at Feature 001 gate: 14 passed in 0.37s
  - live Uvicorn workspace/upload/search smoke test: PASS
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Feature 002 — PDF/DOCX/PPTX Ingestion + Provenance
- Status: INTEGRATION TESTED + LIVE API VERIFIED IN VERIFIER ENVIRONMENT; NOT USER VERIFIED
- Branch: `p001/feature-document-formats`
- Scope implemented:
  - PDF text extraction with page provenance
  - DOCX paragraph extraction with paragraph-order provenance
  - PPTX slide-text extraction with slide provenance
  - malformed accepted-format input fails explicitly
  - encrypted PDFs rejected explicitly
  - Feature 001 TXT/Markdown behavior retained
  - existing FTS5 workspace-scoped retrieval reused
- Verification evidence:
  - PDF direct extraction + page locator: PASS
  - DOCX direct extraction + paragraph locator: PASS
  - PPTX direct extraction + slide locator: PASS
  - malformed PDF/DOCX/PPTX: PASS controlled failure
  - API upload/search for all three formats: PASS
  - Feature 001 regression suite: PASS
  - combined verifier-environment suite: 21 passed in 0.54s
  - live Uvicorn PDF/DOCX/PPTX upload + search: PASS
- Explicit limitations:
  - OCR for scanned/image-only PDFs: NOT IMPLEMENTED
  - images/charts/diagrams extraction: NOT IMPLEMENTED
  - PPTX speaker notes/embedded media extraction: NOT IMPLEMENTED
  - DOCX physical page reconstruction: NOT CLAIMED
  - password-protected Office documents: NOT VERIFIED
  - exact layout reconstruction: NOT IMPLEMENTED
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Feature 003 — Secure Hybrid Retrieval Foundation
- Status: CI VERIFIED WITH TEST-ONLY EMBEDDING PROVIDER; REAL SEMANTIC PROVIDER NOT LIVE VERIFIED
- Branch: `p001/feature-hybrid-retrieval`
- Pull request: #3
- Scope implemented:
  - `EmbeddingProvider` abstraction
  - strict finite/vector-dimension validation
  - workspace-scoped SQLite embedding storage
  - provider/model/version/content-hash metadata
  - stale-embedding detection and recomputation
  - cosine semantic similarity
  - explainable reciprocal-rank-fusion style lexical/semantic merge
  - explicit lexical-only fallback when no semantic provider is configured
  - retrieval component metadata in API responses
  - input bounds for workspace names, filenames, search query length, result count, vector dimension and semantic chunk scan
  - cross-workspace embedding write rejection
  - CI compile/test/dependency-audit gate
- Verification evidence:
  - GitHub Actions checked-out PR merge ref: PASS
  - Python 3.12 compile check: PASS
  - full regression + Feature 003 suite: 32 passed
  - workspace isolation tests: PASS
  - stale embedding test: PASS
  - malformed/non-finite/dimension mismatch vector tests: PASS
  - explicit no-provider lexical fallback test: PASS
  - dependency audit (`pip-audit -r requirements.txt`): no known vulnerabilities found at verification time
  - CI workflow completed successfully after updating to Node-24-based action majors
- Explicit limitations:
  - no real embedding provider/model is configured
  - semantic retrieval is NOT LIVE VERIFIED against an external/local production provider
  - fake deterministic vectors exist only in tests and must not be represented as production embeddings
  - hybrid weights are implementation defaults, not empirically optimal
  - authentication/multi-user authorization remains unimplemented
  - public-deployment hardening remains incomplete
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Still Not Implemented
- real configured semantic embedding provider/model
- grounded LLM question generation
- answer evaluation / evidence-aware feedback
- speech services
- server-rendered UI screens
- authentication/multi-user behavior

## Important Boundary
No external AI or embedding provider is configured. The application must not represent semantic retrieval as live when it is operating in lexical-only fallback mode. It must not display or document AI question generation, answer evaluation, speech input/output, OCR, complex visual document understanding, authentication, or public-deployment security as implemented.
