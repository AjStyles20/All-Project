# P001 M8 Pilot Case Manifest — PILOT-CC3-v1-candidate

**Status:** constructed-case dry-run candidate; not real-student evidence.
**Bounded claim:** Competence Claim 3 (CC3) — Test Design.
**Purpose:** test assessor/rubric clarity before M9 Method Freeze.

## Common task family

Each case presents a small deterministic Python function plus frozen task requirements and supplied tests/reference outputs. Assessors judge only the evidence made available under the applicable method boundary. No arbitrary candidate code needs to be executed by the M7 research API.

## Cases

| Case ID | Condition intentionally represented | Expected procedural stress | Development expectation (not ground truth) |
|---|---|---|---|
| CASE-PILOT-001 | Supplied tests pass; no independent test-design evidence | Distinguish final correctness from CC3 evidence | UNRESOLVED before independent verification |
| CASE-PILOT-002 | Independent test proposal has relevant input, correct expected result, defensible reason | Clear positive anchor | SUPPORTED candidate |
| CASE-PILOT-003 | Independent proposal is relevant but expected result/reason is incomplete | PARTIAL boundary | PARTIAL candidate |
| CASE-PILOT-004 | Response does not defensibly satisfy any structured test-design dimension | PARTIAL vs UNRESOLVED | UNRESOLVED candidate |
| CASE-PILOT-005 | Materially conflicting admissible CC3 evidence | CONTRADICTED boundary + human review | Do not force ordinary incompleteness into CONTRADICTED |
| CASE-PILOT-006 | CC3 already has admissible independent support before targeted verification | Negative-control / unnecessary verification | B4 should not ask a targeted probe if frozen rules already support CC3 |
| CASE-PILOT-007 | EG-T3 exists but the adequate executable probe is unavailable/exhausted under frozen configuration | No-valid-probe stress | HUMAN_REVIEW_REQUIRED |
| CASE-PILOT-008 | Assistance context is disclosed/permitted but independent CC3 evidence remains insufficient | Competence vs integrity separation | May remain UNRESOLVED without misconduct inference |

## Case construction rules

1. Each case receives a frozen task text, artifact/evidence bundle and expected reference behavior before assessor dry run.
2. Case construction notes are hidden from assessors during independent judgment where they could bias the reference state.
3. B0-B4 receive only their permitted evidence boundary.
4. `fixed_viva` evidence is never re-labelled as `targeted_verification`, or vice versa.
5. A development expectation is used to test machinery and rubric clarity; it is not independent ground truth.
6. If an assessor identifies a plausible state not anticipated here, preserve the disagreement and rationale rather than editing the answer after the fact.
7. Material case changes increment the manifest/corpus version.

## Dry-run freeze fields

Before administering a case, record: case_id; case_version; task_version; claim_version; corpus_version; assessor_rubric_version; B0-B4 method/config versions; evidence bundle IDs; B2 question-set version; B4 probe-catalogue/evaluator version; timing-procedure version.

## Promotion rule

A case may enter the actual pilot set only after its wording, evidence bundle and intended methodological stress are internally reviewed for ambiguity. Promotion does not convert its construction expectation into ground truth.
