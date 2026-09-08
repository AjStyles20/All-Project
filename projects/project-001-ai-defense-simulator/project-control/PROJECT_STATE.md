# Project 001 State

## Identity
- Working name: AI Virtual Audience / Presentation & Defense Simulator
- Project ID: P001
- Owner: AJ
- Status: ACTIVE
- Stage: Secure bounded multi-turn text practice workflow implemented and CI verified with test-only providers; real provider and AJ-device live verification remain outstanding.
- Last verified date: 2026-09-08

## Approved Direction
Create a defensible web application that helps users practice presentations, defenses, vivas, interviews, and professional reviews using their own materials as context for source-grounded AI questions and evidence-aware feedback.

## Approved Technical Foundation
- Primary language: Python
- Backend: FastAPI
- Persistence: SQLite for MVP/local single-user phase
- Delivery platform: full web application
- Frontend: server-rendered HTML/CSS + lightweight JavaScript initially
- React: optional later only when UI/client-state complexity justifies it
- Document ingestion: provenance-aware TXT/Markdown/PDF/DOCX/PPTX
- Retrieval: inspectable lexical FTS5 plus optional provider-neutral semantic layer
- AI services: provider-adapter interfaces; no production provider hard-coded into the core
- Security baseline: active release gate for every substantial feature

## Verified Engineering Progress
- Feature 001: TXT/Markdown ingestion + lexical retrieval — VERIFIED in verifier environment
- Feature 002: PDF/DOCX/PPTX provenance ingestion — VERIFIED in verifier environment
- Feature 003: hybrid retrieval foundation — CI VERIFIED with test-only embedding provider
- Feature 004: grounded question generation — CI VERIFIED with test-only generator
- Feature 005: evidence-aware qualitative answer evaluation — CI VERIFIED with test-only evaluator
- Feature 006: secure server-rendered UI — CI VERIFIED
- Feature 007: optional OpenAI provider adapter — CI VERIFIED with mocked HTTP; PR #7 READY FOR REVIEW; real authenticated call NOT VERIFIED
- Feature 008: bounded multi-turn defense sessions — CI VERIFIED with test-only follow-up provider; real authenticated follow-up NOT VERIFIED

## Feature 008 Current Behavior
A practice session now:
1. belongs to exactly one workspace;
2. has one approved reviewer role and topic;
3. starts from a normal source-grounded reviewer question;
4. records ordered turns and parent-question linkage;
5. requires the current question to have an answer/evaluation before another challenge can be generated;
6. reconstructs follow-up evidence from authoritative stored question provenance rather than client-submitted evidence;
7. restricts follow-up decisions to a fixed allowlist (`probe_missing`, `challenge_unsupported`, `clarify_reasoning`, `request_evidence`, `deepen_topic`, `complete`);
8. enforces a configurable maximum with a hard bound of 10 turns;
9. terminates explicitly when the provider returns `complete` or when limits prevent another turn;
10. exposes session history through API and a server-rendered session page.

## Security Posture
- Security baseline: ACTIVE
- Parameterized SQLite statements: in use
- Workspace scoping/ownership checks: implemented across retrieval/question/evaluation/session paths
- Upload size/extension/parser controls: implemented within current feature bounds
- Cross-workspace question/evidence/session checks: tested
- Prompt/instruction separation: tested at request-structure and mocked provider-payload level
- Provider outputs: bounded and validated before persistence
- Provider tools/actions: disabled for current OpenAI adapters
- API secrets: environment-only; not stored in source/UI/database
- Dependency audit in CI: active
- Authentication: NOT IMPLEMENTED
- Multi-user authorization: NOT IMPLEMENTED
- Public deployment hardening/rate limiting/session security: NOT IMPLEMENTED
- Security claim: do not describe the product as production-ready, tamper-proof, hack-proof, or universally prompt-injection-proof

## Current Verification Gate
Feature 008 checked-out GitHub CI:
- Ubuntu 24.04 / Python 3.12.14
- compile check: PASS
- 82 tests PASS
- dependency audit: no known vulnerabilities found at verification time
- real external provider request: NOT RUN
- AJ Windows/browser verification: NOT RUN

## Research / Claim Boundary
- Historical research window: approximately 1990-present
- Generic `AI presentation coach with questions` novelty: CONTRADICTED
- Stronger differentiated direction: source-grounded, evidence-traceable technical/research review with explicit reviewer roles, transparent uncertainty, and bounded multi-turn challenge behavior: UNDER REVIEW / PROVISIONALLY ACCEPTED
- Educational effectiveness claim: UNSUPPORTED
- Human-examiner equivalence claim: UNSUPPORTED
- Confidence/anxiety improvement claim: UNSUPPORTED
- Objective presentation-quality scoring claim: UNSUPPORTED

## Current Pull Request Stack
- PR #1 — Feature 001
- PR #2 — Feature 002, stacked on #1
- PR #3 — Feature 003, stacked on #2
- PR #4 — Feature 004, stacked on #3
- PR #5 — Feature 005, stacked on #4
- PR #6 — Feature 006, stacked on #5
- PR #7 — Feature 007, stacked on #6, READY FOR REVIEW
- PR #8 — Feature 008, stacked on #7, CI VERIFIED but remains draft pending final review/state synchronization

## Current Limitations
- no real authenticated OpenAI provider verification yet
- no speech input/output or delivery analysis
- no authentication/multi-user authorization
- no public deployment hardening/rate limiting
- no OCR for scanned PDFs
- no image/chart/diagram understanding
- no AJ-device/browser verification

## Next Engineering Gate
Complete Feature 008 review/state synchronization, then choose between (a) AJ-controlled live provider verification and local browser verification, or (b) a bounded speech-input/output slice. Live provider verification must never require putting an API key into source control or browser forms.