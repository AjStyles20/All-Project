# Requirements

## R-001 — Shared Source of Truth
The system must maintain canonical project state in version-controlled project-control files accessible to participating agents.

Acceptance criteria:
- Current scope, stack, implementation status, tests, claims, limitations, and pending decisions are recorded.
- Agents read relevant control files before substantial work.
- Conversation history is not treated as the only source of truth.

## R-002 — Authority Control
The system must distinguish A0, A1, A2, and A3 actions and prevent A3 changes without AJ approval.

## R-003 — Research Integrity
Research outputs must preserve provenance and must not fabricate papers, citations, datasets, findings, or novelty claims.

## R-004 — Implementation Integrity
Agents must not invent functionality, integrations, metrics, live data, alerts, or successful actions.

## R-005 — Verification Independence
Substantial engineering work must pass independent verification before it is treated as verified.

## R-006 — Documentation Synchronization
Academic and technical documentation must reflect actual verified implementation and explicitly distinguish implemented, simulated, proposed, parked, and future features.

## R-007 — Explainability
Engineering decisions and implementation must be documented sufficiently for AJ to understand and defend them.

## R-008 — Handoffs
Every workstream must leave a structured handoff enabling another agent to continue without depending on hidden conversation context.

## R-009 — Failure Traceability
Meaningful bugs, environment issues, rejected approaches, corrections, and regression evidence must be logged.

## R-010 — Scope Control
New ideas must be classified as MVP, defense-useful, post-MVP, or future research before implementation.

## R-011 — Claim/Evidence Mapping
Important academic and product claims must have explicit evidence status and source/test provenance.

## R-012 — Defense Readiness
The workflow must include a tutor/defense layer that explains actual implementation and generates likely defense questions based on verified project state.

## R-013 — Connected Workspace
GitHub must serve as canonical technical storage. Google Drive may serve as the research, dissertation, supervisor, presentation, and supporting-document workspace.

## R-014 — Safe Agent Boundaries
Research agents must not silently change implementation. Engineering agents must not silently change research objectives. Documentation agents must not invent implementation details. Verification agents must report failures independently of the implementer.
