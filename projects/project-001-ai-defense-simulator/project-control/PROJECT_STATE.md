# Project 001 State

## Identity
- Working name: AI Virtual Audience / Presentation & Defense Simulator
- Project ID: P001
- Owner: AJ
- Status: ACTIVE
- Stage: Research gap provisionally accepted; architecture awaiting approval
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

## Current Technical Decisions
No core implementation stack has yet been approved.

Architecture proposal awaiting AJ approval:
- FastAPI backend
- SQLite persistence
- server-rendered HTML + lightweight JavaScript frontend
- provenance-aware document ingestion
- inspectable hybrid retrieval using lexical search plus optional embeddings
- provider-adapter interfaces for LLM/embedding/speech services

## Current Workstreams
- Research: IN PROGRESS — historical window expanded to approximately 1990-present; first screened historical/current evidence set recorded.
- Literature review: IN PROGRESS — speech-aware tutoring, conversational ITS, automatic question generation, presentation feedback, RAG assessment, and LLM-mediated oral/performance assessment identified as established prior art.
- Comparable systems: FIRST PASS COMPLETE — Microsoft Speaker Coach, Yoodli, and VirtualSpeech reviewed.
- Research-gap challenge: PROVISIONALLY ACCEPTED — generic presentation-coach novelty rejected; source-grounded evidence-aware review selected as stronger direction.
- Architecture: PROPOSED — awaiting AJ approval of core stack/foundation.
- Engineering/Codex: BLOCKED pending architecture approval.
- Verification: NOT STARTED.
- Documentation: RESEARCH DOCUMENTATION ACTIVE; product documentation waits for implementation evidence.
- Presentation/evaluation preparation: NOT STARTED.

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
- Project 001 literature matrix in Google Drive, now populated with first screened sources.
- Project 001 research & scope brief in Google Drive.

## Current Research Observation
The historical record shows that speech-aware tutoring, conversational questioning, source-text question generation, automated presentation feedback, and RAG-based assessment each have established precedents. Recent work also reaches directly into LLM-mediated oral and performance assessment. Project 001 therefore should not claim novelty from combining generic AI, questioning, speech, and presentation coaching. The strongest current direction remains source-grounded technical/research review with explicit evidence provenance, reviewer-role differentiation, multi-turn challenge behavior, and transparent uncertainty.

## Blockers
- Core framework/database/retrieval foundation requires AJ approval before Engineering/Codex implementation.
- Novelty remains provisional and requires broader literature/product screening before any strong claim is made.

## Next Gate
AJ reviews the architecture proposal. If approved, Architect converts it into implementation contracts and Engineering/Codex begins the first bounded feature cycle: document ingestion + provenance-aware retrieval, followed by independent verification. Research continues in parallel across older oral-exam/speaking-assessment literature and modern document-grounded systems.
