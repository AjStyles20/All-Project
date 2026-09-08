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
  - no autonomous tools/web actions
  - prompt-injection defenses are foundational, not a claim of universal immunity
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Feature 005 — Secure Evidence-Aware Answer Evaluation Foundation
- Status: CI VERIFIED WITH TEST-ONLY ANSWER EVALUATOR; REAL AI EVALUATOR NOT LIVE VERIFIED
- Branch: `p001/feature-answer-evaluation`
- Pull request: #5
- Implemented:
  - provider-neutral `AnswerEvaluator` interface
  - explicit HTTP 503 unavailable state when no evaluator is configured
  - trusted evaluation policy separated from untrusted question, answer, and source evidence
  - answer length and evaluator-output bounds
  - authoritative question/workspace ownership checks
  - authoritative evidence reconstruction from stored question chunk IDs
  - provenance tampering detection for document ID, filename, and locator
  - fixed five-category qualitative feedback rubric
  - fixed qualitative status allowlist
  - explicit prohibition on an objective overall numeric score in this feature
  - feedback evidence-reference confinement to the authoritative evaluation context
  - bounded provider/model/version metadata
  - persistence of answer, feedback, evidence provenance, policy ID, and provider/model metadata
  - ownership recheck immediately before persistence
  - end-to-end FastAPI test of document -> question -> answer -> feedback loop with test-only providers
- Verification evidence:
  - GitHub Actions checked-out PR merge ref: PASS
  - Ubuntu 24.04 / Python 3.12.14 compile check: PASS
  - full regression + Feature 005 suite: 52 passed
  - prompt/instruction separation: PASS at request-structure level
  - cross-workspace question rejection: PASS
  - provenance-tampering rejection: PASS
  - invalid category/status rejection: PASS
  - invalid/out-of-context evidence-reference rejection: PASS
  - oversized answer/summary/provider metadata rejection: PASS
  - full test-only API practice loop: PASS
  - dependency audit: no known vulnerabilities found at verification time
- Explicit limitations:
  - no real evaluator/LLM provider/model is configured
  - no live AI evaluation-quality claim
  - no objective/high-stakes grading claim
  - no speech/delivery/confidence/emotion evaluation
  - no public/multi-user deployment hardening claim
  - prompt-injection controls are foundational, not universal immunity
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Feature 006 — First Usable Secure Server-Rendered Web UI
- Status: CI VERIFIED — NOT USER-DEVICE/BROWSER VERIFIED
- Branch: `p001/feature-web-ui`
- Pull request: #6
- Implemented:
  - Jinja2 server-rendered home, workspace, and question pages
  - workspace creation, document upload, evidence search, question-generation, answer/evaluation form flows
  - question and evaluation history views
  - visible filename/locator/source provenance
  - truthful configured/not-configured capability states
  - no React dependency and no inline JavaScript in this slice
  - restrictive Content-Security-Policy and security response headers
  - trusted-host middleware
  - explicit rejection of unsafe browser mutations with foreign Origin/cross-site fetch signals
  - API docs disabled by default
  - Jinja autoescaped rendering of uploaded/model text
  - semantic form labels, native keyboard controls, textual status communication, visible focus styling
  - cross-workspace question-view isolation
- Verification evidence:
  - GitHub Actions checked-out PR #6 merge ref: PASS
  - Ubuntu 24.04 / Python 3.12.14 compile check: PASS
  - full regression + Feature 006 suite: 59 passed
  - script-like uploaded text HTML escaping/XSS regression: PASS
  - cross-origin unsafe browser mutation rejection: PASS
  - security-header checks: PASS
  - API docs disabled by default: PASS
  - full server-rendered document -> question -> answer -> feedback loop with test-only providers: PASS
  - cross-workspace question URL isolation: PASS
  - dependency audit: no known vulnerabilities found at verification time
- Explicit limitations:
  - no AJ Windows/browser verification yet
  - no real AI providers configured
  - no authentication/multi-user authorization
  - no full session-bound CSRF token infrastructure
  - no public-production deployment claim
  - no full screen-reader/accessibility audit
- User-device/runtime verification: NOT RUN
- User verification: NOT RUN

## Core Text Practice Loop Status
The provider-neutral backend and first browser UI now support the complete bounded text workflow:
1. create a workspace;
2. upload supported documents with provenance;
3. inspect workspace-scoped evidence retrieval;
4. generate a source-grounded reviewer question through a configured provider interface;
5. review the evidence used for the question;
6. submit a text answer;
7. evaluate the answer against authoritative source evidence through a configured evaluator interface;
8. inspect five-category qualitative feedback and evidence provenance.

The complete workflow is verified in CI with explicit test-only AI providers. Real AI providers are still not configured and must not be represented as live.

## Still Not Implemented / Not Live Verified
- real configured semantic embedding provider/model
- real configured LLM question-generation provider/model
- real configured answer-evaluation provider/model
- multi-turn challenge/follow-up behavior
- speech services
- authentication/multi-user behavior
- full CSRF/session infrastructure for authenticated deployment
- public deployment hardening
- AJ-device/browser verification

## Important Boundary
No external AI or embedding provider is configured. Test-only fake providers exist solely for verification and must never be represented as production AI. Semantic retrieval, question generation, and answer evaluation are live only after real providers/models are configured and separately verified. The current web interface is a secure-by-default local prototype foundation, not a claim of public-production readiness, hack-proofing, universal prompt-injection immunity, or completed accessibility certification.
