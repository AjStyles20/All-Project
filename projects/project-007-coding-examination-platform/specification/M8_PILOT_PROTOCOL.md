# P001 M8 Pilot Protocol — Candidate v1.0

**Mechanism:** Evidence-Gap-Driven Programming Competence Verification (EGPCV)
**Bounded claim:** Competence Claim 3 (CC3) — Test Design
**Gap:** EG-T3 — Missing Independent Test Design Evidence
**Status:** Pilot-preparation protocol; no pilot results are reported here.

## 1. Purpose

M8 tests whether the measurement procedure is clear, repeatable and operationally feasible enough for M9 Method Freeze. It is not a confirmatory test that B4 is superior.

The pilot targets ambiguity in CC3 classification, especially PARTIAL versus UNRESOLVED; B2 fixed-viva procedure; B4 admissibility/sufficiency/executability; assessor instructions; timing; and audit/export reconstruction.

## 2. Unit and corpus

One observation is one frozen Programming Case × CC3 pair evaluated under the applicable B0-B4 information boundary. Pilot cases use CASE-PILOT identifiers and a frozen corpus version such as PILOT-CC3-v1. Repeatedly inspected development fixtures cannot simply be relabeled as pilot evidence.

The pilot corpus should cover: absent independent test-design evidence; clearly complete independent evidence; partially adequate evidence; no meaningful evidence; a human-review condition; and, if the frozen rules permit it, a case where targeted verification is unnecessary because CC3 is already supported.

Exact pilot sample size remains unfrozen until case and assessor workload are reviewed.

## 3. Candidate CC3 state rubric

**SUPPORTED:** admissible independent evidence satisfies the frozen CC3 support rule. For the current structured test-design response, proposed input is relevant, expected outcome is correct, and the reason/usefulness is defensible.

**PARTIAL:** relevant independent test-design evidence exists but does not satisfy the complete support rule. Under the current response model, at least one but not all required dimensions is defensibly present.

**UNRESOLVED:** admissible evidence is insufficient to establish complete or meaningful partial support; for example, independent evidence is absent or no required response dimension is defensibly satisfied.

**CONTRADICTED:** admissible evidence contains a material conflict relevant to CC3 that cannot be represented merely as incomplete support. It must not be assigned simply because an answer is wrong, weak or incomplete. The exact scientific contradiction rule remains a pilot item and consequential interpretation requires human review.

Assessors explicitly flag cases where these boundaries cannot be applied confidently. Ambiguity is a pilot finding, not an assessor failure.

## 4. Independent assessor procedure

At least two suitable Computer Science/programming-assessment assessors are preferred when feasible. Each receives frozen materials/rubric, judges independently before seeing another assessor's judgment, is not told that B4 is expected to win, records state plus rationale, records ambiguity rather than guessing, and never uses B4 output as ground truth.

Disagreement is preserved. Raw agreement is reported at minimum. Cohen's kappa or another chance-corrected statistic is considered only if justified by the eventual design/category distribution.

## 5. B2 pilot freeze candidate

B2 remains a generic pre-frozen battery in this order: EXPLAIN; PREDICT/TRACE; TEST DESIGN; MODIFY. For CC3, B2 uses the same relevant-input, correct-expected-output and defensible-reason dimensions as the comparable structured test-design judgment. B2 does not inspect a detected gap to decide whether to ask TEST DESIGN.

## 6. B4 pilot freeze candidate

VP-CC3-01 remains insufficient for EG-T3. VP-CC3-02 is the currently executable bounded independent test-design probe. VP-CC3-03 remains non-executable unless an evaluator is explicitly specified, reviewed and versioned before pilot freeze.

Selection remains: admissible → potentially sufficient → executable → unused → lowest burden rank. No new probe is introduced mid-run to rescue a difficult case.

## 7. Burden procedure

Report separately: question_count; verification_seconds; and frozen LOW/MEDIUM/HIGH complexity per administered item. Timing uses one predeclared procedure. Missing/invalid timing is logged as missing/deviation, never converted to zero unless no verification occurred.

## 8. Data and provenance

Preserve experiment ID; case/task version; claim/version; corpus version; assessor-rubric version; B0-B4 method/config versions; evidence IDs per method; fixed-viva versus targeted-verification provenance; method state; raw burden; independent assessor identity/code and judgment; timestamps; audit events; and deviation/failure status.

If real students participate, institutional consent/ethics, privacy, access, retention and de-identification requirements must be resolved before collection. Constructed cases must not be described as real-student evidence.

## 9. Secure-execution boundary

The M7 research API is not a secure sandbox for arbitrary untrusted candidate code. M8 must not route real untrusted code into unrestricted local execution. Constructed/frozen artifacts or another explicitly safe arrangement may be used for the bounded pilot.

## 10. Failure/deviation log

Preserve missing evidence, unavailable evaluator, no adequate executable probe, HUMAN_REVIEW_REQUIRED, assessor disagreement, missing timing, API/persistence failure, protocol deviation and post-start configuration-change attempts. Each deviation receives an ID, affected run/case, disposition and analysis impact.

## 11. Planned pilot outputs

Before viewing pilot results, report case/claim counts; state distributions; assessor raw agreement/disagreement matrix; unresolved counts by method; B2/B4 question counts and measured time; B4 selection dispositions; HUMAN_REVIEW_REQUIRED count; missing/deviation counts; and qualitative rubric/protocol ambiguities. These diagnose the procedure and are not proof thresholds for EGPCV superiority.

## 12. Exit criteria toward M9

Recommend Method Freeze only when cases are interpretable; assessor ambiguity is acceptably resolved or corrected/re-piloted; PARTIAL/UNRESOLVED has an operational version; B2 remains fixed; B4 catalogue/evaluators are versioned and executable-only; burden capture is reliable; provenance/audit/export reconstruct observations; deviations/disagreements are reviewed; material revisions are versioned/re-piloted where needed; and pilot observations are not represented as held-out final evidence.

## 13. Authorization

This protocol authorizes pilot preparation and constructed-case dry runs. It does not by itself authorize real-student data collection or claim that a pilot has occurred.

Next: create the versioned pilot-case manifest and assessor worksheet/schema for a dry run.
