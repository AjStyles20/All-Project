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
- Not implemented:
  - PDF/DOCX/PPTX parsers
  - semantic embeddings/hybrid merge
  - LLM question generation
  - answer evaluation
  - speech services
  - server-rendered UI screens
- Verification evidence:
  - deterministic chunk/hash logic: PASS
  - overlap/provenance regression: PASS
  - repeated SQLite initialization: PASS
  - FTS5 known-query retrieval: PASS
  - workspace isolation: PASS
  - API integration suite: PASS
  - full verifier-environment suite: 14 passed in 0.37s
  - live Uvicorn workspace/upload/search smoke test: PASS
- Environment limitation:
  - verifier container could not resolve GitHub for direct `git clone`; exact branch files were fetched through the authenticated connector and reconstructed locally for execution.
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Important Boundary
No external AI provider is configured. The system must not display or document AI question generation, answer evaluation, speech input/output, PDF/DOCX/PPTX support, semantic retrieval, or UI completion as implemented.
