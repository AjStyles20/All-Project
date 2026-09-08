# Project 001 Test Evidence

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Date: 2026-09-08
- Branch: `p001/feature-document-ingestion-retrieval`
- Automated result: `14 passed in 0.37s`
- Live Uvicorn workspace/upload/search smoke test: PASS
- User-device/runtime verification: NOT RUN

## Feature 002 — PDF/DOCX/PPTX Ingestion
- Date: 2026-09-08
- Branch: `p001/feature-document-formats`
- Combined regression + format suite: `21 passed in 0.54s`
- Live Uvicorn PDF/DOCX/PPTX upload/search: PASS in verifier environment
- User-device/runtime verification: NOT RUN

## Feature 003 — Secure Hybrid Retrieval Foundation
- Date: 2026-09-08
- Branch: `p001/feature-hybrid-retrieval`
- Automated result: `32 passed`
- Dependency audit: `No known vulnerabilities found`
- Real semantic provider/model: NOT LIVE VERIFIED

## Feature 004 — Secure Source-Grounded Question Generation Foundation
- Date: 2026-09-08
- Branch: `p001/feature-grounded-questioning`
- Automated result: `39 passed`
- Dependency audit: `No known vulnerabilities found`
- Real LLM provider/model: NOT LIVE VERIFIED

## Feature 005 — Secure Evidence-Aware Answer Evaluation Foundation
- Date: 2026-09-08
- Branch: `p001/feature-answer-evaluation`
- Automated result: `52 passed`
- Dependency audit: `No known vulnerabilities found`
- Real AI evaluation: NOT LIVE VERIFIED

## Feature 006 — Secure Server-Rendered Web UI
- Date: 2026-09-08
- Branch: `p001/feature-web-ui`
- Pull request: #6
- Verification run ID: `34202171058`
- Automated result: `59 passed, 2 warnings in 1.92s`
- Dependency audit: `No known vulnerabilities found`
- AJ device/browser verification: NOT RUN

Covered server-rendered workspace/document/search/question/answer/feedback flows, escaped untrusted output, security headers/CSP, cross-origin mutation rejection, provider status disclosure, provenance display, and cross-workspace question isolation.

## Feature 007 — Optional Real Provider Adapter
- Date: 2026-09-08
- Branch: `p001/feature-real-provider-adapter`
- Pull request: #7
- Automated result: `70 passed, 2 warnings in 2.93s`
- Dependency audit: `No known vulnerabilities found`
- HTTP provider behavior verified with mocked transport only.
- Real authenticated provider call: NOT RUN

Covered disabled-by-default environment configuration, missing-secret failure, fixed provider endpoint, no-tool requests, `store: false`, structured evaluation schema, embedding validation, timeout/error handling, and secret-leak regression checks.

## Feature 008 — Bounded Multi-Turn Defense Sessions
- Date: 2026-09-08
- Branch: `p001/feature-multiturn-defense`
- Pull request: #8
- GitHub Actions workflow: `Project 001 CI`
- Verification run ID: `34206342071`
- Checked-out source: PR #8 merge ref `f195136bb5e5f7c4781aba93f9fb18e758a17a26`
- Runner: Ubuntu 24.04
- Python: 3.12.14
- Compile check: PASS
- Automated result: `82 passed, 2 warnings in 2.11s`
- Dependency audit: `No known vulnerabilities found`
- Real authenticated follow-up provider call: NOT RUN
- AJ device/browser verification: NOT RUN

Covered:
- workspace-scoped practice-session creation;
- ordered turn persistence and parent-question linkage;
- authoritative question/evidence provenance reconstruction;
- cross-workspace session-history rejection;
- answer/evaluation prerequisite before follow-up generation;
- hard maximum-turn enforcement;
- explicit completed-session termination;
- fixed follow-up-type allowlist;
- prompt/instruction separation for prior answers, feedback and evidence;
- OpenAI follow-up adapter with strict JSON-schema output;
- no tools/actions and `store: false` in mocked provider request;
- malformed provider JSON fails closed;
- API start -> answer/evaluate -> follow-up -> history integration with test-only providers;
- session-page rendering code compiles with the full application stack;
- Feature 001–007 regression suite remains passing.

## Current CI Maintenance Note
The workflow uses `actions/checkout@v5` and `actions/setup-python@v6`. The suite emits two FastAPI/Starlette test-client dependency deprecation warnings; these remain tracked maintenance debt.

## Security / Claim Boundary
This evidence does not establish that Project 001 is hack-proof, production-ready, universally prompt-injection-proof, educationally effective, equivalent to a human examiner, or suitable for high-stakes grading. Real external AI behavior is not live verified. Public/multi-user authentication, authorization, rate limiting, deployment hardening, speech, OCR, visual understanding, and AJ-device/browser verification remain outstanding.