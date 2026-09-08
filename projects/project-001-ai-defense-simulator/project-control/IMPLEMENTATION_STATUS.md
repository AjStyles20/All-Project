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
- Implemented: provider-neutral embeddings, vector validation, workspace-scoped embedding persistence, stale detection, cosine similarity, explainable hybrid merge, lexical fallback, security bounds, CI + dependency audit.
- Verification: 32 tests PASS; `pip-audit` reported no known vulnerabilities at verification time.
- Limitations: no real embedding provider/model configured; weights are not claimed optimal; public/multi-user hardening incomplete.
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Feature 004 — Secure Source-Grounded Question Generation Foundation
- Status: CI VERIFIED WITH TEST-ONLY QUESTION GENERATOR; REAL LLM PROVIDER NOT LIVE VERIFIED
- Branch: `p001/feature-grounded-questioning`
- Pull request: #4
- Implemented:
  - provider-neutral `QuestionGenerator` interface
  - explicit unavailable state when no provider is configured
  - trusted generation policy separated from untrusted retrieved evidence
  - reviewer-role allowlist
  - bounded topic/evidence/question sizes
  - source-grounded generation request structure
  - question provenance persistence
  - authoritative revalidation that every evidence chunk/document/filename/locator belongs to the target workspace before persistence
  - controlled provider failures
  - prompt-injection fixture and cross-workspace evidence tests
- Verification evidence:
  - GitHub Actions checked-out PR merge ref: PASS
  - Python 3.12 compile check: PASS
  - full regression + Feature 004 suite: 39 passed
  - prompt-injection wrapper separation: PASS
  - reviewer-role allowlist: PASS
  - cross-workspace evidence ownership rejection: PASS
  - oversized provider output rejection before persistence: PASS
  - dependency audit: no known vulnerabilities found at verification time
- Security correction discovered during development:
  - initial question persistence only verified that the target workspace existed;
  - security test identified missing independent ownership verification for evidence chunks;
  - persistence now revalidates each evidence item against authoritative workspace chunks before storage.
- Explicit limitations:
  - no real LLM provider/model is configured
  - no live AI question generation claim
  - no multi-turn follow-up logic yet
  - no answer evaluation/grading yet
  - no autonomous tools/web actions
  - prompt-injection defenses are foundational, not a claim of universal immunity
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Still Not Implemented
- real configured semantic embedding provider/model
- real configured LLM question-generation provider/model
- multi-turn challenge/follow-up behavior
- answer evaluation / evidence-aware feedback
- speech services
- server-rendered UI screens
- authentication/multi-user behavior

## Important Boundary
No external AI or embedding provider is configured. Test-only fake providers exist solely for verification and must never be represented as production AI. Semantic retrieval and question generation are live only after a real provider/model is configured and verified. Public-deployment security, authentication, answer evaluation, speech, OCR, and complex visual understanding remain unverified or unimplemented.
