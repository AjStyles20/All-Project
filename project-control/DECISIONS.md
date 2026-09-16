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

## DR-004 — Instantiate historical Project 001 as AI Virtual Audience / Presentation & Defense Simulator
- Date: 2026-09-08
- Status: Approved
- Authority level: A3
- Context: AJ Project OS needed a pilot project to validate the multi-agent workflow.
- Decision: Use the AI Virtual Audience / Presentation & Defense Simulator as historical Project 001.
- Consequences: Historical work remains under `projects/project-001-ai-defense-simulator/`. The 10 September renumbering later reassigned this project to canonical P011; historical identity/provenance must not be rewritten.
- Claims affected: Novelty and outcome claims remained subject to research and verification.
- Approved by: AJ explicitly on 2026-09-08.

## DR-005 — Canonical portfolio renumbering
- Date: 2026-09-10
- Status: Approved
- Authority level: A3
- Context: Portfolio priorities/identities were renumbered while substantial historical evidence already used old IDs.
- Decision: Adopt the canonical ID map recorded in `CANONICAL_PROJECT_INDEX.md`; preserve historical folder/document IDs as provenance.
- Consequences: Current identity must never be inferred from a historical folder name alone. Historical evidence is interpreted through the migration map rather than renamed destructively.
- Files/components affected: portfolio control files and all future status/reporting references.
- Approved by: AJ.

## DR-006 — P011 CDER fails independent-novelty same-engine test against P001 EGPCV
- Date: 2026-09-16
- Status: Approved
- Authority level: A3
- Context: Canonical P001 EGPCV and canonical P011 CDER both implement the research-control sequence bounded claims → provenance-aware evidence → gap/contradiction detection → minimum targeted verification → evidence-state update → human judgment. P011 had already accumulated substantial research/documentation, so the collision had to be evaluated without sunk-cost protection.
- Options considered: retain P011 as an eighth independent FYP survivor; narrow CDER further; merge the mechanism family with P001; park/kill P011 entirely.
- Decision: **PARK P011 as an independent FYP candidate and MERGE its research-mechanism family with P001.** Preserve CDER as historical/reusable research and a potential dissertation/project-defense application/evaluation domain for the generalized evidence-gap verification family.
- Rationale: Domain inputs, evidence adapters and probe forms differ, but no sufficiently distinct mechanism-level contribution has been demonstrated. A generalized evidence-gap verification engine could implement both by swapping domain adapters, claim ontologies, admissibility/policy rules and probe libraries.
- Consequences: The independent FYP survivor set becomes P001, P003, P004, P006, P007, P009 and P010. P011 remains visible as a collision/merge reference. No P011 files are deleted or renamed. This decision does not authorize implementation or automatic expansion of P001 scope.
- Files/components affected: `CANONICAL_PROJECT_INDEX.md`, `PORTFOLIO_RESEARCH_TRACKER.md`, `PROJECT_PORTFOLIO_CATALOGUE.md`, final portfolio comparison records.
- Claims affected: P011/CDER is not treated as a separate novelty contribution. Its reported Chapters 1–2 v2 audit remains historical evidence, but current GitHub/Drive synchronization/freeze is not verified.
- Approved by: AJ explicitly on 2026-09-16.

## DR-007 — Final portfolio comparison precedes implementation
- Date: 2026-09-16
- Status: Approved
- Authority level: A3
- Context: The P001/P011 collision demonstrated that substantial documentation and plausible bounded mechanisms can still fail cross-project novelty analysis.
- Decision: Do not begin Chapter 3 or survivor implementation merely because a project reached a conditional/provisional research gate. First normalize and adversarially compare all seven independent FYP survivors.
- Rationale: The portfolio must select on research defensibility, experimental quality and feasible academic contribution rather than sunk effort or historical priority.
- Consequences: Before scoring/ordering, reconstruct each survivor as current bounded mechanism → strongest prior art → strongest novelty attack → feasibility attack → experiment attack → surviving contribution → failure condition. Research quality, documentation maturity and implementation progress remain separate dimensions.
- Approved by: AJ explicitly on 2026-09-16.
