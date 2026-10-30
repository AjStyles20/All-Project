# P001 B2 Generic Fixed-Viva Contract — Development v1.0

## Purpose

B2 is a fair non-targeted comparator. It asks the same pre-frozen generic viva procedure for every eligible programming case in the comparison set. Questions are not selected from an Evidence Gap and are not adapted to the candidate's current Evidence State.

## Fixed procedure

For each eligible case, B2 asks these four generic families in this order:

1. **Explain** — Explain the purpose of an important part of your submitted solution and how it contributes to the program's result.
2. **Predict/Trace** — Given a bounded input selected from the case fixture, predict or trace the relevant execution and state the expected result.
3. **Test Design** — Give one additional useful test, its expected result, and why the test is useful.
4. **Modify** — Make or describe one bounded change requested by the frozen case fixture and explain the consequence.

The case fixture supplies the concrete code region, input and modification request before evaluation begins. The family/order is identical across eligible cases.

## Non-adaptivity rule

B2 must not:
- inspect an Evidence Gap to choose a question;
- skip a fixed question because a claim already appears supported;
- add a question because a claim is unresolved;
- choose a lower-burden probe for a particular candidate;
- reuse B4's ProbeSelector.

Thus B2 may ask unnecessary questions. That burden is part of the comparison rather than an implementation defect.

## Structured response records

Each fixed-viva response is stored with:
- case ID;
- question family;
- question/fixture version;
- response;
- start/end timestamps when measured;
- assessor/evaluator result;
- rationale.

A response can become independent evidence only under the frozen response rubric for the competence claim being evaluated.

## CC3 Test Design development rubric

For the current bounded CC3 slice, the fixed Test Design question uses the same three observable dimensions already used by the development structured CC3 response rule:

1. input is relevant;
2. expected result is correct;
3. usefulness reason is defensible.

Development state mapping:
- all three satisfied -> SUPPORTED;
- one or two satisfied -> PARTIAL;
- none satisfied -> UNRESOLVED;
- no automatic CONTRADICTED state.

Using the same CC3 response dimensions avoids weakening B2 through a deliberately inferior scoring rule. The methodological difference is question allocation: B2 asks the fixed battery regardless of the evidence gap; B4 selects targeted verification only when its frozen gap/selection rules justify it.

This mapping remains a development rule pending assessor/pilot validation.

## Burden accounting

B2 records:
- number of fixed questions administered;
- measured verification time where available;
- frozen question complexity category.

No arbitrary weighted composite burden score is introduced.

## Fair-comparison safeguard

If B2 reaches comparable expert agreement or resolves the same competence uncertainty at acceptable burden, the experiment must report that result. B4 is not presumed superior.

## Version

Contract identifier: B2-FIXED-VIVA-v1.0-development.
