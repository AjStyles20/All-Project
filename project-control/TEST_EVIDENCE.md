# Test Evidence

All verification evidence should be reproducible where practical. Do not record a PASS without the test, environment, and observed result.

## Test Record Template

### TE-XXX — Test name
- Date:
- Requirement(s):
- Feature/subsystem:
- Test type: Unit / Integration / Live / User / Accessibility / Security / Regression
- Environment:
- Preconditions:
- Procedure:
- Expected result:
- Observed result:
- Status: PASS / FAIL / PARTIAL / NOT RUN
- Evidence:
- Performed by:
- Notes:

---

### TE-001 — GitHub repository access
- Date: 2026-09-08
- Requirement(s): R-013
- Feature/subsystem: Connected technical workspace
- Test type: Live
- Environment: ChatGPT GitHub connector
- Procedure: Query authenticated repository list and retrieve `AjStyles20/All-Project`; then create repository files.
- Expected result: Repository is visible and write operations succeed.
- Observed result: Repository was visible with write/admin permissions and file creation returned successful commit SHAs.
- Status: PASS
- Performed by: ChatGPT

### TE-002 — Google Drive account connection
- Date: 2026-09-08
- Requirement(s): R-013
- Feature/subsystem: Academic/supporting workspace
- Test type: Live
- Environment: ChatGPT Google Drive connector
- Procedure: Query connected Drive profile.
- Expected result: Connected profile is returned successfully.
- Observed result: Connected profile returned successfully.
- Status: PASS
- Performed by: ChatGPT

### TE-003 — Work orchestration
- Status: NOT RUN

### TE-004 — Codex shared-state handoff
- Status: NOT RUN

### TE-005 — P001 FD-01/FD-02 live MySQL integration
- Date: 2026-10-29
- Requirement(s): P001 FR-30 (examiner side), FD-01 identity/RBAC
- Feature/subsystem: P001 MySQL product layer
- Test type: Live
- Environment: MySQL Community Server **8.4.9**: a disposable local instance started from the MySQL 8.4 binaries installed on AJ's Windows PC (`--initialize-insecure`, scratch data directory, 127.0.0.1:3399, X Protocol off). This is **not** AJ's own configured server on port 3307, and that server was not touched. Setup followed `database/mysql/README.md`: bootstrap 000 with a one-off generated test password, then migrations 001–003 as root. Tests connected as the least-privilege `p001_app@127.0.0.1` account (SELECT/INSERT/UPDATE/DELETE only). Python 3.14.0, mysql-connector-python 9.x.
- Preconditions: bootstrap 000 and migrations 001–003 applied; `P001_DB_*` set for `p001_app`; branch `p001-fd02-exam-question-management` at `409d6c5`.
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest tests/integration/test_mysql_identity_live.py tests/integration/test_mysql_fd02_live.py`.
- Expected result: schema check PASS; both live tests pass.
- Observed result: schema check PASS; 2 passed in 8.86s.
- Status: PASS
- Evidence: `FULL_DEVELOPMENT_WORK_LOG.md`, entry "FD-01/FD-02 live MySQL evidence (2026-10-29)".
- Performed by: Claude Code (Engineering)
- Notes: this is the implementing agent's own run, not independent Verification (PROJECT_RULES §6). It was not run on AJ's configured server.

### TE-007 — P001 FD-02 live MySQL re-run after DR-011
- Date: 2026-10-29
- Requirement(s): P001 FR-30 (examiner side); DR-011 (2)
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (re-initialised after migration 003 changed), same setup as TE-005: bootstrap 000, migrations 001–003, least-privilege `p001_app`.
- Procedure: `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `c757a96` on `p001-fd02-exam-question-management`.
- Expected result: whole suite passes with no skips, including the foreign-question refusal.
- Observed result: 180 passed, 0 skipped in 93.51s.

