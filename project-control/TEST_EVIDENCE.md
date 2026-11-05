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

### TE-016 — P001 web UI slice 2 browser verification
- Date: 2026-10-30
- Requirement(s): P001 FR-29, FR-30; FD-02 to FD-06 policies through the UI
- Test type: Live (browser) + automated
- Environment: built-in browser; uvicorn on 127.0.0.1:8001; fresh disposable MySQL 8.4.9 (migrations 001–006) and a temporary research store, seeded only with test accounts and a template case. Everything else was created through the UI's forms, submitted by script so its own handlers ran.
- Observed result:
  - **Refusals shown correctly:** scheduling with no questions; scheduling with no contract; `LIMITED` terminal without an allowlist; amendment without a reason; unknown template case; score above the maximum; release before marking finished.
  - **Lifecycle and rules:** contract defaulted to lab-controlled; locked on schedule; amendment created v2 and superseded v1.
  - **Student:** saw v2; opted in; autosaved; submitted.
  - **Marking:** re-mark kept 7 then 8 in history; result 8/10, 80%; release locked marking.
  - **Bridge:** copied one case labelled with v2; re-run reported `already recorded 1`.
  - **Withdrawal:** deleted the case and code link; the log kept only the code and counts.
  - **Injection:** a question with `<img onerror>` markup displayed as plain text, with 0 injected elements and no script run.
  - **Phone width:** no horizontal scroll at 375 px on the contract screen.
