# Project 001 Test Evidence

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Date: 2026-09-08
- Branch: `p001/feature-document-ingestion-retrieval`
- Verifier environment: Python 3.13.5, FastAPI 0.128.2, HTTPX 0.28.1, pytest 9.0.2, SQLite 3.46.1
- Automated result: `14 passed in 0.37s`
- Live Uvicorn workspace/upload/search smoke test: PASS
- User-device/runtime verification: NOT RUN

Covered deterministic chunking, hash determinism, overlap/provenance regression, idempotent schema initialization, FTS5 retrieval, workspace isolation, upload validation, API search and provenance.

## Feature 002 — PDF/DOCX/PPTX Ingestion
- Date: 2026-09-08
- Branch: `p001/feature-document-formats`
- Combined regression + format suite: `21 passed in 0.54s`
- Live Uvicorn PDF/DOCX/PPTX upload/search: PASS in verifier environment
- Verified locators: PDF page, DOCX paragraph order, PPTX slide
- Controlled malformed-file failures: PASS
- Encrypted PDF rejection: PASS
- User-device/runtime verification: NOT RUN

Not covered/claimed: OCR, visual understanding, PPTX speaker notes/media, exact DOCX/PPTX layout reconstruction.

## Feature 003 — Secure Hybrid Retrieval Foundation
- Date: 2026-09-08
- Branch: `p001/feature-hybrid-retrieval`
- GitHub Actions checked-out PR merge ref: PASS
- Runner: Ubuntu 24.04
- Python: 3.12.14
- Compile check: PASS
- Automated result: `32 passed`
- Dependency audit: `No known vulnerabilities found`
- Test-only embedding provider only; real semantic provider/model NOT LIVE VERIFIED

Covered no-provider lexical fallback, workspace isolation, vector validation, non-finite/dimension mismatch rejection, stale embedding detection/re-indexing, hybrid merge behavior, cross-workspace embedding write rejection and provenance preservation.

## Feature 004 — Secure Source-Grounded Question Generation Foundation
- Date: 2026-09-08
- Branch: `p001/feature-grounded-questioning`
- GitHub Actions checked-out PR merge ref: PASS
- Runner: Ubuntu 24.04
- Python: 3.12.14
- Compile check: PASS
- Automated result: `39 passed, 2 warnings in 1.30s`
- Dependency audit: `No known vulnerabilities found`
- Test-only question generator only; real LLM provider/model NOT LIVE VERIFIED

Covered reviewer-role allowlist, trusted-policy/evidence separation, prompt-injection fixture, source/evidence provenance persistence, cross-workspace evidence ownership rejection, bounded provider output and explicit provider-not-configured behavior.

Security correction discovered during development: the first persistence path checked target-workspace existence but did not independently prove every evidence chunk belonged to it. A regression test exposed this; authoritative evidence ownership validation was added before persistence.

## Feature 005 — Secure Evidence-Aware Answer Evaluation Foundation
- Date: 2026-09-08
- Branch: `p001/feature-answer-evaluation`
- Pull request: #5
- GitHub Actions workflow: `Project 001 CI`
- Verification run ID: `34201364045`
- Runner: Ubuntu 24.04
- Python: 3.12.14
- Compile check: PASS
- Automated result: `52 passed, 2 warnings in 1.64s`
- Dependency audit: `No known vulnerabilities found`
- Test-only question/evaluation providers only; real AI evaluation NOT LIVE VERIFIED

Covered question/workspace ownership, authoritative evidence reconstruction, provenance-tampering rejection, prompt/instruction separation, fixed qualitative rubric, invalid category/status/evidence-reference rejection, bounded input/output/provider metadata, persistence integrity, provider-not-configured behavior, and the complete FastAPI document -> question -> answer -> feedback loop using test-only providers.

## Feature 006 — First Usable Secure Server-Rendered Web UI
- Date: 2026-09-08
- Branch: `p001/feature-web-ui`
- Pull request: #6
- GitHub Actions workflow: `Project 001 CI`
- Verification run ID: `34202171058`
- Runner: Ubuntu 24.04
- Python: 3.12.14
- Checked-out source: PR #6 merge ref
- Compile check: PASS
- Automated result: `59 passed, 2 warnings in 1.92s`
- Dependency audit: `No known vulnerabilities found`
- AJ device/browser verification: NOT RUN

Covered:
- home-page rendering;
- workspace creation through server-rendered form;
- document upload through UI;
- evidence search with visible filename/locator/source provenance;
- script-like uploaded content is HTML-escaped and not rendered as executable markup in tested output;
- restrictive CSP and security-header checks;
- cross-origin/cross-site unsafe browser mutation rejection;
- API docs disabled by default;
- truthful configured/not-configured AI capability states;
- full server-rendered document -> question -> answer -> qualitative-feedback flow using explicit test-only providers;
- cross-workspace question URL isolation;
- existing Feature 001–005 regression suite remains passing.

Accessibility foundations checked at implementation/test level include semantic headings/landmarks, explicit labels, native keyboard-operable controls, textual statuses, visible focus styling, and provenance that does not require hover. This is not a full screen-reader/device accessibility certification.

## Current CI Maintenance Note
The workflow uses `actions/checkout@v5` and `actions/setup-python@v6`. The pytest suite still emits two dependency deprecation warnings in the FastAPI/Starlette test-client path; these are tracked maintenance debt rather than silently accepted permanent state.

## Security / Claim Boundary
This evidence does not establish that Project 001 is hack-proof, production-ready, universally prompt-injection-proof, or suitable for high-stakes grading. No real embedding/question/evaluation provider is currently configured. The browser UI is verified in CI/TestClient, not yet on AJ's Windows/browser environment. Public/multi-user security, authentication/authorization, full session-bound CSRF controls, deployment hardening, speech, OCR, visual understanding, and user-device verification remain outstanding.
