# Project 001 Decisions

## P001-DR-001 — Approve MVP architecture foundation
- Date: 2026-09-08
- Status: APPROVED
- Authority level: A3
- Context: Project 001 completed an initial research-gap review and architecture proposal. Engineering was blocked pending owner approval of the core framework, persistence, frontend, retrieval, and provider abstraction strategy.
- Decision: Approve the MVP foundation as FastAPI + Python backend, SQLite persistence, server-rendered HTML with lightweight JavaScript, provenance-aware document ingestion, inspectable hybrid retrieval, and provider-adapter interfaces for AI and later speech services.
- Rationale: The stack is lightweight, explainable, testable, compatible with modest hardware, aligned with existing Python/FastAPI skills, and avoids premature vector-database or SPA complexity.
- Consequences: Engineering may begin bounded implementation. Dedicated vector databases, heavy SPA migration, microphone/STT, TTS, avatars, VR, body-language analysis, and multi-user conferencing remain post-MVP unless separately approved.
- Approved by: AJ
- Approval evidence: User reply “Okay, move on” immediately after the architecture approval request.

## P001-DR-002 — First bounded engineering feature
- Date: 2026-09-08
- Status: APPROVED FOR EXECUTION
- Authority level: A2
- Decision: Implement document ingestion + provenance-aware lexical retrieval as the first engineering slice before adding LLM question generation.
- Rationale: Grounding quality and evidence traceability are foundational to the project’s differentiated direction and can be tested without relying on an external AI provider.
- Acceptance gate: Independent verification must confirm extraction/provenance/retrieval behavior before the feature is treated as verified.

## P001-DR-003 — Feature 001 verification gate passed in verifier environment
- Date: 2026-09-08
- Status: RECORDED
- Authority level: A1 verification outcome
- Decision: Feature 001 passed independent logic tests, API integration tests, and a live Uvicorn workspace/upload/search smoke test in the verifier environment. It may move to review-ready status.
- Evidence: `project-control/TEST_EVIDENCE.md` and `verification/FEATURE_001_VERIFICATION_REPORT.md`.
- Limitation: direct Git checkout was unavailable in the verifier container because GitHub DNS resolution failed; exact branch files were fetched through the authenticated connector and reconstructed locally. AJ-device/runtime and user verification remain outstanding.
