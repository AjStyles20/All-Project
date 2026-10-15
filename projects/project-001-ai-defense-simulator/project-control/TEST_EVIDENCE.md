# Project 001 Test Evidence

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval

### Verification environment
- Date: 2026-09-08
- Python: 3.13.5
- FastAPI: 0.128.2
- HTTPX: 0.28.1
- pytest: 9.0.2
- SQLite: 3.46.1
- AI provider: not configured

### Source under test
Branch: `p001/feature-document-ingestion-retrieval`

The execution environment could not resolve `github.com` for a direct Git clone. Verification therefore reconstructed the test workspace from the exact branch file contents fetched through the authenticated GitHub connector before execution. This limitation is recorded explicitly; no claim is made that a network Git checkout itself was tested.

### Automated test run
Command:
`python -m pytest -q`

Result:
`14 passed in 0.37s`

Covered behaviors include:
- deterministic chunking
- SHA-256 hash determinism
- overlap/provenance regression
- idempotent SQLite initialization
- FTS5 retrieval
- workspace isolation
- health endpoint
- workspace creation and blank-name rejection
- valid Markdown upload
- unsupported type rejection
- empty upload rejection
- invalid UTF-8 rejection
- oversize rejection
- API search with provenance

### Live API smoke test
Server:
`uvicorn app.main:app --host 127.0.0.1 --port 8765`

Observed flow:
1. `GET /health` -> HTTP 200; application/database available; AI provider `not configured`.
2. `POST /api/workspaces` -> HTTP 200; workspace created.
3. `POST /api/workspaces/{id}/documents` with `sample.md` -> HTTP 200; `EXTRACTED`, one chunk, SHA-256 document hash returned.
4. `GET /api/workspaces/{id}/search?q=provenance` -> HTTP 200; one result returned with `chunk_id`, `document_id`, filename `sample.md`, locator `paragraph 1`, and matching source text.

### Verification status
- Unit/logic tests: PASS
- API integration tests: PASS in verifier environment
- Live API smoke test: PASS in verifier environment
- Browser/UI test: NOT APPLICABLE to Feature 001; no UI implemented yet
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Boundary
This evidence supports Feature 001 only. It does not support claims for PDF/DOCX/PPTX ingestion, semantic retrieval, LLM question generation, answer evaluation, speech, presentation scoring, or UI functionality.
