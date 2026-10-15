# Project 001 State

## Identity
- Working name: AI Virtual Audience / Presentation & Defense Simulator
- Project ID: P001
- Owner: AJ
- Status: ACTIVE
- Stage: Feature 001 verified in verifier environment; awaiting user-runtime verification / review
- Last verified date: 2026-09-08

## Approved Direction
Create a defensible prototype that helps users practice presentations, defenses, vivas, interviews, and professional reviews using their own materials as context for source-grounded AI questions and feedback.

## Approved Initial Scope
- Upload or ingest project documents/slides.
- Ground question generation in supplied materials where appropriate.
- Support configurable reviewer/audience/panel personas.
- Conduct practice sessions through text and, where technically feasible, microphone input.
- Store or summarize session history.
- Produce explainable feedback based on explicit criteria.
- Track provenance for claims, tests, generated questions, retrieved evidence, and evaluation outputs.

## Not Yet Approved as MVP
- Computer-vision body-language scoring.
- Emotion recognition.
- Voice cloning.
- Animated 3D classroom/audience.
- Multi-user real-time conferencing.
- Automated high-stakes grading.
- Any claim that the system objectively measures confidence or presentation quality without validated evidence.

## Approved Technical Foundation
- FastAPI backend
- SQLite persistence
- server-rendered HTML + lightweight JavaScript frontend
- provenance-aware document ingestion
- inspectable hybrid retrieval beginning with lexical FTS5 and optional embeddings later
- provider-adapter interfaces for LLM/embedding/speech services

## Current Workstreams
- Research: IN PROGRESS — historical window approximately 1990-present; screened evidence set recorded and expanding.
- Literature review: IN PROGRESS — speech-aware tutoring, conversational ITS, automatic question generation, presentation feedback, RAG assessment, and LLM-mediated oral/performance assessment identified as established prior art.
- Comparable systems: FIRST PASS COMPLETE — Microsoft Speaker Coach, Yoodli, and VirtualSpeech reviewed.
- Research-gap challenge: PROVISIONALLY ACCEPTED — generic presentation-coach novelty rejected; source-grounded evidence-aware review selected as stronger direction.
- Architecture: APPROVED for MVP foundation.
- Engineering/Codex: FEATURE 001 IMPLEMENTED on branch `p001/feature-document-ingestion-retrieval`.
- Verification: FEATURE 001 PASS in verifier environment; user-device/runtime verification still pending.
- Documentation: RESEARCH + TECHNICAL DOCUMENTATION ACTIVE.
- Presentation/evaluation preparation: NOT STARTED.

## Feature 001 Status
Document ingestion + provenance-aware lexical retrieval:
- implementation: COMPLETE within bounded contract
- TXT/Markdown ingestion: IMPLEMENTED
- deterministic chunking + SHA-256 provenance: IMPLEMENTED
- SQLite FTS5 retrieval: IMPLEMENTED
- workspace isolation: IMPLEMENTED
- API integration suite: PASS
- full verifier-environment suite: 14 passed
- live Uvicorn workspace/upload/search smoke test: PASS
- independent verification: PASS IN VERIFIER ENVIRONMENT
- user-device/runtime verification: NOT RUN
- user verification: NOT RUN
- pull request: #1, ready for review after verification update

## Current Claims
- Speech-enabled automated tutoring existed by the late 1990s: SUPPORTED as historical background.
- Mixed-initiative conversational intelligent tutoring is established prior art: SUPPORTED.
- Automatic question generation from supplied text is established prior art: SUPPORTED.
- Simulation-based public-speaking practice and automated presentation feedback are established prior art: SUPPORTED as background.
- Retrieval-augmented generation is an established grounding/assessment approach: SUPPORTED as background; Project 001 implementation effectiveness not verified.
- LLM-mediated oral/performance assessment is established prior art by 2026: SUPPORTED at abstract-level evidence; detailed comparison still required.
- `AI presentation coaching with follow-up questions` as novelty: CONTRADICTED by reviewed literature/comparable systems.
- Project 001 source-grounded, evidence-traceable review workflow as a differentiated contribution: UNDER REVIEW.
- Confidence/anxiety improvement by Project 001: UNSUPPORTED.
- Objective presentation-quality scoring by Project 001: UNSUPPORTED.

## Evidence Created
- `research/COMPARABLE_SYSTEMS.md`
- `research/LITERATURE_SCREENING.md`
- `research/HISTORICAL_LITERATURE_TIMELINE.md`
- `research/RESEARCH_GAP_REVIEW.md`
- `docs/technical/ARCHITECTURE_PROPOSAL.md`
- `docs/technical/FEATURE_001_INGESTION_RETRIEVAL_CONTRACT.md`
- `verification/FEATURE_001_VERIFICATION_REPORT.md`
- `project-control/TEST_EVIDENCE.md`
- Project 001 literature matrix in Google Drive, populated with screened sources.
- Project 001 research & scope brief in Google Drive.

## Current Research Observation
The historical record shows that speech-aware tutoring, conversational questioning, source-text question generation, automated presentation feedback, and RAG-based assessment each have established precedents. Recent work also reaches directly into LLM-mediated oral and performance assessment. Project 001 therefore should not claim novelty from combining generic AI, questioning, speech, and presentation coaching. The strongest current direction remains source-grounded technical/research review with explicit evidence provenance, reviewer-role differentiation, multi-turn challenge behavior, and transparent uncertainty.

## Current Engineering Boundary
Feature 001 does not implement PDF/DOCX/PPTX extraction, semantic retrieval, LLM question generation, answer evaluation, speech, or UI screens. No documentation or interface may imply otherwise.

## Known Verification Limitation
The verifier execution environment could not resolve GitHub for direct cloning, so exact branch files were retrieved through the authenticated GitHub connector and reconstructed locally before running the test suite and live API smoke test. This is not equivalent to AJ's own-device verification.

## Next Gate
Review Feature 001 PR and perform user-runtime verification when practical. In parallel, continue research. After Feature 001 is accepted, the next bounded engineering slice should add richer document-format ingestion (PDF/DOCX/PPTX) or the first question-generation contract, subject to Project Lead sequencing and evidence review.
