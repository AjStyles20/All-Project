# Project 001 Implementation Status

## Feature 001 — Document Ingestion + Provenance-Aware Retrieval
- Status: INTEGRATION TESTED + LIVE API VERIFIED IN VERIFIER ENVIRONMENT; NOT USER VERIFIED
- Branch: `p001/feature-document-ingestion-retrieval`
- Pull request: #1
- Verification: 14 tests at gate + live Uvicorn smoke test PASS.
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Feature 002 — PDF/DOCX/PPTX Ingestion + Provenance
- Status: INTEGRATION TESTED + LIVE API VERIFIED IN VERIFIER ENVIRONMENT; NOT USER VERIFIED
- Branch: `p001/feature-document-formats`
- Pull request: #2
- Verification: 21 tests at gate + live PDF/DOCX/PPTX upload/search PASS.
- Limitations: no OCR, visual understanding, speaker notes/media extraction, exact layout reconstruction.
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

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
- Implemented: server-rendered Jinja UI, workspace/document/search/question/answer flows, provenance display, security headers, restrictive CSP, host/origin controls, escaped untrusted output, provider-status disclosure.
- Verification: 59 tests PASS; dependency audit reported no known vulnerabilities at verification time.
- Public/multi-user deployment security: NOT CLAIMED.

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
- Pull request: #8
- Implemented:
  - workspace-scoped practice sessions;
  - ordered turn persistence and parent-question linkage;
  - configurable maximum turns with hard upper bound of 10;
  - answer/evaluation prerequisite before a follow-up;
  - authoritative evidence reconstruction from stored question provenance;
  - explicit provenance mismatch/cross-workspace rejection;
  - fixed follow-up type allowlist;
  - explicit `complete` termination state;
  - trusted follow-up policy separated from untrusted answer/feedback/evidence;
  - API routes for session creation, history, and follow-up generation;
  - server-rendered session history UI;
  - OpenAI follow-up adapter with strict JSON schema, no tools/actions, `store: false`;
  - provider-neutral/test-only multi-turn integration coverage.
- Verification evidence:
  - GitHub Actions checked-out PR merge ref: PASS;
  - Ubuntu 24.04 / Python 3.12.14 compile check: PASS;
  - full regression + Feature 008 suite: 82 passed, 2 dependency deprecation warnings;
  - session/workspace isolation: PASS;
  - answer-before-follow-up enforcement: PASS;
  - max-turn and completion enforcement: PASS;
  - prompt/instruction separation: PASS at request-structure/provider-payload level;
  - strict provider follow-up JSON schema: PASS with mocked HTTP;
  - dependency audit: no known vulnerabilities found at verification time.
- Explicit limitations:
  - no live authenticated OpenAI follow-up call has been made;
  - no claim of educational effectiveness or human-examiner equivalence;
  - no speech/delivery behavior yet;
  - public/multi-user authentication and authorization remain unimplemented;
  - user-device/browser verification remains NOT RUN.

## Current Product Boundary
The application now supports a bounded provider-neutral text practice workflow with document provenance, retrieval, reviewer questions, evidence-aware qualitative feedback, and multi-turn challenge sessions. Real provider adapters exist but are only live after explicit secure environment configuration and credentialed verification.

## Still Not Implemented / Not Live Verified
- authenticated live external AI verification
- speech input/output and delivery analysis
- authentication/multi-user authorization
- public deployment hardening/rate limiting/session security
- OCR for scanned PDFs
- image/chart/diagram understanding
- user-device/browser verification

## Important Boundary
Passing tests and dependency audits do not establish that the product is hack-proof, production-ready, universally prompt-injection-proof, or suitable for high-stakes grading. Security remains a continuing release gate.