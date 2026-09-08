# Project 001 Test Evidence

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Date: 2026-09-08
- Automated result: `14 passed in 0.37s`
- Live Uvicorn workspace/upload/search smoke test: PASS

## Feature 002 — PDF/DOCX/PPTX Ingestion
- Date: 2026-09-08
- Automated result: `21 passed in 0.54s`
- Live PDF/DOCX/PPTX upload/search: PASS in verifier environment

## Feature 003 — Secure Hybrid Retrieval Foundation
- Automated result: `32 passed`
- Dependency audit: `No known vulnerabilities found`

## Feature 004 — Secure Source-Grounded Question Generation
- Automated result: `39 passed`
- Dependency audit: `No known vulnerabilities found`

## Feature 005 — Evidence-Aware Answer Evaluation
- Automated result: `52 passed`
- Dependency audit: `No known vulnerabilities found`

## Feature 006 — Secure Server-Rendered Web UI
- Verification run ID: `34202171058`
- Automated result: `59 passed, 2 warnings in 1.92s`
- Dependency audit: `No known vulnerabilities found`

## Feature 007 — Optional Real Provider Adapter
- Automated result: `70 passed, 2 warnings in 2.93s`
- Dependency audit: `No known vulnerabilities found`
- Real authenticated provider call: NOT RUN

## Feature 008 — Bounded Multi-Turn Defense Sessions
- Final verification run ID: `34206784750`
- Automated result: `82 passed, 2 warnings in 2.23s`
- Dependency audit: `No known vulnerabilities found`

## Feature 009 — Secure Microphone / Speech Input
- Final verification run ID: `34207981904`
- Checked-out PR merge ref: `6b66dfaf3d55ac4806389928dd433a92766229fb`
- Automated result: `95 passed, 2 warnings in 2.30s`
- Dependency audit: `No known vulnerabilities found`
- Real authenticated transcription/browser microphone verification: NOT RUN

## Feature 010 — Optional Reviewer Speech Output
- Verification run ID: `34210980562`
- Checked-out PR merge ref: `58894f845cea5aa0beb632ee5f7e7ab02c604702`
- Automated result: `106 passed, 2 warnings in 2.28s`
- Dependency audit: `No known vulnerabilities found`
- Real authenticated TTS/browser playback verification: NOT RUN

## Feature 011 — End-to-End Rehearsal Experience
- Date: 2026-09-08
- Branch: `p001/feature-rehearsal-experience`
- Pull request: #11
- Verification run ID: `34244019212`
- Checked-out PR merge ref: `bb68a0e853a23157fbf7bb9f8034aca0b1e7e022`
- Runner: Ubuntu 24.04.5
- Python: 3.12.14
- Compile check: PASS
- Automated result: `115 passed, 2 warnings in 8.26s`
- Dependency audit: `No known vulnerabilities found`
- AJ-device/browser rehearsal: NOT RUN
- Live authenticated external provider verification: NOT RUN

Feature 011 coverage includes:
- direct session-start -> first-turn navigation;
- authoritative workspace/session/question association checks;
- turn/max-turn progress rendering;
- cross-workspace session-question URL tampering rejection;
- session-scoped answer/evaluation navigation;
- feedback review + continue-session link;
- direct follow-up -> new-turn navigation;
- current-turn/generated-turn/answered-turn session state;
- automatic terminal completion when the final configured turn is answered;
- rejection of additional follow-up after completion;
- idempotent completion reconciliation;
- complete Features 001–010 regression suite.

Development correction: the first Feature 011 CI run produced `114 passed, 1 failed` because an older Feature 008 regression expected a `maximum` error after the final answered turn. Feature 011 intentionally promotes that state to the truthful terminal state `session is complete`. The stale test expectation was updated; application behavior was retained; the final gate then passed 115 tests.

## Current CI Maintenance Note
The suite still emits two FastAPI/Starlette test-client dependency deprecation warnings. These are tracked maintenance debt rather than passing security claims.

## Security / Claim Boundary
This evidence does not establish that Project 001 is hack-proof, production-ready, universally prompt-injection-proof, educationally effective, equivalent to a human examiner, or suitable for high-stakes grading. It does not establish AJ-device/browser compatibility or live external AI/transcription/TTS quality. Authentication, multi-user authorization, public deployment hardening, rate limiting, OCR and visual understanding remain outstanding.
