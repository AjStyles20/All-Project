# Project 001 Implementation Status

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Status: IMPLEMENTED — SELF-TESTED, NOT INDEPENDENTLY VERIFIED
- Branch: `p001/feature-document-ingestion-retrieval`
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
  - initial automated tests
- Not implemented:
  - PDF/DOCX/PPTX parsers
  - semantic embeddings/hybrid merge
  - LLM question generation
  - answer evaluation
  - speech services
  - server-rendered UI screens
- Self-test evidence:
  - deterministic chunk/hash logic exercised
  - repeated SQLite initialization exercised
  - FTS5 known-query retrieval exercised
  - workspace isolation exercised
- Independent verification: NOT RUN
- Live browser/API verification: NOT RUN
- User verification: NOT RUN

## Important Boundary
No external AI provider is configured. The system must not display or document AI question generation, answer evaluation, speech input/output, PDF/DOCX/PPTX support, or semantic retrieval as implemented.
