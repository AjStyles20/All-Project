# P001 Development Corpus Specification — Candidate v1.0

## Partitions

P001 separates:
1. **DEVELOPMENT** — design/debug cases; may inform mechanism changes.
2. **PILOT** — tests rubric/assessor clarity before final freeze.
3. **FINAL_EVALUATION** — held out after method freeze.

Final-evaluation cases must not be used to tune the mechanism.

## Seed development cases

The current eight seed concepts are DEVELOPMENT cases, not observed student data:

- C1 correct loop solution/no process evidence → trace execution.
- C2 polished function program → parameter/scope variant.
- C3 passes supplied tests → design a boundary test.
- C4 fixed bug/process unclear → diagnose a related defect.
- C5 list-processing solution → explain list-versus-set consequence.
- C6 recursive solution → identify base/general case and reason about changed input.
- C7 partially correct code/strong explanation → bounded modification.
- C8 correct code with assistance disclosure → assistance-free explain/modify verification.

## Required stress cases

The development corpus should include:
- **negative control:** all REQUIRED claims already supported → zero targeted probes;
- **contradiction stress:** conflicting evidence → preserve contradiction/human-review path;
- **no-valid-probe stress:** material gap but no adequate probe → HUMAN_REVIEW_REQUIRED;
- **assistance-context stress:** disclosed/permitted assistance may leave independent competence unresolved without implying misconduct.

## CASE-DEV-003

Task family: find even numbers.

Current development expectation:
- CC3 REQUIRED.
- Examiner-supplied tests passing do not establish independent test-design competence.
- Initial CC3 state: UNRESOLVED.
- Gap: EG-T3.
- B4 selects VP-CC3-02 from the current candidate set because VP-CC3-01 is insufficient and VP-CC3-03 has higher burden.
- A complete structured development response may update CC3 to SUPPORTED.
- This expectation is a development fixture, not an independently validated empirical result.

## Versioning

Freeze/version at minimum:
- competence-claim model;
- evidence-state rubric;
- gap taxonomy;
- probe catalogue;
- B0–B4 configurations;
- assessor rubric;
- Examination Capability Contract schema.
