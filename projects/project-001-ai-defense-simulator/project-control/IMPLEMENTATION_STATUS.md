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
- Environment limitation:
  - verifier container could not resolve GitHub for direct `git clone`; exact authenticated branch contents were reconstructed locally for execution.
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Still Not Implemented
- semantic embeddings/hybrid merge
- LLM question generation
- answer evaluation
- speech services
- server-rendered UI screens
- authentication/multi-user behavior

## Important Boundary
No external AI provider is configured. The system must not display or document semantic retrieval, AI question generation, answer evaluation, speech input/output, OCR, complex visual document understanding, or UI completion as implemented.
