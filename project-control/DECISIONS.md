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


## DR-011 — P001 FD-02/FD-03 operational policy decisions
- Date: 2026-10-29
- Status: Approved
- Authority level: A2 (product-layer policy; no change to objectives, methodology, stack or EGPCV semantics)
- Context: the FD-02 completion and FD-03 handoffs (`project-control/AGENT_HANDOFFS/2026-10-29_P001_FD02_COMPLETION.md`, `2026-10-29_P001_FD03_OPENED.md`) listed policy points that the implementing agent could not settle on its own. Each was put to AJ with options and a recommendation.
- Decision:
  1. **Scheduling requires content.** DRAFT → SCHEDULED needs at least one attached question. *(Kept as implemented.)*
  2. **Own questions only.** An examiner may attach only questions they created. Another examiner's question is answered as not found (404), so ids cannot be probed. Deliberate sharing may be designed later. *(Changed from the implemented "any question".)*
  3. **Time window optional.** SCHEDULED does not require `starts_at`/`ends_at`. When a window is set, FD-03 enforces it. *(Kept.)*
  4. **One attempt.** One examination session per assignment; a repeated start resumes it. *(Kept.)*
  5. **Late submit allowed.** Submitting after `ends_at` is permitted. It locks only content saved before the deadline, because saves are refused afterwards. *(Kept.)*
  6. **Auto-submit on close.** ACTIVE → CLOSED also finalises every IN_PROGRESS session of that examination in the same transaction. These sessions are recorded as `AUTO_ON_CLOSE`, distinct from candidate submissions. *(New.)*
  7. **Latest response only.** No response revision history for now. History is parked as SP-001 until EGPCV process-evidence requirements define it. *(Kept; parked.)*
  8. **Historical PRs #1–#16 stay open.** No action. *(Kept.)*
- Rationale: least privilege (2); no-loss finalisation of saved work (5, 6); no invented multi-attempt or process-evidence policy (4, 7); the examiner's ACTIVE/CLOSE transitions remain the primary access control (3).
- Consequences: FD-02 adds a question-ownership check. FD-03 adds `submission_mode` to `examination_sessions` (migration 003 has not been applied to any shared database, so it is amended in place) and auto-finalisation in the close transition.
- Files/components affected: `examination_service.py`, `mysql_examination_repository.py`, `candidate_session` domain/service/repository, migration 003, FD-02/FD-03 design documents and tests.
- Claims affected: none (product layer only).
- Approved by: AJ, in the Claude Code session of 2026-10-29. Each point was answered explicitly.
- Supersedes: the "open points" lists in the two handoffs above.


## DR-012 — P001 FD-04 marking policy: weighted total, mark history, results release
- Date: 2026-10-29
- Status: Approved
- Authority level: A2 (product-layer assessment policy; EGPCV semantics unchanged)
- Context: FD-04 (draft PR #21) left three open points: how `score_weight` combines with scores, what happens to superseded marks, and whether candidates see marks.
- Decision:
  1. **Weighted percentage.** Total % = Σ(score ÷ max_score × weight) ÷ Σ(weight) × 100. It is computed exactly and rounded once to 2 dp, and reported alongside the raw total. It is undefined (null) until every question in the session is marked.
  2. **Mark history.** Every saved mark is appended to `response_mark_history` in the same transaction as the current-mark upsert. The current mark is still the default view.
  3. **Explicit release.** Candidates see marks only after the owning examiner releases results. Release requires the examination to be CLOSED (or ARCHIVED) and every session to be SUBMITTED and fully marked. Release is idempotent and locks further marking. Candidates see score, max, comment and totals, not the marker identity or the history.
- Rationale: weight expresses relative importance independent of each question's point scale (1); integrity and auditability of assessment decisions (NFR-02, NFR-03) (2); students never see partial or provisional marks (3).
- Consequences: migration 004 gains `response_mark_history` and `examination_result_releases` (amended in place; it was only ever applied to the disposable test instance). New endpoints: `POST /examiner/examinations/{id}/release` and `GET /candidate/sessions/{id}/result`.
- Claims affected: none.
- Approved by: AJ, in the Claude Code session of 2026-10-29. Each point was answered explicitly.


## DR-013 — Adopt the P001 Examination Capability Contract specification v0.1
- Date: 2026-10-29
- Status: **Approved** (Option A) by AJ on 2026-10-29. The spec is frozen as ECC v1.0.
- Authority level: A3 (research methodology: interpretation rules for observations; freezes an artifact listed in the development-corpus versioning set)
- Context: the formal research spec (§12) requires observations to be interpreted under the ECC. RTM FR-15 is PENDING, and the operational → EGPCV evidence bridge is blocked on it (FD-04 scope decision).
- Proposal: `projects/project-007-coding-examination-platform/specification/EXAMINATION_CAPABILITY_CONTRACT_SPECIFICATION.md`.

DECISION REQUEST DR-013
- **Issue:** adopt the ECC v0.1 specification (capability schema, lifecycle, evidence labelling, interpretation rules R1–R7)?
- **Requirement/objective affected:** FR-15 (directly); FR-16 to FR-19 (bounded); EGPCV interpretation chain.
- **Option A, approve v0.1 as drafted:**
  - Pro: unblocks FD-05 (ECC management) and FD-06 (evidence bridge); formalises existing PASS_003 to PASS_005 material without new claims.
  - Con: the capability set is fixed until a schema revision.
- **Option B, approve with changes to the open questions Q1–Q5:**
  - Pro: AJ tailors binding point, mapping and defaults.
  - Con: a revision cycle before implementation.
- **Option C, defer the ECC:**
  - Pro: no methodology freeze yet.
  - Con: the evidence bridge stays blocked; FR-15 to FR-19 remain PENDING.
- **Project Lead recommendation:** Option A, answering Q1–Q5 with the proposed defaults unless AJ prefers otherwise.
- **Reason:** the draft only operationalises approved research material and existing code fields. It keeps the ECC non-enforcing and verdict-free.
- **Requires AJ approval:** YES
- **AJ resolution (2026-10-29):** Option A, with Q1–Q5 answered as proposed:
  - Q1: capability set as drafted;
  - Q2: bind on SCHEDULED;
  - Q3: responses become ARTIFACT and the contract POLICY_CONTEXT; marks are not mapped;
  - Q4: question → case linking is an explicit research step;
  - Q5: LAB_CONTROLLED by default.
- **Consequences:**
  - FR-15 is SPECIFIED / APPROVED;
  - FD-05 (ECC management) is unblocked;
  - FD-06 (evidence bridge) needs an explicit research-link step.


## DR-014 — Apply ECC exception extra time to the candidate's deadline
- Date: 2026-10-29
- Status: Approved
- Authority level: A2 (product-layer behaviour)
- Context: FD-05 (PR #23) recorded exception extra time but did not apply it to FD-03 deadlines, so a candidate promised more time could have been cut off.
- Decision: a candidate's effective deadline is the examination's `ends_at` plus the **largest single** extra-time grant recorded for that candidate. Start and save checks use it, and the candidate's session view shows it (`my_ends_at`).
- Rationale: candidates must actually receive accommodations they were granted. Using the largest grant rather than the sum means re-recording an exception never silently stacks time; an examiner who wants more time grants a larger exception.
- Consequences: `CandidateSessionService` takes an optional contract repository. Other capabilities in exceptions remain declarative (DECLARED, NOT ENFORCED).
- Approved by: AJ, in the Claude Code session of 2026-10-29. The "largest single grant" rule is the implementing agent's choice and is flagged here for AJ review.
