# P001 M8 — Assessor Dry-Run Pack v1.0

Status: constructed dry-run instrument. It contains no participant data, no assessor result, and no claim that validation has occurred.

## Assessor instructions

You are judging one Programming Case × Competence Claim 3 (CC3: Test Design). Judge only the evidence provided for the case. Do not infer authorship, cheating, misconduct, overall programming competence, or performance on evidence not shown.

Choose one evidence state: SUPPORTED, PARTIAL, UNRESOLVED, or CONTRADICTED. Record a rationale. If the boundary is ambiguous, preserve that ambiguity rather than forcing confidence.

SUPPORTED means admissible independent evidence satisfies the frozen CC3 rule. PARTIAL means meaningful independent test-design evidence exists but does not completely satisfy the rule. UNRESOLVED means evidence is insufficient to establish complete or meaningful partial support. CONTRADICTED requires a material conflict relevant to CC3; an ordinary weak, wrong, or incomplete answer is not automatically contradiction.

Do not consult another assessor's answer. Do not treat any B0-B4 system output as a reference answer.

## CASE-PILOT-001

Task: Implement `count_even(values)`, returning the number of even integers.

Frozen artifact:

    def count_even(values):
        count = 0
        for value in values:
            if value % 2 == 0:
                count += 1
        return count

Frozen examiner-supplied execution record:
- `[1, 2, 3, 4]` → `2` — pass
- `[2, 4, 6]` → `3` — pass
- `[1, 3, 5]` → `0` — pass

No additional candidate-authored test-design response is included at this evidence boundary.

Assessor records: state; relevant proposed input dimension Yes/No/Cannot determine; correct expected outcome dimension Yes/No/Cannot determine; defensible reason dimension Yes/No/Cannot determine; rationale; ambiguity; additional evidence needed; human-review concern.

## CASE-PILOT-003

Task context: `count_even(values)` returns the number of even integers in a list.

Frozen independent response:

> Input: `[2, 3]`. Expected output: `2`. Reason: this checks that the function can handle both an even and an odd number.

Judge the response using the same CC3 rubric. Do not assume a construction expectation.

Assessor records: state; the three CC3 dimensions; rationale; ambiguity; additional evidence needed; human-review concern.

## Independence declaration

I made each judgment independently, without seeing another assessor's answer and without treating a system/B4 output as ground truth.