### TE-006 — P001 FD-03 live MySQL integration
- Date: 2026-10-29
- Requirement(s): baseline FR-05, FR-06, FR-07; P001 FR-30 (candidate side)
- Feature/subsystem: P001 MySQL product layer, candidate sessions
- Test type: Live
- Environment: same as TE-005.
- Preconditions: migrations 001–003 applied; branch `p001-fd03-candidate-sessions`.
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` (entire suite) at `c5780a3`.
- Expected result: FD-03 schema check PASS; whole suite passes with no skips.
- Observed result: schema check PASS (nine tables); 206 passed, 0 skipped in 99.75s.
- Status: PASS
- Evidence: `FULL_DEVELOPMENT_WORK_LOG.md`, entry "FD-03 live MySQL evidence (2026-10-29)".
- Performed by: Claude Code (Engineering)
- Notes: implementing agent's own run, not independent Verification.

### TE-008 — P001 FD-03 live MySQL re-run after DR-011
- Date: 2026-10-29
- Requirement(s): baseline FR-05/06/07; DR-011 (6)
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (re-initialised after migration 003 changed), same setup as TE-005: bootstrap 000, migrations 001–003, least-privilege `p001_app`.
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `dbbe8eb` on `p001-fd03-candidate-sessions`.
- Expected result: schema check PASS; whole suite passes with no skips, including auto-submit on close.
- Observed result: schema check PASS; 212 passed, 0 skipped in 66.57s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification.

### TE-009 — P001 FD-04 review/marking live MySQL integration
- Date: 2026-10-29
- Requirement(s): baseline FR-12 (operational review); P001 FR-30
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (same setup as TE-005, migrations 001–004, least-privilege `p001_app`).
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `f9f8331` on `p001-fd04-review-marking`.
- Expected result: FD-04 schema check PASS; whole suite passes with no skips. The live FD-04 test should show: marking refused while in progress; revision recorded; re-mark replaces; unanswered question markable; identical re-mark counts as saved; auto-submitted session markable after close; marks frozen after archive.
- Observed result: schema check PASS; 227 passed, 0 skipped in 79.90s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification.

### TE-010 — P001 FD-04 live MySQL re-run after DR-012
- Date: 2026-10-29
- Requirement(s): baseline FR-12; DR-012 (1)(2)(3)
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (same setup as TE-005, migrations 001–004, least-privilege `p001_app`).
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `cad0a95` on `p001-fd04-review-marking`.
- Expected result: whole suite passes with no skips. The live FD-04 test should show: history keeps 7 then 9; release refused while a session is incomplete; idempotent release; marking locked after release; candidate result 9/15 raw and 60.0%.
- Observed result: schema check PASS; 235 passed, 0 skipped in 81.45s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification.

### TE-011 — P001 FD-05 ECC management live MySQL integration
- Date: 2026-10-29
- Requirement(s): RTM FR-15, FR-18 (recording); ECC v1.0 §5, §8
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (same setup as TE-005, migrations 001–005, least-privilege `p001_app`).
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `e502488` on `p001-fd05-ecc-management`.
- Expected result: whole suite passes with no skips. The live FD-05 test should show:
  - scheduling without a contract refused, with the SQL backstop rolling back;
  - an identical re-save found;
  - a bound contract whose recomputed hash equals the stored hash after the MySQL JSON round trip;
  - bound versions not editable;
  - exception visible to its candidate;
  - an amendment superseding v1 without rewriting it;
  - `in_force_at` resolving v1 then v2.
- Observed result: schema check PASS; 256 passed, 0 skipped in 167.63s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification.

### TE-012 — P001 FD-05 extra time applied (DR-014) live re-run
- Date: 2026-10-29
- Requirement(s): RTM FR-18; DR-014
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (same setup as TE-005, migrations 001–005).
- Procedure: `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `c17ccb5` on `p001-fd05-ecc-management`.
- Expected result: whole suite passes with no skips. The live FD-05 test should show the timed exam's effective deadline for the candidate as `ends_at` + 25 minutes.
- Observed result: schema check PASS; 257 passed, 0 skipped in 88.05s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification.

