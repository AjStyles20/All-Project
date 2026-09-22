# P001 M8 — Pre-Assessor Audit Closure

Status: candidate closure pending CI verification of the listed implementation commits.

The three findings from M8_INSTRUMENT_AUDIT_V1 are addressed as follows:

- A1 literal artifact equivalence: corrected in machine evidence.
- A2 supplied-test/result equivalence: corrected in machine evidence.
- A3 task version ambiguity: bounded pilot rule explicitly defines task_version = case.version. AssessorPackage exposes both names, and the readiness path documents/checks the alias. A separate Task entity is deferred unless later methodology requires independent task versioning.

Regression tests require CASE-PILOT-001 machine evidence to contain the literal count_even artifact and all three frozen supplied tests/results; CASE-PILOT-003 to contain the exact frozen response; and hidden construction/reference fields to remain absent.

If CI is green, the first two-case package is PRE-ASSESSOR READY for independent dry-run judgment under the existing M8 authorization. This means the instrument may be shown to assessors; it does not mean the pilot is validated, complete, or scientifically successful.

Still external/human-dependent: Assessor A judgment; preferably Assessor B independently; actual B2/B4 administration timing; disagreement/ambiguity review; versioned revision if the dry run exposes rubric/protocol problems.
