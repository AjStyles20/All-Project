# Verification Report — Feature 002

## Verifier Role
Independent Verification Agent

## Scope Reviewed
Feature 002: PDF, DOCX, and PPTX ingestion with source provenance, stacked on verified Feature 001 ingestion/retrieval behavior.

## Evidence Inspected
- Feature 002 implementation contract
- updated ingestion module
- updated upload endpoint
- parser dependencies
- Feature 001 regression tests
- new document-format tests
- live Uvicorn upload/search smoke test

## Findings

### V2-001 — PDF provenance
- Valid extractable PDF: PASS
- Retrieved locator: `page 1`
- Live API upload/search: PASS
- Encrypted PDF: explicitly rejected by implementation
- Scanned/image-only PDF OCR: NOT IMPLEMENTED

### V2-002 — DOCX provenance
- Valid DOCX: PASS
- Retrieved locator observed: `paragraph 2`
- Live API upload/search: PASS
- Physical page number is deliberately not claimed because DOCX pagination is not reliably represented by the document XML alone.

### V2-003 — PPTX provenance
- Valid PPTX: PASS
- Retrieved locator: `slide 1`
- Live API upload/search: PASS
- Speaker notes/images/charts are not claimed as extracted.

### V2-004 — Malformed binary documents
- Invalid PDF: controlled extraction failure
- Invalid DOCX: controlled extraction failure
- Invalid PPTX: controlled extraction failure
- Status: PASS

### V2-005 — Feature 001 regression
The expanded file support required updating the old unsupported-file test because PDF is no longer an unsupported type. Unsupported-file coverage now uses an `.exe` input. UTF-8 failure wording was also aligned with the new extraction layer.

Status: PASS after regression update.

## Test Execution
Verifier environment:
- Python runtime: container runtime
- `pypdf`: 5.9.0
- `python-docx`: 1.2.0
- `python-pptx`: 1.0.2
- `fastapi`: 0.128.2
- `httpx`: 0.28.1

Command:
`PYTHONPATH=. pytest -q`

Result:
**21 passed in 0.54s**

## Live API Verification
A Uvicorn server was started against an isolated SQLite database. One workspace was created and three real generated documents were uploaded:
- `evidence.pdf` → HTTP 200, 1 extracted chunk
- `evidence.docx` → HTTP 200, 2 extracted chunks
- `slides.pptx` → HTTP 200, 1 extracted chunk

Search for `rainfall` returned both the PDF (`page 1`) and DOCX (`paragraph 2`) evidence. Search for `provenance` returned the PPTX result with locator `slide 1`.

## Environment Limitation
Direct `git clone` from GitHub failed because the verifier container could not resolve `github.com`. Verification therefore reconstructed the execution copy from exact authenticated-connector branch contents. This is verifier-environment evidence, not user-device verification.

## Verification Decision
**PASS IN VERIFIER ENVIRONMENT — NOT USER VERIFIED.**

Feature 002 meets its bounded acceptance criteria. It must not be described as OCR-capable, layout-preserving, image-aware, or comprehensive for every PDF/DOCX/PPTX construct.
