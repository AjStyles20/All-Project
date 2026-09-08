# Project 001 State

## Identity
- Working name: AI Virtual Audience / Presentation & Defense Simulator
- Project ID: P001
- Owner: AJ
- Status: ACTIVE
- Stage: Secure bounded multi-turn practice workflow plus optional review-before-submit speech input implemented and CI verified; real provider/device verification remains outstanding.
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
- Feature 007: optional OpenAI provider adapter — CI VERIFIED with mocked HTTP; PR #7 READY FOR REVIEW; real authenticated call NOT VERIFIED
- Feature 008: bounded multi-turn defense sessions — CI VERIFIED; PR #8 READY FOR REVIEW; real authenticated follow-up NOT VERIFIED
- Feature 009: secure microphone/speech input — CI VERIFIED with fake/mocked transcription providers; real microphone/provider NOT VERIFIED

## Current Practice Flow
1. Create workspace.
2. Upload supported source documents.
3. Extract/chunk with provenance.
4. Retrieve workspace-scoped evidence.
5. Generate a grounded reviewer question.
6. Answer by text, or optionally record audio and explicitly request transcription.
7. Speech transcript is returned to the answer textarea for review/editing; it is never auto-submitted.
8. Submit answer for five-category evidence-aware qualitative feedback.
9. In a bounded defense session, generate evidence-grounded follow-up challenges only after the current question has been answered/evaluated.
10. Stop when the reviewer returns `complete` or the configured turn bound is reached.

## Feature 009 Privacy / Security Behavior
- microphone capture never starts automatically;
- browser microphone invocation occurs only from the explicit Start button handler;
- camera and geolocation remain denied;
- recording stops at 120 seconds maximum;
- Cancel discards captured data;
- Stop recording does not transmit audio;
- Transcribe recording is a separate explicit network-consent action;
- UI discloses the configured transcription provider/model before the user records/sends audio;
- server validates workspace/question ownership, audio size and media type;
- raw audio is not persisted by the application;
- transcript is bounded to the existing 8000-character answer limit;
- transcription does not create an answer/evaluation automatically;
- text answer remains available when speech is unsupported, denied, or unconfigured;
- provider credential stays server-side/environment-only;
- provider raw error bodies are not exposed to users.

## Security Posture
- Security baseline: ACTIVE
- Parameterized SQLite statements: in use
- Workspace scoping/ownership checks: implemented across retrieval/question/evaluation/session/transcription paths
- Upload/audio bounds and allowlists: implemented within current feature bounds
- Cross-workspace question/evidence/session checks: tested
- Prompt/instruction separation: tested at request-structure and mocked provider-payload level
- Provider outputs: bounded/validated before persistence or use
- Provider tools/actions: disabled for current OpenAI adapters
- API secrets: environment-only; not stored in source/UI/database
- Dependency audit in CI: active
- Authentication: NOT IMPLEMENTED
- Multi-user authorization: NOT IMPLEMENTED
- Public deployment hardening/rate limiting/session security: NOT IMPLEMENTED
- Security claim: do not describe the product as production-ready, tamper-proof, hack-proof, or universally prompt-injection-proof

## Current Verification Gate
Feature 009 checked-out GitHub CI:
- final run ID: `34207981904`
- checked-out merge ref: `6b66dfaf3d55ac4806389928dd433a92766229fb`
- Ubuntu 24.04 / Python 3.12.14
- compile check: PASS
- 95 tests PASS
- dependency audit: no known vulnerabilities found at verification time
- real external transcription request: NOT RUN
- AJ Windows/browser/microphone verification: NOT RUN

## Research / Claim Boundary
- Generic `AI presentation coach with questions` novelty: CONTRADICTED
- Stronger differentiated direction: source-grounded, evidence-traceable technical/research review with explicit reviewer roles, transparent uncertainty, bounded multi-turn challenge behavior, and optional voice interaction: UNDER REVIEW / PROVISIONALLY ACCEPTED
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
- PR #7 — Feature 007, stacked on #6, READY FOR REVIEW
- PR #8 — Feature 008, stacked on #7, READY FOR REVIEW
- PR #9 — Feature 009, stacked on #8, CI VERIFIED; ready-state pending final documentation/PR transition

## Current Limitations
- no real authenticated external AI/transcription verification yet
- no AJ-device/browser/microphone verification
- no speech output/TTS yet
- no delivery analysis
- no authentication/multi-user authorization
- no public deployment hardening/rate limiting
- no OCR for scanned PDFs
- no image/chart/diagram understanding

## Next Engineering Gate
Close Feature 009 review state, then implement speech output/TTS as a separate bounded feature if it preserves accessibility and does not make audio mandatory. Live provider/device verification remains a separate AJ-controlled gate and must never require committing or pasting secrets into source/browser forms.