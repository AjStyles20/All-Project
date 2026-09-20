# P003 — Frozen Independent Reviewer Package Contract v1

## Purpose
Define exactly what an independent reviewer receives and exactly what must be returned. This contract is frozen before real B2 outputs are available.

## Reviewer receives
For each review package:
- package ID and protocol version;
- case ID;
- frozen evidence-packet identity and SHA-256;
- blinded atomic claims (blind ID, text, claim type);
- fixed instructions and judgment definitions;
- the evidence/counterevidence material authorized by the frozen packet.

Reviewer material must not expose B2/B3 identity, generation number where revealing, expected ETEC state, construction expectation, later comparative metrics, or another reviewer's answers.

## Required response per claim
One of:
- SUPPORTED
- PARTIALLY_SUPPORTED
- UNSUPPORTED
- CONTRADICTED
- INDETERMINATE

and a non-empty rationale.

A reviewer submission must cover exactly the package's frozen blinded claim set: no omitted claims, extra claims or duplicates.

## Package integrity
The complete reviewer-facing package is canonically serialized and SHA-256 hashed. If evidence, wording, claims or instructions change, the package hash changes and a new version is required.

## Reviewer qualification record
External execution must separately preserve a reviewer qualification record sufficient to explain why the reviewer is competent to assess the economic/evidentiary claims. The software package does not manufacture or certify expertise.

## Workflow
1. Real B2 runs are captured immutably.
2. Atomic claims are extracted without support labels.
3. B2/B3 claims are blinded.
4. Frozen reviewer packages are generated and hashed.
5. Independent reviewers return complete submissions.
6. Submissions are converted to review batches and locked.
7. Only then may the analysis authorization gate permit unblinding/comparison.

## Boundary
This contract prepares external review. It is not itself human validation and does not complete M9.
