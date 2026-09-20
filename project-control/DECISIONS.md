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
- Decision: Use GitHub for application code, tests, technical documentation, and canonical project-control Markdown files.
- Consequences: Agents synchronize technical state through this repository rather than relying only on chat memory.

## DR-002 — Use Google Drive for academic/supporting workspace
- Date: 2026-09-08
- Status: Approved
- Authority level: A2
- Decision: Use connected Google Drive for research and academic/supporting artifacts while keeping technical state in GitHub.
- Consequences: Critical state should still be reflected in project-control files when it affects implementation or claims.

## DR-003 — Independent verification gate
- Date: 2026-09-08
- Status: Approved
- Authority level: A2
- Decision: Substantial implementation work must be independently challenged before being accepted as verified.
- Consequences: `IMPLEMENTED` is not equivalent to `VERIFIED`.

## DR-004 — Instantiate historical Project 001 as AI Virtual Audience / Presentation & Defense Simulator
- Date: 2026-09-08
- Status: Approved
- Authority level: A3
- Decision: Use the AI Virtual Audience / Presentation & Defense Simulator as historical Project 001.
- Consequences: Historical work remains under `projects/project-001-ai-defense-simulator/`. The 10 September renumbering later reassigned this project to canonical P011; historical identity/provenance must not be rewritten.

## DR-005 — Canonical portfolio renumbering
- Date: 2026-09-10
- Status: Approved
- Authority level: A3
- Decision: Adopt the canonical ID map recorded in `CANONICAL_PROJECT_INDEX.md`; preserve historical folder/document IDs as provenance.
- Consequences: Current identity must never be inferred from a historical folder name alone.

## DR-006 — P011 CDER fails independent-novelty same-engine test against P001 EGPCV
- Date: 2026-09-16
- Status: Approved
- Authority level: A3
- Context: P001 EGPCV and P011 CDER share the mechanism-level sequence bounded claims → provenance-aware evidence → gaps/contradictions → minimum targeted verification → evidence-state update → human judgment.
- Decision: **PARK P011 as an independent FYP candidate and MERGE its research-mechanism family with P001.** Preserve CDER as historical/reusable research and a potential dissertation/project-defense application/evaluation domain.
- Consequences: P011 remains visible as a collision/merge reference. No files are deleted/renamed and P001 implementation scope is not automatically expanded.
- Approved by: AJ explicitly on 2026-09-16.

## DR-007 — Final portfolio comparison precedes implementation
- Date: 2026-09-16
- Status: Approved
- Authority level: A3
- Decision: Do not begin Chapter 3 or survivor implementation merely because a project reached a conditional/provisional research gate. Complete adversarial portfolio research and comparative selection first.
- Consequences: Research quality, documentation maturity and implementation progress remain separate dimensions.
- Approved by: AJ explicitly on 2026-09-16.

## DR-008 — Final Portfolio Research Gate freezes residual contribution boundaries
- Date: 2026-09-16
- Status: Approved
- Authority level: A3
- Context: Contribution-type normalization, project-specific falsification/kill searches and residual-materiality/experimental-separability audits showed that several earlier bounded claims still overlapped materially with direct prior art. The gate therefore tested only what remained after removing already-covered mechanisms/methods/empirical questions.
- Decision:
  - **P001 SURVIVES / residual STRONG:** contribution narrowed to competence-gap-driven **minimum independent evidence acquisition**. Adaptive viva/code-conditioned questioning generally are prior art, not the contribution.
  - **P003 SURVIVES / residual STRONG:** contribution narrowed to **typed transmission-edge evidence sufficiency + weakest-link downstream claim progression**. Generic evidence contracts/RAG/provenance/abstention are not the contribution.
  - **P004 PROVISIONAL SURVIVOR / residual FRAGILE:** treat as **modern empirical systems evaluation**, not invention of adaptive/net-benefit transcoding. Scientific materiality remains uncertain and fails if modern conditions merely reproduce established conclusions with different numerical values.
  - **P007 SURVIVES / residual ADEQUATE:** contribution narrowed to **policy/opportunity-relative reward-governance diagnosis + independently validated benchmark**. Generic contextual fairness auditing is not the contribution.
  - **P009 SURVIVES / residual STRONG:** contribution is the empirical **privacy/resource/selective-capture trade-off constrained by measured human task-resumption performance**. Simulated/LLM-rated resumption cannot substitute for the target human outcome.
  - **P010 SURVIVES / residual ADEQUATE:** contribution is the experimentally testable effect of **board state + speaker role + game phase + match contract on speech adjudication**, with an independently constructed/validated contrastive benchmark.
  - **P006 PARK AS INDEPENDENT FYP / residual COLLAPSES:** MEC failed the final same-engine/prior-art attack. Assistance/help-aware mastery modelling/scaffolding plus independent verification and delayed reassessment/relearning substantially reproduce the claimed lifecycle; an explicit evidence-contract/state-machine formalization is insufficient by itself. Preserve Personal Learning World as a valid product/project concept. Do not narrow P006 again during this portfolio gate.
