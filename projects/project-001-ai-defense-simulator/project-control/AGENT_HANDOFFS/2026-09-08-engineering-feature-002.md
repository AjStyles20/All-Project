# Agent Handoff

## Workstream
Engineering / Document Processing

## Task
Feature 002 — PDF/DOCX/PPTX ingestion with source provenance.

## Starting Project State
Feature 001 was integration tested and live API verified in the verifier environment. PDF/DOCX/PPTX support was explicitly not implemented.

## Files Inspected
- `app/ingestion.py`
- `app/main.py`
- `tests/test_api.py`
- `tests/test_ingestion.py`
- `requirements.txt`
- Feature 001 verification/status records

## Files Changed / Added
- `app/ingestion.py`
- `app/main.py`
- `requirements.txt`
- `tests/test_api.py`
- `tests/test_document_formats.py`
- `docs/technical/FEATURE_002_DOCUMENT_FORMATS_CONTRACT.md`
- `verification/FEATURE_002_VERIFICATION_REPORT.md`
- `project-control/IMPLEMENTATION_STATUS.md`

## Implemented
- PDF extraction via `pypdf` with page locators.
- DOCX extraction via `python-docx` with paragraph locators.
- PPTX extraction via `python-pptx` with slide locators.
- Common extractor dispatch for TXT/MD/PDF/DOCX/PPTX.
- Controlled malformed-document failure.
- Explicit encrypted-PDF rejection.
- API integration coverage for the three new formats.

## Not Implemented
- OCR/scanned PDF support.
- Image/chart/diagram extraction.
- PPTX notes/media extraction.
- DOCX physical pagination.
- Semantic retrieval.
- LLM question generation/evaluation.
- Speech/UI.

## Tests
- Combined regression + Feature 002 suite: PASS — 21 tests.
- Live Uvicorn upload/search with PDF, DOCX, PPTX: PASS.
- User-device verification: NOT RUN.

## Issues / Assumptions
- Binary-format libraries are new dependencies and must be installed on the target environment.
- Complex document structures may expose parser limitations not covered by the current fixtures.
- DOCX paragraph order is a truthful structural locator; page number is deliberately not inferred.
- Scanned PDF without embedded text will produce no extractable chunks and should not be described as OCR failure/recovery support.

## Architecture Changes
None. This is a bounded extension of the approved document-ingestion interface.

## Claims Affected
- PDF/DOCX/PPTX text ingestion may now be described as implemented and verifier-environment tested within the documented limitations.
- OCR, visual understanding, and complex-layout fidelity remain unsupported.

## Decisions Awaiting AJ
None for Feature 002. The next significant design decision is whether Feature 003 should introduce semantic retrieval before LLM question generation.

## Recommended Next Agent
Project Lead + Architect should review retrieval quality needs. Verification should keep Feature 002 stacked until Feature 001 base PR handling is resolved.