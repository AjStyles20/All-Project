# Project 001 State

## Identity
- Working name: AI Virtual Audience / Presentation & Defense Simulator
- Project ID: P001
- Owner: AJ
- Status: ACTIVE
- Stage: Coherent bounded rehearsal workflow implemented and CI verified through Feature 011; live AJ-device/provider verification remains outstanding.
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
- AI/speech services: provider-adapter interfaces; no production provider hard-coded into the core
- Security baseline: active release gate for every substantial feature

## Verified Engineering Progress
- Feature 001: TXT/Markdown ingestion + lexical retrieval — VERIFIED in verifier environment
- Feature 002: PDF/DOCX/PPTX provenance ingestion — VERIFIED in verifier environment
- Feature 003: hybrid retrieval foundation — CI VERIFIED with test-only embedding provider
- Feature 004: grounded question generation — CI VERIFIED with test-only generator
- Feature 005: evidence-aware qualitative answer evaluation — CI VERIFIED with test-only evaluator
- Feature 006: secure server-rendered UI — CI VERIFIED
- Feature 007: optional OpenAI provider adapter — CI VERIFIED with mocked HTTP; real authenticated call NOT VERIFIED
- Feature 008: bounded multi-turn defense sessions — CI VERIFIED; real authenticated follow-up NOT VERIFIED
- Feature 009: secure microphone/speech input — CI VERIFIED; real microphone/provider NOT VERIFIED
- Feature 010: optional reviewer speech output — CI VERIFIED; real TTS/browser playback NOT VERIFIED
- Feature 011: end-to-end rehearsal experience — CI VERIFIED / D4 INTEGRATED; AJ-device rehearsal NOT VERIFIED

## Current Rehearsal Flow
1. Create a workspace and upload supported source documents.
2. Extract and chunk content with provenance.
3. Start a bounded defense session using topic, reviewer role, retrieval mode and max-turn count.
4. Land directly on the first authoritative reviewer turn.
5. Read the written question and source evidence; optionally listen to reviewer speech.
6. Answer by text or optionally record -> stop -> explicitly transcribe -> review/edit transcript.
7. Submit for five-category evidence-aware qualitative feedback.
8. Review feedback and return to the same session.
9. Generate one evidence-grounded follow-up when configured; land directly on that new turn.
10. Stop when the provider returns `complete` or when the final configured turn is answered.
11. Review the completed session summary and any prior turn/feedback.

## Feature 011 State Rules
- session IDs do not authorize question access by themselves;
- session question pages verify workspace + session + question membership server-side;
- current turn, generated-turn count, answered-turn count and max turns are server-derived;
- final-turn answer completion does not require another provider call;
- an exhausted answered session is reconciled to `complete`;
- completion reconciliation is idempotent;
- completed sessions reject further follow-up generation;
- normal non-session question workflows remain available.

## Security Posture
- Security baseline: ACTIVE
- Parameterized SQLite statements: in use
- Workspace scoping/ownership checks: implemented across retrieval/question/evaluation/session/transcription/TTS paths
- Upload/audio bounds and allowlists: implemented within current feature bounds
- Cross-workspace question/evidence/session/session-question checks: tested
- Prompt/instruction separation: tested at request-structure and mocked provider-payload level
- Provider outputs: bounded/validated before persistence or use
- Provider tools/actions: disabled for current OpenAI adapters
- API secrets: environment-only; not stored in source/UI/database
- Same-origin/TrustedHost/CSP controls: active regression gates
- Authentication: NOT IMPLEMENTED
- Multi-user authorization: NOT IMPLEMENTED
- Public deployment hardening/rate limiting/secure authenticated session management: NOT IMPLEMENTED
- Security claim: do not describe the product as production-ready, tamper-proof, hack-proof, or universally prompt-injection-proof

## Current Verification Gate
Feature 011 checked-out GitHub CI:
- run ID: `34244019212`
- checked-out merge ref: `bb68a0e853a23157fbf7bb9f8034aca0b1e7e022`
- Ubuntu 24.04.5 / Python 3.12.14
- compile check: PASS
- `115 passed, 2 warnings in 8.26s`
- dependency audit: `No known vulnerabilities found`
- AJ Windows/browser/microphone/audio rehearsal: NOT RUN
- live authenticated external provider requests: NOT RUN

## Research / Claim Boundary
- Generic `AI presentation coach with questions` novelty: CONTRADICTED
- Stronger differentiated direction: source-grounded, evidence-traceable technical/research review with explicit reviewer roles, transparent uncertainty, bounded multi-turn challenge behavior, optional speech interaction and coherent rehearsal state: UNDER REVIEW / PROVISIONALLY ACCEPTED
- Educational effectiveness claim: UNSUPPORTED
- Human-examiner equivalence claim: UNSUPPORTED
- Confidence/anxiety improvement claim: UNSUPPORTED
- Objective presentation-quality scoring claim: UNSUPPORTED
- Voice emotion/confidence/accent scoring claim: NOT IMPLEMENTED / NOT CLAIMED

## Current Pull Request Stack
- PR #1 — Feature 001
- PR #2 — Feature 002, stacked on #1
- PR #3 — Feature 003, stacked on #2
- PR #4 — Feature 004, stacked on #3
- PR #5 — Feature 005, stacked on #4
- PR #6 — Feature 006, stacked on #5
- PR #7 — Feature 007, stacked on #6
- PR #8 — Feature 008, stacked on #7
- PR #9 — Feature 009, stacked on #8, READY FOR REVIEW
- PR #10 — Feature 010, stacked on #9, READY FOR REVIEW
- PR #11 — Feature 011, stacked on #10, CI VERIFIED; ready-state pending final documentation gate

## Current Limitations
- no real authenticated external AI/transcription/TTS verification yet
- no AJ-device/browser/microphone/audio rehearsal verification
- no delivery analysis
- no authentication/multi-user authorization
- no public deployment hardening/rate limiting
- no OCR for scanned PDFs
- no image/chart/diagram understanding

## Next Engineering Gate
After Feature 011 documentation/PR synchronization, prioritize AJ-controlled local rehearsal verification and a release-readiness pass before adding new modalities. Authentication/authorization should become the next major security feature only when moving beyond the local/single-user prototype toward shared or public deployment.