- Rationale: A residual is research-material only if removing it collapses the project into the strongest prior-art baseline and if its added effect can be independently measured. The six survivors retain experimentally separable residuals; P006 does not under the current claim. P004 remains explicitly fragile because empirical novelty/materiality is not yet guaranteed by technical feasibility.
- Consequences: The independent FYP survivor set becomes **P001, P003, P004, P007, P009 and P010**. P006 and P011 are parked as independent FYP candidates for distinct collision reasons. Broader historical claims are **superseded prospectively by this gate**, not erased. Historical research passes, documents and folder identities remain provenance.
- Files/components affected: `CANONICAL_PROJECT_INDEX.md`, `PORTFOLIO_RESEARCH_TRACKER.md`, `PROJECT_PORTFOLIO_CATALOGUE.md`, future comparison/selection records.
- Claims affected: all future novelty/contribution descriptions for P001/P003/P004/P007/P009/P010 must use the residual boundaries above unless a later explicitly approved research decision supersedes DR-008.
- Approved by: AJ explicitly on 2026-09-16.
- Supersedes: broader contribution/status language in earlier portfolio-control summaries where inconsistent; does **not** rewrite historical research evidence.

## DR-009 — Final Comparative Selection Gate required before final FYP selection
- Date: 2026-09-16
- Status: Approved
- Authority level: A3
- Context: Six projects survive the Final Portfolio Research Gate with different contribution types, evaluation burdens and residual strengths. Documentation maturity differs and cannot be used as a proxy for research quality.
- Decision: Before recommending/selecting the final FYP, compare P001, P003, P004, P007, P009 and P010 using a normalized evidence matrix with no arbitrary initial weighted score. Keep separate at minimum: **research defensibility; prior-art distance; experimental strength/falsifiability; evidence/data feasibility; implementation feasibility; evaluation validity; benchmark/human-study burden; scope/time risk; dependency risk; defense explainability; reproducibility; negative-result value; documentation maturity.** Identify genuine trade-offs and Pareto-dominated candidates before any final selection.
- Consequences: P004's **FRAGILE** residual must remain visible. Documentation maturity is reported separately and cannot determine research quality. No Chapter 3 or implementation begins before this gate is inspected and explicitly resolved.
- Approved by: AJ explicitly on 2026-09-16.


## DR-010 — Final Comparative Selection Gate resolved; authorize staged P001 then P003 implementation
- Date: 2026-09-20
- Status: Approved
- Authority level: A3
- Context: The six surviving FYP candidates were compared after DR-009 using residual contribution, falsifiability, evidence/data feasibility, implementation feasibility, dependency risk, defense clarity, reproducibility, negative-result value, engineering substance and research-to-system traceability. P004 remains scientifically fragile; P009 requires a human-participant study; P007 and P010 retain external-validation/materiality dependencies. P001 and P003 retain strong, experimentally separable residuals with feasible local implementation.
- Decision:
  - Select **P001 Intelligent Coding Examination Platform** as the first research-critical implementation target.
  - Select **P003 Geopolitical Economic Risk to Economic Impact Forecasting and Warning System** as the second implementation target.
  - Keep P004, P007, P009 and P010 as research survivors/reserves subject to their existing gates; do not treat this implementation order as a claim that other survivors are globally inferior.
  - For P001, the implementation contribution remains **Evidence-Gap-Driven Programming Competence Verification (EGPCV)**, specifically competence-gap-driven bounded minimum independent evidence acquisition.
  - Authorize research-critical P001 implementation only after/alongside explicit method/specification contracts. Fuller product features remain deferred.
  - P003 implementation should not begin until P001 reaches an agreed checkpoint unless AJ explicitly changes the order.
- Rationale: P001 permits a bounded local experiment with explicit B0–B4 baselines, strong research-to-software traceability, useful negative results, no required external API, and manageable hardware requirements. P003 remains the next implementation candidate but requires careful evidence-chain construction and domain review.
- Consequences: DR-009's implementation prohibition is satisfied and superseded prospectively by this completed selection decision. Historical records remain unchanged. Implementation does not establish scientific superiority; independent assessment and held-out evaluation remain required.
- Files/components affected: P001 specification/implementation; P003 future implementation; portfolio control records.
- Claims affected: future P001 implementation status and future P003 implementation order.
- Approved by: AJ through the completed All-Project selection/implementation workflow and repeated authorization to proceed.
- Supersedes: DR-009 only with respect to the unresolved Final Comparative Selection Gate and implementation prohibition; DR-009's comparison criteria remain historical methodology.
