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

## Feature 013 — Groq Speech-to-Text
- Date: 2026-09-09
- Branch: `p001/feature-groq-transcription`
- Pull request: #14
- GitHub CI: PASS
- CI automated result: `141 passed, 2 warnings in 2.50s`
- CI dependency audit: `No known vulnerabilities found`
- AJ Windows/Python 3.14 regression result: `141 passed, 2 warnings in 71.80s`
- Live browser microphone recording: PASS
- Explicit Stop-without-upload behavior: PASS
- Explicit Transcribe-recording action: PASS
- Live Groq transcription HTTP path: PASS (`POST .../transcriptions` → `200 OK`)
- Transcript inserted into editable answer box: PASS
- Transcript auto-submission: DID NOT OCCUR
- Separate explicit answer submission/evaluation: PASS
- Provider/model displayed in UI: `groq / whisper-large-v3-turbo`
- Raw audio application persistence: not introduced by Feature 013

Observed STT quality issue during the live test: domain terms were imperfectly recognized (`sequence numbers` was rendered as `sequential numbers`; `retransmission timers` was rendered as `transmission timelines`). This is recorded as a transcription-quality limitation rather than an integration failure. The editable review step is therefore a functional safety requirement, not merely a convenience.

Claim boundary: Feature 013 is live-verified for AJ's local browser/device workflow and the tested microphone path. It does not establish universal microphone/browser compatibility, universal transcription accuracy, noisy-environment robustness, or production deployment readiness.

## Feature 014 — Zero-Cost Browser Reviewer TTS
- Date: 2026-09-09
- Branch: `p001/feature-browser-tts`
- Pull request: #15
- GitHub CI: PASS
- CI automated result: `145 passed, 2 warnings in 9.40s`
- CI dependency audit: `No known vulnerabilities found`
- AJ Windows/Python 3.14 regression result: `145 passed, 2 warnings in 59.03s`
- Live local/browser reviewer speech: PASS
- Explicit Listen-to-reviewer start: PASS
- Stop-audio interruption: PASS
- Written reviewer question remained visible/authoritative: PASS
- No additional TTS API key or subscription required for local browser speech: PASS
- Existing server/OpenAI TTS path: PRESERVED

Observed browser speech edge case: one live attempt displayed `Local reviewer speech could not be played. Read the question text above.` after another successful playback attempt. This is tracked as a browser/device speech-engine reliability limitation rather than a failed Feature 014 gate, because AJ independently confirmed successful audible playback and successful Stop-audio interruption on the same local environment.

Claim boundary: Feature 014 is live-verified on AJ's current Windows/browser environment for explicit local speech playback and interruption. It does not establish identical voice availability, quality, pronunciation, or reliability across all browsers/devices.

## Current CI Maintenance Note
The workflow uses `actions/checkout@v5` and `actions/setup-python@v6`. The suite emits two FastAPI/Starlette test-client dependency deprecation warnings; these remain tracked maintenance debt. They are warnings, not failed tests.

## Security / Claim Boundary
This evidence does not establish that Project 001 is hack-proof, production-ready, universally prompt-injection-proof, educationally effective, equivalent to a human examiner, or suitable for high-stakes grading. Public/multi-user authentication, authorization, rate limiting, deployment hardening, OCR, visual understanding, and broad device/browser verification remain outstanding.
