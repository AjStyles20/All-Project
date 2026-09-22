# P001 Formal Research Experiment Specification

**Project:** P001 — Intelligent Coding Examination Platform
**Mechanism:** Evidence-Gap-Driven Programming Competence Verification (EGPCV)
**Status:** Development protocol; final scientific thresholds and sample sizes remain unfrozen.

## 1. Research question
For bounded programming competence claims, can evidence-gap-driven targeted independent verification reduce unresolved claims or verification burden while preserving or improving agreement with independent expert judgments, compared with simpler assessment baselines? A working prototype is not evidence that the answer is yes.

## 2. Unit of comparison
The comparison unit is one eligible Programming Case × Competence Claim pair. Every method within a run uses the same frozen case, claim, corpus version, and applicable policy context. The first implemented slice is Competence Claim 3 (CC3), Test Design, with EG-T3, Missing Independent Test Design Evidence.

## 3. Methods
- **B0 — Baseline 0:** final submission plus ordinary tests/rubric.
- **B1 — Baseline 1:** B0 plus controlled programming-process/event evidence.
- **B2 — Baseline 2:** B1 plus a pre-frozen generic fixed viva; questions are not gap-selected.
- **B3 — Baseline 3:** evidence-centered competence model using admissible non-verification evidence, with no targeted follow-up.
- **B4 — Baseline/Method 4:** EGPCV: evidence model → gap → adequate probe set → lowest-burden candidate → independent response → state update → stop/continue/human review.

Simpler baselines must not be intentionally weakened to make B4 appear better.

## 4. Evidence-access and leakage rules
All methods start from the same underlying case evidence collection but receive only their frozen information boundary. B0 excludes process and verification evidence. B1 adds process but excludes verification. B2 may use verification only when provenance is explicitly fixed-viva. B3 excludes verification. B4 creates targeted-verification evidence. B4 evidence must never be back-fed into B0-B3 for the same comparison. Unmarked verification is not B2 fixed-viva evidence.

## 5. Applicability and evidence states
Applicability is separate from evidence state.

Applicability: REQUIRED; NOT_APPLICABLE.
Evidence states: SUPPORTED; PARTIAL; UNRESOLVED; CONTRADICTED.

The scientific PARTIAL/UNRESOLVED boundary remains subject to assessor/pilot validation and must be frozen before final evaluation.

## 6. B4 bounded-minimum rule
“Minimum” means lowest burden within the pre-frozen candidate set after adequacy filtering, not globally minimal possible questioning.

A probe is eligible only if it is: (1) admissible for the claim/gap; (2) potentially sufficient under the frozen catalogue; (3) supported by a frozen executable response evaluator; and (4) unused in the current verification run. Only then may burden determine selection. If no adequate unused probe remains, the automated path terminates in HUMAN_REVIEW_REQUIRED.

## 7. Independent reference judgment
The system's output is never its own ground truth. Reference judgments must come from an independent computer-science assessor using a frozen assessor rubric. Assessor identity, claim, judgment, rationale, and rubric version are recorded separately from method outputs. Designed development cases are not independent ground truth merely because expected behavior is known to the developer.

Inter-rater agreement may be added where multiple assessors are available. The final statistic and acceptance criterion remain unfrozen.

## 8. Outcomes
Primary outcomes are: agreement with independent expert judgment; reduction in unresolved required claims; and verification burden required to resolve a target gap.

Burden is reported separately as question/probe count, measured verification time, and per-question/probe complexity. No unvalidated weighted composite burden score is used.

Secondary/contextual outcomes may include unnecessary-verification rate, false integrity escalation, examiner review effort, usability, perceived fairness, and accessibility failures. Numerical success thresholds are not declared before pilot evidence justifies them.

## 9. Experimental phases
### Phase A — Development
Build/debug claims, evidence rules, gap taxonomy, probe catalogue, evaluators, persistence, auditability, and experiment mechanics. Development cases may be repeatedly inspected and modified and are not held-out confirmatory evidence.

### Phase B — Pilot
Test task clarity, assessor rubric, response evaluators, timing, burden categories, evidence-state boundaries, and operational feasibility. Material revisions create new versions.

### Phase C — Method Freeze
Before final evaluation freeze at minimum: competence-claim model; evidence-state rubric; gap taxonomy; B0-B4 versions/configurations; B2 fixed-viva contract; B4 probe catalogue/evaluators; assessor rubric; corpus/task definitions; outcome calculations; provenance rules.

### Phase D — Held-Out Final Evaluation
Final cases must not have been used to tune methods/rubrics. Frozen methods run without post-hoc alteration. Deviations, failures, missing data, human escalations, and negative results are retained rather than silently removed.

## 10. Experiment-run reproducibility
Each run records experiment ID, case ID, claim ID, corpus version, assessor-rubric version, B0-B4 method/configuration versions, evidence IDs exposed to each method, resulting state, burden, independent reference, timestamps, and terminal status.

A run cannot be COMPLETE until B0-B4 and the independent reference are present. Completed observations are not silently overwritten.

## 11. Negative and mixed results
Valid outcomes include: B4 adds useful resolution; B3 is sufficient; B2 resolves the same gaps at acceptable workload; B1 is sufficient for the bounded claim; B4 adds burden without meaningful benefit; B4 causes unacceptable false escalation/fairness/accessibility/operational problems; or no adequate automated probe exists and human review is required. Results must not be reinterpreted merely to preserve a positive EGPCV conclusion.

## 12. Integrity and competence separation
Observation is interpreted under the Examination Capability Contract (ECC) before integrity meaning is assigned. A competence gap is not misconduct evidence. An integrity concern does not automatically establish lack of competence. The prototype does not automatically determine cheating, authorship, disciplinary outcome, final marks, or overall programming competence.

## 13. Missing-data and failure handling
Missing evidence is not invented. Missing burden timing is not recorded as zero when verification occurred. A failed/unavailable evaluator is not treated as successful. An unexecutable probe cannot be selected merely because it appears potentially sufficient. Human-review cases remain human-review outcomes unless a pre-frozen protocol specifies otherwise.

## 14. Current limitations
Only the bounded CC3/EG-T3 B4 path has an implemented structured targeted-response evaluator. VP-CC3-02 is currently executable. VP-CC3-03 is potentially sufficient but not executable and cannot be selected. The final CC1-CC6 ontology, PARTIAL/UNRESOLVED criteria, corpus size, assessor count, agreement statistic, and numerical thresholds remain scientifically unfrozen. ECC management, full process capture, integrity observations, accessibility handling, secure untrusted-code execution, and the full examination platform remain outside the current vertical slice.

## 15. Forbidden inferences
This experiment does not by itself prove AI use/non-use, code authorship, perfect cheating detection, complete programming competence, lecturer replacement, EGPCV superiority to all coding-exam methods, or hypothesis validity merely because the prototype works.

## 16. Entry condition for final research evidence
Software runs may be development evidence immediately. A run may be treated as final comparative research evidence only after the relevant methods, configurations, assessor rubric, corpus, evidence rules, and outcome calculations are frozen for final evaluation. Material post-freeze changes must be versioned and their effect on comparability documented.
