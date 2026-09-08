# Project 001 State

## Identity
- Working name: AI Virtual Audience / Presentation & Defense Simulator
- Project ID: P001
- Owner: AJ
- Status: ACTIVE
- Stage: Core provider-neutral text practice loop implemented and CI verified with test-only AI providers; first usable web UI is the next engineering slice.
- Last verified date: 2026-09-08

## Approved Direction
Create a defensible web application that helps users practice presentations, defenses, vivas, interviews, and professional reviews using their own materials as context for source-grounded AI questions and evidence-aware feedback.

## Approved Initial Scope
- Upload or ingest project documents/slides.
- Ground question generation in supplied materials where appropriate.
- Support configurable reviewer/audience/panel personas.
- Conduct practice sessions through text and, where technically feasible later, microphone input.
- Store or summarize session history.
- Produce explainable feedback based on explicit criteria.
- Track provenance for claims, tests, generated questions, retrieved evidence, and evaluation outputs.

## Approved Technical Foundation
- Primary language: Python
- Backend: FastAPI
- Persistence: SQLite for the MVP/local single-user phase
- Delivery platform: full web application
- Frontend: server-rendered HTML/CSS + lightweight JavaScript initially
- React: optional later only if UI/client-state complexity materially justifies it
- Document ingestion: provenance-aware TXT/Markdown/PDF/DOCX/PPTX
- Retrieval: inspectable lexical FTS5 plus optional provider-neutral semantic layer
- AI services: provider-adapter interfaces; no production provider hard-coded
- Security baseline: active release gate for every substantial feature

## Not Yet Approved / Not Yet Verified as MVP Claims
- Computer-vision body-language scoring
- Emotion recognition
- Voice cloning
- Animated 3D classroom/audience
- Multi-user real-time conferencing
- Automated high-stakes grading
- Objective confidence or presentation-quality scoring without validated evidence
- Public/multi-user deployment security until authentication/authorization/deployment hardening are implemented and verified

## Current Engineering Status

### Feature 001 — Document Ingestion + Lexical Retrieval
- TXT/Markdown ingestion: VERIFIED in verifier environment
- deterministic chunking + SHA-256 provenance: VERIFIED
- SQLite FTS5 retrieval: VERIFIED
- workspace isolation: VERIFIED
- API integration: PASS
- live Uvicorn smoke test: PASS in verifier environment
- user-device verification: NOT RUN

### Feature 002 — Rich Document Formats
- PDF text extraction with page locators: VERIFIED in verifier environment
- DOCX paragraph locators: VERIFIED
- PPTX slide locators: VERIFIED
- malformed/encrypted input handling: VERIFIED within bounded cases
- OCR/visual understanding/exact layout reconstruction: NOT IMPLEMENTED

### Feature 003 — Hybrid Retrieval Foundation
- provider-neutral embedding interface: IMPLEMENTED
- workspace-scoped embedding persistence: IMPLEMENTED
- stale detection/vector validation: IMPLEMENTED
- explainable lexical/semantic merge: IMPLEMENTED
- no-provider lexical fallback: VERIFIED
- test-only semantic provider: CI VERIFIED
- real semantic provider/model: NOT CONFIGURED / NOT LIVE VERIFIED
- CI gate at feature verification: 32 tests PASS; dependency audit reported no known vulnerabilities at that time

### Feature 004 — Source-Grounded Question Generation Foundation
- provider-neutral question generator: IMPLEMENTED
- trusted-policy/untrusted-evidence separation: IMPLEMENTED
- reviewer-role allowlist: IMPLEMENTED
- question/evidence provenance persistence: IMPLEMENTED
- authoritative workspace evidence ownership validation: IMPLEMENTED
- test-only question generator: CI VERIFIED
- real LLM provider/model: NOT CONFIGURED / NOT LIVE VERIFIED
- CI gate at feature verification: 39 tests PASS; dependency audit reported no known vulnerabilities at that time

