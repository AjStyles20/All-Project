# P001 Independent Assessor Protocol — Candidate v1.0

## Purpose

Independent assessors provide a reference judgment against which B0–B4 outputs can be evaluated. The P001 system must not generate its own ground truth.

## Assessor role

An assessor should have suitable Computer Science/programming-assessment competence and independently judge bounded competence evidence.

For each applicable claim, record:
- applicability;
- evidence state;
- evidence relied upon;
- rationale;
- whether additional evidence is needed;
- human-review concern where applicable.

## Independence

During initial judgment, assessors should not be shown B4's predicted state, selected probe rationale or claimed method advantage when this could bias their reference judgment.

## Multiple assessors

Pilot procedure:
1. Assessor A judges eligible cases.
2. Assessor B independently judges the same eligible cases.
3. Preserve disagreements.
4. Measure raw agreement at minimum.
5. Inspect disagreement causes.
6. Refine ambiguous rubrics only during the permitted development/pilot phase.
7. Repeat/freeze before held-out final evaluation.

Cohen's kappa or another chance-corrected statistic may be used if justified by the final design, but no statistic is frozen merely because it is familiar.

## Reference judgment

A reference judgment may combine known case construction, reference solutions, deliberately introduced evidence conditions and independent assessor judgments. Designed development cases are not automatically independent ground truth.

## Prohibited shortcuts

- Do not use B4 output as its own reference.
- Do not resolve assessor disagreement silently.
- Do not label synthetic development cases as real student observations.
- Do not tune final-evaluation labels after seeing method outcomes.
