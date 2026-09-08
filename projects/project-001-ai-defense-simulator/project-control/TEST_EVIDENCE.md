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

## Feature 007 — Optional Real Provider Adapter
- Date: 2026-09-08
- Branch: `p001/feature-real-provider-adapter`
- Pull request: #7
- Automated result: `70 passed, 2 warnings in 2.93s`
- Dependency audit: `No known vulnerabilities found`
- HTTP provider behavior verified with mocked transport only.
- Real authenticated provider call: NOT RUN

## Feature 008 — Bounded Multi-Turn Defense Sessions
- Date: 2026-09-08
- Branch: `p001/feature-multiturn-defense`
- Pull request: #8
- Final verification run ID: `34206784750`
- Final checked-out PR merge ref: `c5c04e2bd0b9f7cb4d2d319e6cee82ef010b6f00`
- Automated result: `82 passed, 2 warnings in 2.23s`
- Dependency audit: `No known vulnerabilities found`
- Real authenticated follow-up provider call: NOT RUN
- AJ device/browser verification: NOT RUN

## Feature 009 — Secure Microphone / Speech Input
- Date: 2026-09-08
- Branch: `p001/feature-speech-input`
- Pull request: #9
- GitHub Actions workflow: `Project 001 CI`
- Final verification run ID: `34207981904`
- Checked-out PR merge ref: `6b66dfaf3d55ac4806389928dd433a92766229fb`
- Runner: Ubuntu 24.04
- Python: 3.12.14
- Compile check: PASS
- Automated result: `95 passed, 2 warnings in 2.30s`
- Dependency audit: `No known vulnerabilities found`
- Real authenticated transcription call: NOT RUN
- Real browser/microphone recording: NOT RUN

Covered:
- provider-neutral speech-transcription interface;
- 10 MiB server-side audio bound;
- explicit audio media-type allowlist;
- 8000-character transcript bound;
- provider-not-configured HTTP 503 behavior;
- workspace/question scoping for transcription requests;
- cross-workspace question rejection;
- unsupported media-type rejection;
- oversize rejection before provider invocation;
- no raw-audio database persistence path/table;
- transcript response explicitly marks `submitted_as_answer=false` and `audio_persisted=false`;
- mocked fixed OpenAI `/audio/transcriptions` multipart request;
- provider HTTP error handling does not expose raw upstream body or API key;
- invalid provider JSON fails closed;
- server configuration keeps secrets outside source/UI/database;
- external JavaScript only; restrictive CSP remains compatible;
- microphone API invocation occurs only inside explicit Start-recording handler;
- 120-second browser recording bound;
- Cancel discards captured data;
- Stop does not transmit audio;
- separate Transcribe-recording action controls network upload;
- transcript fills the answer textarea for review/editing;
- JavaScript contains no form `.submit()` or `requestSubmit()` path;
- text-answer workflow and Features 001–008 regressions remain passing.

Development-test correction recorded: an initial UI regression test incorrectly treated feature detection (`navigator.mediaDevices.getUserMedia` reference) as a microphone invocation. The application behavior was correct; the test was corrected to assert the awaited `getUserMedia` invocation occurs after the explicit Start-button handler begins. The final gate then passed.

## Current CI Maintenance Note
The workflow uses `actions/checkout@v5` and `actions/setup-python@v6`. The suite emits two FastAPI/Starlette test-client dependency deprecation warnings; these remain tracked maintenance debt.

## Security / Claim Boundary
This evidence does not establish that Project 001 is hack-proof, production-ready, universally prompt-injection-proof, educationally effective, equivalent to a human examiner, or suitable for high-stakes grading. It does not establish real microphone/browser compatibility or live external transcription quality. Public/multi-user authentication, authorization, rate limiting, deployment hardening, speech output, OCR, visual understanding, and AJ-device/browser verification remain outstanding.