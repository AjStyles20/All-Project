# P001 M8 — End-to-End Instrument Audit v1

Scope: CASE-PILOT-001 and CASE-PILOT-003 constructed dry-run package. Status: pre-assessor audit; not validation evidence.

## Result

The audit found three correctable instrument-consistency issues. No assessor data exist, so correction does not contaminate observations.

A1: The human CASE-PILOT-001 pack shows the literal artifact while the machine package previously exposed only a generic artifact description. BLOCKING; corrected by freezing the literal artifact in machine evidence.

A2: The human pack shows the three supplied tests/results while machine evidence previously said only that supplied tests pass. BLOCKING; corrected by freezing the literal supplied test/result record.

A3: The protocol asks for case_version and task_version, while ProgrammingCase currently has one version field. For this bounded pilot, task_version must be explicitly defined as equal to case.version and checked as such until a separate task entity/version is justified. BLOCKING FOR FORMAL READINESS until encoded.

Checks passed: construction expectations absent from assessor package; B0-B4 outputs/reference state absent; CASE-PILOT-003 literal response synchronized; CONTRADICTED not ordinary wrong/incomplete response; assessor disagreement preserved; missing timing not zero; B2/B4 common timing rule; real-student collection not authorized; constructed cases not independent ground truth.

Gate: encode A3, add regression tests for evidence equivalence, rerun CI, then re-audit readiness. Do not send the package to an assessor before corrections are verified.
