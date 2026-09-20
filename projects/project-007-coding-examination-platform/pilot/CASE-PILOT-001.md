# CASE-PILOT-001 — Evidence Bundle v1.0

**Corpus:** PILOT-CC3-v1-candidate
**Claim:** CC3 — Test Design
**Status:** constructed dry-run material; not real-student evidence and not independent ground truth.

## Frozen task

A student is given the following function specification:

`count_even(values)` receives a list of integers and returns the number of even integers in the list.

Frozen submitted artifact:

    def count_even(values):
        count = 0
        for value in values:
            if value % 2 == 0:
                count += 1
        return count

Examiner-supplied tests shown in the case bundle:

- `[1, 2, 3, 4]` → `2`
- `[2, 4, 6]` → `3`
- `[1, 3, 5]` → `0`

For this constructed case, the supplied tests are recorded as passing. This is a frozen case condition, not a claim that real candidate code was executed by the research API.

## Evidence bundle

- `P001-EV-A1` — ARTIFACT — submitted function shown above — source `constructed_pilot_artifact`.
- `P001-EV-X1` — EXECUTION — frozen record that the three examiner-supplied tests pass — source `constructed_reference_execution`.
- No independent candidate-authored test-design evidence is present at the initial boundary.

## Intended methodological stress

The case asks whether final correctness plus examiner-supplied tests are mistakenly treated as evidence that the candidate can independently design tests. Under the current CC3 development rule, they are not sufficient by themselves.

## B0-B4 dry-run boundary

- B0: artifact + ordinary supplied-test/rubric evidence.
- B1: same bundle; no additional real process evidence is invented for this constructed case.
- B2: B1 plus the frozen generic fixed-viva battery when administered.
- B3: structured evidence-centered mapping of admissible non-verification evidence; no targeted follow-up.
- B4: structured evidence model; if CC3 remains unresolved, detect EG-T3 and apply the frozen targeted selection policy.

## B2 TEST DESIGN item fixture

Generic family: TEST DESIGN.

Case fixture prompt: `Give one additional test input for count_even that is not one of the supplied tests. State the expected result and explain what useful behavior or boundary the test checks.`

This item is part of B2's pre-frozen battery and is not selected because EG-T3 was detected.

## B4 candidate response fixture for dry-run machinery

VP-CC3-02 prompt: `Design one additional test for count_even. Give the input, expected output, and why this test is useful.`

A positive machinery fixture may use:
- input: `[]`
- expected: `0`
- reason: checks the empty-list boundary and verifies that the function returns zero when there are no values to count.

This fixture exists to exercise the evaluator. It must not be shown to an independent assessor before that assessor records a reference judgment.

## Construction expectation — hidden from assessor

Initial CC3 is expected by the current development rule to remain UNRESOLVED until independent test-design evidence is supplied. This expectation tests the machinery and rubric; it is not the assessor's ground truth.

## Safety/provenance note

No untrusted code execution is required. The artifact and execution record are frozen constructed materials. If later replaced by observed participant evidence, the source/provenance and ethics status must change accordingly.