- Defect found and fixed: administrators had no way to learn question ids or exam ids (admin question list added; exam id shown to the examiner).
- Automated: full suite 278 passed, 6 skipped.
- Status: PASS (implementing agent's own run; no screen-reader, real-user or independent verification)
- Performed by: Claude Code (Engineering)

### TE-017 — P001 FD-07 user management, live and browser
- Date: 2026-11-02
- Requirement(s): baseline FR-02; DR-019
- Test type: Live + browser + full regression
- Environment: fresh disposable MySQL 8.4.9 (migrations 001–007, least-privilege `p001_app`); built-in browser; uvicorn on 127.0.0.1:8001.
- Observed result, live: full suite with `P001_RUN_MYSQL_TESTS=1` at `7a64cf3`: schema check PASS; **306 passed, 0 skipped**.
- Observed result, browser:
  - **First administrator:** created by the real script against that database.
  - **First sign-in:** the new user was held on the forced-change screen; the API returned 403 `PASSWORD_CHANGE_REQUIRED`; a password containing the username and a mismatched repeat were refused.
  - **Reset:** a live session went from 200 to 401 and the old one-time password was refused.
  - **Deactivate:** a live session went from 200 to 401 and login was refused; reactivation did not revive the old session.
  - **Self-deactivation:** refused.
  - **Lecturer:** assigned a candidate from the list; `/admin/users` returned 403.
  - **Administrator:** saw the exam list.
  - **CSP:** no refusals in the console.
- Test-script defect: a first reset check used a token already signed out, so its 401 proved nothing; it was redone with live sessions.
- Application defects found and fixed: validation errors displayed as "Request failed (422)" (`core.js`, changed after the live run and rechecked in the browser); a forced change on `#/home` could leave the user stuck on the form (found by code reading, fixed before the run).
- Status: PASS (implementing agent's own run; not independent verification or a security review)
- Performed by: Claude Code (Engineering)

### TE-018 — P001 FD-08 login protection and account audit trail, live and browser
- Date: 2026-11-03
- Requirement(s): PROJECT_RULES §22; DR-020
- Test type: Live + browser + API + full regression
- Environment: disposable MySQL 8.4.9 (migrations 001–008, least-privilege `p001_app`); built-in browser; uvicorn on 127.0.0.1:8001.
- Observed result, live: schema check PASS. Full suite with `P001_RUN_MYSQL_TESTS=1`: 329 passed at `705748d`; 333 passed at `051af00`; **334 passed, 0 skipped at `89a9487`** (final code).
- Observed result, browser and API:
  - **Sign-in form:** after the limit it shows "Too many failed sign-in attempts. Please try again later."
  - **Parallel burst** of 12 wrong passwords (unknown username): exactly 5 × 401, 7 × 429. Same for 8 and 10 attempts on real accounts.
  - **Clear sign-in lock** from the Users screen: the next wrong password got 401, not 429.
  - **Audit trail:** shows the lock and the clearing, names the administrator, and records no passwords.
- Application defects found and fixed:
  1. **Race (security):** on `705748d` a parallel burst passed the lock check while earlier attempts were still hashing, so more than five guesses got through and the correct password then signed in. The earlier tests missed it because they recorded failures one at a time. Fixed in `051af00`: each attempt is counted atomically before hashing. Regression tests use real threads, through the API and on live MySQL.
  2. **Duplicate audit records:** one lock caused by a burst was recorded five times. Fixed in `89a9487`: only the attempt that reaches the limit records it.
  3. **Audit screen** showed the administrator's internal id. Fixed in `89a9487`.
- Test-script defects: a burst against a username that turned out not to exist (still a valid check, since unknown names lock the same); one check hit an account already locked by an interrupted earlier script, and was repeated after clearing the lock. The final audit-screen check was made through the API because the browser pane was pointed at the wrong port.
- Status: PASS (implementing agent's own run; not independent verification or a security review)
- Performed by: Claude Code (Engineering)

### TE-019 — P007 School Points first version: tests, benchmark and browser
- Date: 2026-11-05
- Requirement(s): P007 Pass 004 (H5, §11–§16); DR-021
- Test type: Unit + API + benchmark evaluation + browser
- Environment: Python 3.14 locally (CI: 3.11); SQLite; built-in browser; uvicorn on 127.0.0.1:8011.
- Observed result, tests: 30 passed (ledger rules including parallel redemptions, each engine on each scenario, scoring, success rule, API, CSP).
- Observed result, benchmark: thresholds committed in `c174ed2` before the final run. Final seeds 1000–1019 at 30 students per group: B4 recall 1.00, false positives 0.05, unsupported claims 0.02, appropriate insufficiency 1.00; B3 0.57 / 0.30 / 0.41 / 0.00; B1 0.39 / 0.38 / 0.58 / 0.00. Composite rule met, also at 15 and 60 students per group.
- Observed result, browser: loaded S8 into an empty ledger; B4 showed the issuer disparity and proxy-gaming findings with observations, missing context and non-claims; no console errors.
- Threat to validity: the same agent wrote the scenario generator and B4, so the benchmark result is not evidence the audit works on unseen or real data (`docs/RESULTS.md`).
- Test defect found: one test matched the word "benchmark" in a docstring; replaced with an import check.
- Status: PASS for the software; the research result is NOT independently established.
- Performed by: Claude Code (Engineering)

### TE-020 — P009 Screen Memory first version: tests, simulation, Windows probes
- Date: 2026-11-05
- Requirement(s): P009 Pass 003 (H5 boundary); DR-021; `docs/PRIVACY_SECURITY_MODEL.md`
- Test type: Unit + API + offline simulation + Windows probe check
- Environment: Windows 10, Python 3.14 locally (CI: windows-latest, Python 3.11).
- Observed result, tests: 27 passed (exclusions, policies including no-future check, encryption on disk, retention and cap, deletion, path safety, recorder pause/lock/idle/exclusion, token and Host checks, simulation).
- Observed result, DPAPI: encrypt/decrypt round trip on this machine.
- Observed result, simulation (seeds 100–119, policies frozen in `fb03410`): B4 145 frames/hour, 12 sensitive frames, proxy 1.00; B3 415, 51, 1.00; B2 107, 15, 0.97. Predeclared rule met on the proxy. B2 keeps fewer images than B4.
- Observed result, Windows probes: run from the development session, Windows reported the desktop as locked and no foreground window; the recorder's lock check therefore captured nothing. **Live capture not verified.**
- Status: PASS for the tested software; live recording UNVERIFIED; research question NOT tested (needs people).
- Performed by: Claude Code (Engineering)

### TE-021 — P010 Chess first version: rules, arbiter, browser
- Date: 2026-11-05
- Requirement(s): P010 Pass 003 (H5); DR-021
- Test type: Unit + API + perft + benchmark evaluation + browser
- Environment: Python 3.14 locally (CI: 3.11); built-in browser; uvicorn on 127.0.0.1:8012.
- Observed result, rules: perft counts match published values for five reference positions (start position to depth 4 locally).
- Observed result, tests: 28 passed.
- Observed result, evaluation (frozen in `5df38dd`): B4 dev F1 1.00 and held-out F1 0.93 with no false penalties; best other method 0.75 dev, 0.45 held-out. Predeclared rule met. B4 misses 22 % of severe held-out cases (unlisted threat and insult phrasings).
- Observed result, browser: created a social game, White played e4 from the board, a spectator's "night to f six" got a high-confidence notice naming g8f6, the game was unchanged, ordinary chat got no notice.
- Defects found: a move-generator bug (iterating a list being mutated), found by the first perft run and fixed before commit; one test expectation was wrong (promotions there give mate); evidence wording "said during DURING" reworded after the evaluation (rulings unchanged).
- Status: PASS for the software; the research result is NOT independently established.
- Performed by: Claude Code (Engineering)

### TE-022 — P004 Compression Gateway first version: security invariants, benchmark, live gateway
- Date: 2026-11-05
- Requirement(s): P004 Pass 004; `docs/SPECIFICATION.md`; DR-021
- Test type: Unit + integration + benchmark + live servers
- Environment: Windows 10, Intel Atom/Celeron-class CPU, Python 3.14 (CI: Ubuntu, 3.11); origin and gateway on 127.0.0.1.
- Observed result, tests: 31 passed, covering security invariants S1–S10 for every transforming policy where relevant.
- Observed result, benchmark (frozen in `0970587`): regressions B1 181, B2 168, B3 147, B4 3; B4 kept 99 %/98 % of B3's savings on the slow profiles; B4 and B3 agreed on 42 % of decisions. All §9 thresholds met.
- Observed result, live: correct pass/gzip/abstain decisions; absolute-form target refused (400); upstream redirect returned, not followed.
- Defects found: cost-model fit distorted by tiny objects (fixed on pilot data before freezing); lab gateway started without its fitted model so B4 never transformed (fixed, regression test added); two wrong test expectations fixed. B4's verification cost (24–56 % of encode time) was not counted in the benchmark and makes large photos exceed the 5 s limit on this laptop — recorded, not fixed.
- Status: PASS for the software and the predeclared thresholds; the result relies on a modelled network and is NOT independently established.
- Performed by: Claude Code (Engineering)

### TE-023 — P006 Learning World first version: kernels, gates, browser
- Date: 2026-11-05
- Requirement(s): P006 (legacy P002) Pass 017 §14, Pass 018 truth tables E1–E8; DR-021
- Test type: Unit + API + evaluation + browser
- Environment: Python 3.14 locally (CI: 3.11); built-in browser; app on 127.0.0.1:8015 with a throwaway token.
- Observed result, tests: 29 passed, organised by the Pass 018 truth tables and experiments E1–E8.
- Observed result, evaluation (frozen in `e5a6d40`, seeds 100–149): artifact propagation precision/recall 1.00/1.00 (B2 recall 0), no laundering in 1,150 AI-descended claims, false invalidation 0; simulated false mastery 13.9 % (B3 19.4 %), missed mastery 10.0 % (B3 27.8 %), L6-only independent 0 % (B3 100 %).
- Observed result, browser: hint then correct answer gave "provisional" and moved to a check without help (no hint button); course view showed the superseded v1 claim and dependent lessons as STALE with reasons; no console errors.
- Defects found: paraphrase lower-cased "INNER" ("iNNER"); explanation listed the authority note before the reason that decided the status; one tautological test assertion; the production Host check briefly allowed the test client's host name — all fixed before commit.
- Status: PASS for the software and the automatic gates; the reference is a second implementation by the same agent, and learners are simulated.
- Performed by: Claude Code (Engineering)

### TE-024 — P011 Defence Practice first version: ingestion, findings, sessions, browser
- Date: 2026-11-05
- Requirement(s): P011 (legacy P001) FR-001–FR-006, NFR-001/003/004; DR-021
- Test type: Unit + API + evaluation + browser
- Environment: Python 3.14 locally (CI: 3.11); built-in browser; app on 127.0.0.1:8016 with a throwaway token.
- Observed result, tests: 13 passed (TXT/DOCX/PPTX/PDF extraction with locations; refused: wrong type, over 10 MB, broken zip, DTD/XXE, zip bomb; findings tied to real sentences; grounded questions; feedback criteria; token/Host; full flow; delete removes search results).
- Observed result, evaluation (frozen in `4796c67`): planted issues reached by 12 questions — dev wording B4 99 %, B1 20 %, B0 0 %; held-out wording B4 17 %, B1 15 %, B0 0 %. Quotes found in cited passages 100 %; no false alarms; role categories 97 % distinct.
- Observed result, browser: uploaded report gave one finding of each kind with document and paragraph; a session of grounded questions; an overconfident answer got relevance, evidence and absolute-wording feedback.
- Defects found: the first benchmark used reports too short to separate methods (random questions reached 100 %), fixed in the pilot before freezing; one wrong test expectation; XML guard tightened to the whole file after a security hook warning.
- Status: PASS for the software; the rule-based method does NOT generalise to new wording.
- Performed by: Claude Code (Engineering)
