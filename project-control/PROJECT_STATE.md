# Project State

## Project Identity
- Project name: AJ Project OS
- Project type: Research-first final-year-project portfolio and implementation workspace
- Project owner: AJ
- Last verified date: 2026-10-29 (P001 implementation/PR status; research sections unchanged since 2026-09-20)
- Repository: AjStyles20/All-Project
- Default branch: main

## Canonical Portfolio State
Canonical identity is controlled by `project-control/CANONICAL_PROJECT_INDEX.md`. Historical folder numbers are preserved for provenance.

Independent FYP survivors after the completed research and comparative selection work remain P001, P003, P004, P007, P009 and P010. P011 remains parked as an independent FYP because its evidence-gap verification mechanism collides with P001. P006 remains parked as an independent FYP.

## Current Implementation Decision
Decision Record DR-010 prospectively supersedes the earlier implementation prohibition after completion of the comparative selection work.

- **P001 — Intelligent Coding Examination Platform:** first research-critical implementation target.
- **P003 — Geopolitical Economic Risk to Economic Impact Forecasting & Warning:** second implementation target.
- P003 should not begin until the agreed P001 checkpoint unless AJ changes the order.
- P004, P007, P009 and P010 remain survivors/reserves; no full implementation is authorized merely by survivor status.

## P001 Current State
Historical GitHub folder: `projects/project-007-coding-examination-platform`.
Research-critical implementation: branch `p001-egpcv-implementation`, PR #17, **merged into main on 2026-09-22** (merge commit `cb29f06…`). Latest main CI: run #292, success, head `2596768…`.

Full-product layer (MySQL, per the MySQL technology decision in `documentation/DATABASE_TECHNOLOGY_DECISION_MYSQL.md`):
- **FD-01 Identity/RBAC** — on main. Live MySQL test passed on 2026-10-29 (MySQL 8.4.9 disposable local instance; see TE-005).
- **FD-02 Examination & Question Management** — branch `p001-fd02-exam-question-management`, **draft PR #19, not merged**. Status: IMPLEMENTED / UNIT + API TESTED / **LIVE VERIFIED on MySQL 8.4.9** (disposable local instance, 2026-10-29; AJ's own server not used). As of 2026-10-29 it includes examiner list/read/update/detach endpoints, compare-and-set lifecycle transitions, DRAFT-guarded SQL, and a scheduling-requires-a-question rule (A2, awaiting AJ review). See `documentation/FD02_EXAMINATION_QUESTION_DESIGN.md`.
- **FD-03 Candidate Assignment, Session & Response Capture**: branch `p001-fd03-candidate-sessions`, stacked on FD-02, with a draft PR targeting the FD-02 branch. Status: IMPLEMENTED / UNIT + API TESTED. **Not live-MySQL verified.** Four policy points await AJ. See `documentation/FD03_CANDIDATE_SESSION_DESIGN.md`.

Residual contribution: **Evidence-Gap-Driven Programming Competence Verification (EGPCV)**, narrowed to competence-gap-driven bounded minimum independent evidence acquisition rather than generic adaptive viva, browser coding, proctoring, or code-conditioned questioning.

Implemented research-critical scope includes:
- M1 core domain model and SQLite persistence;
- M2 bounded CC3 Test Design evidence evaluator and EG-T3 gap detector;
- M3 B4 targeted-verification vertical slice;
- M4 immutable audit/traceability and generic stop/human-review control;
- M5 distinct B0-B3 baseline engines, B2 fixed-viva development comparator, evidence-leakage controls, separate burden dimensions, and method/reference records;
- M6 persistent experiment identity, frozen B0-B4 method/configuration versions, per-method observations, independent reference judgments, experiment completeness gate, automatic B0-B3 execution, and bounded B4 integration;
- formal B0-B4 development research experiment specification.

Latest directly verified GitHub Actions checkpoint: **run #159 — 98 passed, 0 failed, 1.57s** at commit `a2a7bb6...`. This is software verification only; it is not scientific validation.

## P001 Scientific Status
Development mechanics are implemented for the bounded CC3/EG-T3 slice. VP-CC3-02 is the currently executable targeted development probe. VP-CC3-03 is potentially sufficient but not executable and is therefore rejected rather than used as an automated fallback.

The final competence ontology, PARTIAL/UNRESOLVED boundary, final probe library, assessor reliability method, corpus/sample size, participants if any, numerical thresholds, accessibility validation, Examination Capability Contract implementation, secure untrusted-code execution, and held-out final evaluation remain unfrozen or pending.

No superiority, authorship, AI-use detection, perfect cheating detection, lecturer replacement, or complete programming-competence claim is established.

## Historical P011 Warning
Historical Source-Grounded AI Defense Simulator / canonical P011 test claims must not be transferred to P001. Any historical approximately-146-test claim belongs to a different implementation lineage and remains separate from the verified P001 suite.

## Open Pull Requests (observed 2026-10-29)
- **#19** P001 FD-02. Draft and mergeable. Merge awaits AJ plus live-MySQL evidence.
- **#18** P003 ETEC research-critical implementation. Draft, 100 commits, currently **conflicting** with main. Not touched in the 2026-10-29 cycle.
- **#1–#16** are historical branches from the earlier Source-Grounded AI Defense Simulator lineage (now canonical P011 per `CANONICAL_PROJECT_INDEX.md`). They are still open and reported mergeable. Whether to close or keep them is AJ's decision.

## Current Work
1. Obtain live-MySQL evidence for FD-01/FD-02 (`P001_RUN_MYSQL_TESTS=1` against AJ's local server), then AJ review and merge of PR #19.
2. Review FD-03 (opened 2026-10-29) and resolve its policy points, then live-MySQL verification. Next increment after FD-03: examiner review of submissions and evidence registration (FR-08, FR-12).
3. Prepare pilot and method-freeze materials without treating development fixtures as independent ground truth.
4. Do not begin P003 implementation until the P001 checkpoint is reached unless AJ changes the order.

### Superseded current-work list (2026-09-20)
1. Keep P001 on its separate implementation branch until the agreed merge gate. *(PR #17 has since merged.)*
2. Complete governance/documentation synchronization and remaining M6 hardening.
