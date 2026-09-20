# P001 Baseline Decision Semantics — Development Contract

This contract prevents B0-B3 from becoming four labels around the same evaluator.

## Shared rule

All methods operate on the same eligible Programming Case where the experiment requires comparability. A method may use only the evidence and mechanism explicitly permitted by its contract. Missing access is not replaced by inference.

## B0 — Outcome-oriented artifact assessment

B0 represents ordinary final-submission assessment. It may use final artifact, ordinary execution/test outcomes and rubric evidence.

B0 answers an **artifact-performance question**, not a competence-evidence question:

> What does the final submission and ordinary assessment evidence support about the submitted solution?

For competence claims that intrinsically require independent process/reasoning evidence, B0 must not manufacture support from final correctness alone. For current CC3 Test Design, supplied-test success is insufficient to establish independent test-design competence.

## B1 — Artifact assessment plus process observations

B1 adds controlled process/event evidence to B0.

Process evidence may strengthen, weaken or contextualize what happened during the examination, but an observation is not automatically a competence judgment or misconduct verdict. For CC3, process logs do not by themselves establish that the candidate can independently design a useful test unless the frozen claim rule explicitly makes a particular process artifact admissible for that purpose.

## B2 — Generic fixed viva

B2 adds a **pre-frozen, same generic viva procedure** for eligible cases. Question choice must not depend on a detected evidence gap or candidate-specific unresolved claim.

B2 may create independent response evidence. Its final response rubric must be frozen before comparative evaluation. Until that rubric is frozen, B2 is architecturally implemented but scientifically incomplete.

## B3 — Evidence-centered competence model without targeted verification

B3 maps admissible artifact/process/execution/rubric evidence to explicit bounded Competence Claims and Evidence States:

SUPPORTED / PARTIAL / UNRESOLVED / CONTRADICTED.

It may expose a gap as an unresolved state, but it must stop there. It may not select or administer a targeted verification probe.

This makes B3 a direct test of whether structured evidence modeling alone is sufficient.

## B4 — EGPCV

B4 begins from the evidence-centered model, detects an explicit Evidence Gap, evaluates a frozen candidate-probe set, selects the lowest-burden admissible and potentially sufficient executable unused probe, incorporates the resulting independent evidence, updates the Evidence State and applies the Stop Rule.

## Current CC3 distinction

For Competence Claim 3 (CC3) — Test Design:

- B0 can observe artifact/tests/rubric, but passing supplied tests does not establish independent test design.
- B1 can additionally observe process events, but generic process presence does not establish independent test design.
- B2 may ask its pre-frozen generic viva question(s), once its response rubric is frozen.
- B3 explicitly represents CC3 as UNRESOLVED when admissible evidence cannot support it, but asks nothing further.
- B4 may convert the explicit CC3 gap into EG-T3 and select targeted independent verification.

## Scientific safeguard

No baseline should be deliberately weakened to make B4 appear superior. If B0, B1, B2 or B3 is sufficient under a fair frozen contract, that is a valid result and may reduce or eliminate the claimed value of B4.