### TE-013 — P001 FD-06 evidence bridge live integration
- Date: 2026-10-29
- Requirement(s): RTM FR-19 (provenance), ECC v1.0 §6; DR-013 Q3/Q4; DR-015
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (same setup as TE-005, migrations 001–006, `p001_app`) plus a temporary SQLite research store initialised by the project schema.
- Procedure: `python -m scripts.check_mysql_connection`; `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `818220b` on `p001-fd06-evidence-bridge`.
- Expected result: whole suite passes with no skips. The live FD-06 test should show:
  - only the currently opted-in candidate bridged;
  - an idempotent re-run;
  - the locked identity mapping;
  - ARTIFACT `policy_version` equal to the bound contract's label;
  - POLICY_CONTEXT hash equal to the bound hash;
  - the full research-store dump containing no candidate, examiner or administrator ID and no withdrawn candidate's answer.
- Observed result: schema check PASS; 270 passed, 0 skipped in 125.74s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification. No real participant data was involved.

### TE-014 — P001 FD-06 withdrawal deletion (DR-016) live re-run
- Date: 2026-10-29
- Requirement(s): DR-016; RTM FR-19
- Test type: Live + full regression
- Environment: fresh disposable MySQL 8.4.9 instance (same setup as TE-005, migrations 001–006) plus a temporary SQLite research store.
- Procedure: `P001_RUN_MYSQL_TESTS=1 python -m pytest -q -W error::DeprecationWarning` at `6005537` on `p001-fd06-evidence-bridge`.
- Expected result: whole suite passes with no skips. The live FD-06 test should show a withdrawal after bridging that:
  - deletes the case;
  - leaves zero evidence rows;
  - removes the code → person link and the bridge records;
  - writes one anonymous log row with the code and `cases_deleted = 1`.
- Observed result: schema check PASS; 277 passed, 0 skipped in 149.18s.
- Status: PASS
- Performed by: Claude Code (Engineering). This is the implementing agent's own run, not independent Verification. No real participant data was involved.

### TE-015 — P001 web UI slice 1 browser verification
- Date: 2026-10-29
- Requirement(s): NFR-08, P001 FR-30 (candidate workflow), PROJECT_RULES §13 and §22
- Test type: Live (browser) + automated
- Environment: Claude desktop built-in browser (Chromium); app served by uvicorn on 127.0.0.1:8001 against a disposable MySQL 8.4.9 instance (migrations 001–006) seeded with test accounts and an ACTIVE timed exam with a bound contract, a 20-minute exception and a research link.
- Procedure: sign in → exam list → rules → research opt-in → start → type answer → simulate a newer save from another tab → type again → attempt submit → reload → answer question 2 → submit immediately → result before release → 375 px viewport → deep link → sign out.
- Observed result:
  - **Autosave:** showed "Saved … (revision n)".
  - **Deadline:** showed the extended end (+20 minutes).
  - **Stale tab:** the edit got 409 and "Not saved: a newer version was saved elsewhere…", and the newer copy was not overwritten.
  - **Submit:** refused while an answer was unsaved; later, Submit flushed the pending question-2 save, then submitted, and the answers became read-only.
  - **Result:** reported "not released yet".
  - **Phone width:** no horizontal scroll at 375 px.
  - **Sign-out:** cleared the token.
- Defects found and fixed during the run:
  1. a focus ring on `main` after programmatic focus;
  2. raw enum values in the rules view;
  3. **duplicate accessible names** ("Your answer") on both answer boxes;
  4. a stale notice carried to the next screen;
  5. the account header missing on deep links;
  6. compiled `.pyc` files accidentally committed (removed in `eeda20a`; `.gitignore` added).
- Automated: `tests/integration/test_web_ui.py` (5 tests); full suite 276 passed, 6 skipped.
- Status: PASS (software/browser verification; no screen-reader or real-user test)
- Performed by: Claude Code (Engineering)