### Feature 005 — Evidence-Aware Answer Evaluation Foundation
- provider-neutral answer evaluator: IMPLEMENTED
- trusted-policy separation from untrusted question/answer/evidence: IMPLEMENTED
- authoritative question/workspace ownership validation: IMPLEMENTED
- authoritative evidence reconstruction: IMPLEMENTED
- provenance tampering detection: IMPLEMENTED
- fixed five-category qualitative rubric: IMPLEMENTED
- objective overall numeric grading: INTENTIONALLY NOT CLAIMED
- feedback evidence-reference confinement: IMPLEMENTED
- answer/evaluation persistence: IMPLEMENTED
- complete test-only HTTP practice loop: VERIFIED
- CI gate: 52 tests PASS on checked-out PR merge ref
- dependency audit: no known vulnerabilities found at verification time
- real evaluator/LLM provider/model: NOT CONFIGURED / NOT LIVE VERIFIED
- user-device verification: NOT RUN

## Core Text Practice Loop
The backend now has a complete bounded provider-neutral flow:
1. user creates a workspace;
2. uploads supported source material;
3. system extracts/chunks it with provenance;
4. retrieval selects workspace-scoped evidence;
5. configured question provider receives trusted policy + untrusted evidence and returns one grounded review question;
6. question and evidence provenance are persisted;
7. user submits a text answer;
8. configured evaluator receives trusted policy + authoritative question/evidence + untrusted answer;
9. evaluator returns five-category qualitative feedback;
10. output is validated, provenance-checked, persisted, and returned without an objective overall score.

This flow is verified with test-only providers only. It is not yet a live AI product because no real embedding/question/evaluation provider is configured.

## Security Posture
- Security baseline: ACTIVE
- Parameterized SQLite statements: in use
- Workspace scoping/ownership checks: implemented across current retrieval/question/evaluation paths
- Upload size/extension/parser controls: implemented within current feature bounds
- Cross-workspace question/evidence checks: tested
- Prompt/instruction separation: tested at request-structure level
- Provider outputs: bounded and validated before persistence
- Dependency audit in CI: active
- Authentication: NOT IMPLEMENTED
- Multi-user authorization: NOT IMPLEMENTED
- Public rate limiting/CSRF/production headers/HTTPS config: NOT IMPLEMENTED
- Security claim: do not describe the product as production-ready, tamper-proof, or universally prompt-injection-proof

## Research Status
- Historical window: approximately 1990-present, with earlier foundational work where relevant
- Literature review: IN PROGRESS
- Comparable-system first pass: COMPLETE
- Generic `AI presentation coach with questions` novelty: CONTRADICTED
- Stronger differentiated direction: source-grounded, evidence-traceable technical/research review with explicit reviewer roles, transparent uncertainty, and multi-turn challenge behavior: UNDER REVIEW / PROVISIONALLY ACCEPTED
- Confidence/anxiety improvement claim: UNSUPPORTED
- Objective presentation-quality scoring claim: UNSUPPORTED

## Current Pull Request Stack
- PR #1 — Feature 001 document ingestion/retrieval
- PR #2 — Feature 002 PDF/DOCX/PPTX ingestion, stacked on Feature 001
- PR #3 — Feature 003 hybrid retrieval, stacked on Feature 002
- PR #4 — Feature 004 grounded questioning, stacked on Feature 003
- PR #5 — Feature 005 answer evaluation, stacked on Feature 004

All remain review/merge controlled; verification status must not be inferred merely from PR existence.

## Current Limitations
- no real embedding model/provider configured
- no real question-generation LLM configured
- no real answer-evaluation LLM configured
- no first usable browser UI yet
- no session/history UI
- no multi-turn challenge/follow-up behavior yet
- no speech input/output
- no authentication/multi-user authorization
- no public deployment hardening
- no OCR for scanned PDFs
- no image/chart/diagram understanding

## Next Engineering Gate
Build the first usable server-rendered web interface around the verified core text workflow, with accessibility, safe output rendering, CSRF/deployment considerations documented, and no fake AI state. The UI must clearly distinguish configured/unconfigured AI capabilities and preserve evidence provenance in visible feedback.
