# Decisions

Use this file for durable architectural, methodological, governance, and scope decisions.

## Decision Record Template

### DR-XXX — Decision title
- Date:
- Status: Proposed / Approved / Rejected / Superseded
- Authority level: A1 / A2 / A3
- Context:
- Options considered:
- Decision:
- Rationale:
- Consequences:
- Files/components affected:
- Claims affected:
- Approved by:
- Supersedes:

---

## DR-001 — Use GitHub as canonical technical source
- Date: 2026-09-08
- Status: Approved
- Authority level: A2
- Context: Multiple AI tools need a shared project state that is independent of conversation history.
- Decision: Use GitHub for application code, tests, technical documentation, and canonical project-control Markdown files.
- Rationale: Version control, traceability, shared access, commit history, and compatibility with Codex/ChatGPT workflows.
- Consequences: Agents must synchronize technical state through this repository rather than relying only on chat memory.
- Approved by: AJ through continuation of the setup workflow.

## DR-002 — Use Google Drive for academic/supporting workspace
- Date: 2026-09-08
- Status: Approved
- Authority level: A2
- Context: Dissertation, papers, supervisor documents, diagrams, presentations, and supporting assets are better managed in a document workspace.
- Decision: Use connected Google Drive for research and academic/supporting artifacts while keeping technical state in GitHub.
- Consequences: Critical state should still be reflected in project-control files when it affects implementation or claims.
- Approved by: AJ through continuation of the setup workflow.

## DR-003 — Independent verification gate
- Date: 2026-09-08
- Status: Approved
- Authority level: A2
- Context: Implementing agents can introduce regressions and should not be sole judges of completion.
- Decision: Substantial implementation work must be independently challenged before being accepted as verified.
- Consequences: `IMPLEMENTED` is not equivalent to `VERIFIED`.
- Approved by: AJ through prior workflow design.

## DR-004 — Instantiate Project 001 as AI Virtual Audience / Presentation & Defense Simulator
- Date: 2026-09-08
- Status: Approved
- Authority level: A3
- Context: AJ Project OS needs a real pilot project to validate the multi-agent workflow from research through engineering, verification, documentation, and defense preparation.
- Options considered: Multiple earlier project ideas including virtual classroom, coding examination platform, and AI presentation/defense simulator.
- Decision: Use the AI Virtual Audience / Presentation & Defense Simulator as Project 001.
- Rationale: It exercises research, literature review, RAG/document grounding, personas, speech interfaces, frontend/backend engineering, evaluation, testing, documentation, and defense preparation without requiring specialized hardware.
- Consequences: Project-specific work is now authorized under `projects/project-001-ai-defense-simulator/`. Advanced features remain subject to scope gates.
- Files/components affected: Project 001 workspace, Drive Project 001 workspace, project-control state.
- Claims affected: Novelty and outcome claims remain unverified pending research.
- Approved by: AJ explicitly on 2026-09-08.
