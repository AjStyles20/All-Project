# Project 001 Implementation Status

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Status: INTEGRATION TESTED + LIVE API VERIFIED IN VERIFIER ENVIRONMENT; NOT USER VERIFIED
- Branch: `p001/feature-document-ingestion-retrieval`
- Pull request: #1
- Verification: 14 tests at gate + live Uvicorn smoke test PASS.

## Feature 002 — PDF/DOCX/PPTX Ingestion + Provenance
- Status: INTEGRATION TESTED + LIVE API VERIFIED IN VERIFIER ENVIRONMENT; NOT USER VERIFIED
- Branch: `p001/feature-document-formats`
- Pull request: #2
- Verification: 21 tests at gate + live PDF/DOCX/PPTX upload/search PASS.
- Limitations: no OCR, visual understanding, speaker notes/media extraction, exact layout reconstruction.

## Feature 003 — Secure Hybrid Retrieval Foundation
- Status: CI VERIFIED WITH TEST-ONLY EMBEDDING PROVIDER; REAL SEMANTIC PROVIDER NOT LIVE VERIFIED
- Branch: `p001/feature-hybrid-retrieval`
- Pull request: #3
- Verification: 32 tests PASS; dependency audit reported no known vulnerabilities at verification time.

## Feature 004 — Secure Source-Grounded Question Generation Foundation
- Status: CI VERIFIED WITH TEST-ONLY QUESTION GENERATOR; REAL LLM PROVIDER NOT LIVE VERIFIED
- Branch: `p001/feature-grounded-questioning`
- Pull request: #4
- Verification: 39 tests PASS; dependency audit reported no known vulnerabilities at verification time.

## Feature 005 — Secure Evidence-Aware Answer Evaluation Foundation
- Status: CI VERIFIED WITH TEST-ONLY ANSWER EVALUATOR; REAL AI EVALUATOR NOT LIVE VERIFIED
- Branch: `p001/feature-answer-evaluation`
- Pull request: #5
- Verification: 52 tests PASS; dependency audit reported no known vulnerabilities at verification time.
- Objective overall numeric grading: INTENTIONALLY NOT CLAIMED.

## Feature 006 — Secure Server-Rendered Web Interface
- Status: CI VERIFIED; NOT USER-DEVICE VERIFIED
- Branch: `p001/feature-web-ui`
- Pull request: #6
- Verification: 59 tests PASS; dependency audit reported no known vulnerabilities at verification time.

## Feature 007 — Optional Real Provider Adapter
- Status: CI VERIFIED WITH MOCKED HTTP; LIVE AUTHENTICATED PROVIDER NOT VERIFIED
- Branch: `p001/feature-real-provider-adapter`
- Pull request: #7 — READY FOR REVIEW
- Implemented: environment-only OpenAI configuration, fixed outbound API base, embeddings/question/evaluation adapters, no-tool calls, `store: false`, structured evaluation output, bounded provider errors/timeouts.
- Verification: 70 tests PASS; dependency audit reported no known vulnerabilities at verification time.
- API secret: NOT STORED IN SOURCE/UI/DB.

## Feature 008 — Bounded Multi-Turn Defense Sessions
- Status: CI VERIFIED WITH TEST-ONLY FOLLOW-UP PROVIDER; REAL FOLLOW-UP PROVIDER NOT LIVE VERIFIED
- Branch: `p001/feature-multiturn-defense`
- Pull request: #8 — READY FOR REVIEW
- Implemented: workspace-scoped sessions, ordered turns, parent linkage, answer-before-follow-up gate, authoritative provenance reconstruction, fixed follow-up types, max-turn enforcement, explicit completion, session API/UI, optional OpenAI follow-up adapter.
- Final verification: 82 tests PASS on checked-out PR merge ref; dependency audit reported no known vulnerabilities at verification time.
- AJ-device/browser verification: NOT RUN.

## Feature 009 — Secure Microphone / Speech Input
- Status: CI VERIFIED WITH TEST-ONLY + MOCKED TRANSCRIPTION PROVIDERS; REAL MICROPHONE/PROVIDER NOT LIVE VERIFIED
- Branch: `p001/feature-speech-input`
- Pull request: #9
- Implemented:
  - provider-neutral `SpeechTranscriber` interface;
  - bounded audio validation with 10 MiB maximum;
  - explicit audio media-type allowlist;
  - bounded transcript validation at 8000 characters;
  - workspace/question-scoped transcription endpoint;
  - explicit HTTP 503 when transcription is not configured;
  - optional server-side OpenAI transcription adapter using fixed `/audio/transcriptions` endpoint;
  - provider secret remains environment-only;
  - raw provider error bodies are not propagated;
  - no raw-audio persistence path or audio table;
  - external `speech.js` compatible with the restrictive CSP;
  - same-origin microphone permission only in the configured app entrypoint; camera/geolocation remain disabled;
  - explicit browser flow: Start recording -> Stop -> Transcribe recording -> Review/Edit transcript -> Submit for feedback;
  - Cancel discards captured audio;
  - hard 120-second browser recording limit;
  - microphone access occurs only inside the explicit Start button handler;
  - Stop does not transmit audio;
  - Transcribe is a separate explicit network-consent action;
  - returned transcript only fills the answer textarea and never auto-submits or auto-evaluates;
  - text answer path remains available.
- Verification evidence:
  - GitHub Actions checked-out PR merge ref: PASS;
  - final run ID: `34207981904`;
  - checked-out merge ref: `6b66dfaf3d55ac4806389928dd433a92766229fb`;
  - Ubuntu 24.04 / Python 3.12.14 compile check: PASS;
  - full regression + Feature 009 suite: `95 passed, 2 warnings in 2.30s`;
  - provider-not-configured behavior: PASS;
  - cross-workspace question rejection: PASS;
  - media type and upload size bounds: PASS;
  - no audio persistence: PASS;
  - no automatic microphone invocation: PASS;
  - no automatic form submission/evaluation: PASS;
  - mocked fixed-endpoint multipart provider call: PASS;
  - provider-secret/raw-error non-disclosure: PASS;
  - dependency audit: no known vulnerabilities found at verification time.
- Explicit limitations:
  - no real microphone/browser device verification has been run;
  - no authenticated external transcription request has been run;
  - browser codec compatibility is not yet user-device verified;
  - realtime streaming transcription is not implemented;
  - no emotion/confidence/accent/pronunciation/identity scoring;
  - speech output/TTS is not yet implemented.

## Current Product Boundary
The application now supports a bounded source-grounded practice workflow with document provenance, retrieval, reviewer questions, text answers, evidence-aware qualitative feedback, multi-turn challenge sessions, and an optional review-before-submit speech-input path. Real provider adapters exist but are live only after explicit secure environment configuration and credentialed verification.

## Still Not Implemented / Not Live Verified
- authenticated live external AI/transcription verification
- AJ-device/browser/microphone verification
- speech output / TTS
- delivery analysis
- authentication/multi-user authorization
- public deployment hardening/rate limiting/session security
- OCR for scanned PDFs
- image/chart/diagram understanding

## Important Boundary
Passing tests and dependency audits do not establish that the product is hack-proof, production-ready, universally prompt-injection-proof, or suitable for high-stakes grading. Security remains a continuing release gate.