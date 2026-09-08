# Agent Handoff

## Workstream
Engineering / Backend

## Task
Feature 001 — Document ingestion + provenance-aware lexical retrieval.

## Starting Project State
Architecture proposed and awaiting AJ approval. Research gap provisionally accepted around source-grounded, evidence-traceable review.

## Files Inspected
- `project-control/PROJECT_STATE.md`
- `project-control/REQUIREMENTS.md`
- `docs/technical/ARCHITECTURE_PROPOSAL.md`
- Project root structure

## Files Changed / Added
- `project-control/DECISIONS.md`
- `project-control/IMPLEMENTATION_STATUS.md`
- `docs/technical/FEATURE_001_INGESTION_RETRIEVAL_CONTRACT.md`
- `requirements.txt`
- `app/__init__.py`
- `app/ingestion.py`
- `app/db.py`
- `app/main.py`
- `tests/test_ingestion.py`

## Implemented
- Architecture approval recorded.
- FastAPI application skeleton.
- SQLite persistence and idempotent schema creation.
- Workspace creation.
- TXT/Markdown ingestion with validation.
- Deterministic paragraph-aware chunking.
- SHA-256 source/chunk hashes.
- Provenance fields for stored/retrieved chunks.
- SQLite FTS5 lexical retrieval scoped to workspace.
- Initial tests for deterministic chunking, hashes, DB initialization, retrieval relevance, and workspace isolation.

## Not Implemented
- PDF/DOCX/PPTX parsing.
- Embeddings/semantic retrieval.
- LLM question generation.
- Answer evaluation.
- STT/TTS.
- UI screens.
- Authentication/multi-user behavior.

## Tests
- Logic-level self-test: PASS for chunking, repeat DB initialization, FTS5 known-query retrieval, and workspace isolation.
- Repository pytest suite: NOT YET RUN in a checked-out branch environment.
- API integration tests: NOT YET RUN.
- Live browser verification: NOT RUN.
- Independent Verification Agent: NOT RUN.

## Issues / Assumptions
- SQLite build must support FTS5; common modern Python SQLite builds do, but Verification must confirm the target runtime.
- Search query syntax currently passes through to SQLite FTS5; malformed FTS queries are converted to HTTP 422 rather than silently rewritten.
- Text decoding is deliberately UTF-8 only for this slice; encoding auto-detection is not claimed.

## Architecture Changes
None. Implementation follows the approved proposal.

## Claims Affected
No product-performance or novelty claims are upgraded by this implementation.

## Documentation Requiring Update
- Project state after independent verification.
- Technical API reference after endpoint behavior is verified.

## Decisions Awaiting AJ
None for Feature 001 implementation. Future semantic retrieval/provider selection remains open.

## Recommended Next Agent
Independent Verification Agent. It should challenge upload validation, database idempotency, provenance correctness, workspace isolation, FTS query behavior, and API error handling before merge/verification.
