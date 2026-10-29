# P001 Full Development Work Log

## 2026-09-23 — Full-development transition
**Decision:** transition from research-critical vertical-slice implementation to full software-product development while preserving the frozen research experiment.

**Method:** Agile iterative and incremental SDLC with explicit research/change-control gates. The project does not claim formal Scrum.

**Design work opened:** actor model; functional/non-functional requirements; use-case baseline; high-level architecture; candidate-examination activity flow; evidence-gap verification activity flow; logical ERD baseline; submission-to-verification sequence baseline.

**Implementation order:** authentication/RBAC -> operational examination/session/submission domain -> persistence/schema -> APIs -> lightweight UI -> integration/security/system testing -> deployment hardening.

**Documentation rule:** every material increment must update requirements, design/diagrams, RTM, tests/evidence, and this work log.

**Research boundary:** full product development is authorized, but external assessor evidence and frozen experimental definitions remain controlled. Product completeness must not be represented as scientific validation.


## 2026-09-23 — Increment FD-01: Identity, authentication and RBAC foundation
**Implemented:** operational User/Role model; four explicit roles (Candidate, Examiner, Administrator, Independent Assessor); PBKDF2-HMAC-SHA256 salted password hashing; opaque random bearer sessions with only SHA-256 token digests persisted; login/logout/current-user API; role guards; SQLite users, user_roles and auth_sessions schema; unit and integration tests.

**Security boundary:** plaintext passwords and raw bearer tokens are not stored. This is a development authentication foundation, not yet a production internet-facing identity service. Account recovery, rate limiting, CSRF/cookie policy, MFA and production secret/transport configuration remain future hardening work.

**Traceability:** full-product FR-01 is implemented for the current API foundation; FR-02 is partial because administrative user-management endpoints/UI are not yet implemented.

**Verification status:** tests were added, but no new CI result is claimed in this log until GitHub Actions executes the new main revision.


## 2026-09-23 — Database architecture correction and diagram baseline
**Developer environment decision:** MySQL Server is now the canonical operational DBMS and MySQL Workbench the local administration/modelling client. SQLite is retained only for legacy research/isolated test roles where appropriate.

**Completed:** database technology decision record; versioned MySQL migration 001 for FD-01 users/roles/sessions; Workbench setup guide; formal diagram register; system-design document synchronized with the database decision.

**Reasoning:** the target system is multi-user and relational, requiring transactions, referential integrity, indexes and concurrent client-server access. The selected toolchain also matches the developer's intended local environment.

**Verification boundary:** the SQL migration has been authored but is not recorded as executed on the developer's local MySQL instance. The Python application is not yet claimed to be MySQL-integrated. That requires the next adapter/configuration increment and MySQL-backed integration testing.


## 2026-09-23 — Increment FD-01B: MySQL application adapter
**Implemented in code:** environment-driven `MySQLSettings`; transactional `MySQLDatabase` connection adapter using `mysql-connector-python`; MySQL-specific identity repository using parameterized `%s` queries; MySQL-backed FastAPI construction entry point; unit tests for configuration; dependency declaration.

**Architecture reason:** the service/domain layer remains independent of SQL dialect while persistence adapters absorb DBMS-specific connection and parameter behavior. This avoids contaminating authentication/business logic with MySQL details and preserves the older SQLite research path.

**CI correction:** the P001 workflow previously ran on pushes to the historical implementation branch but not canonical `main`. It now also triggers for relevant pushes to `main`.

**Verification boundary:** unit/legacy tests can run in CI without a live MySQL service. A genuine MySQL integration test still requires a MySQL Server schema created from the migration and must be recorded separately. No claim is made yet that the developer's local Workbench/MySQL instance has passed application integration.


## 2026-09-23 — Academic figure integration correction
The earlier consolidated multi-diagram sheet is no longer treated as a final report figure. The design document now introduces and discusses individual figures in their proper analysis/design sections: Figure 3.3.1 Use Case Diagram, Figure 3.4.1 High-Level System Architecture, Figure 3.4.2 Component Diagram, and Figure 3.5.1 Candidate Examination Activity Diagram. Future figures will be inserted progressively as the corresponding components stabilize. Final numbering remains subject to Chapter Three reconciliation.


## 2026-09-23 — Increment FD-01C: executable local MySQL verification
**Added:** least-privilege Workbench bootstrap SQL; non-destructive Python connection/schema checker; opt-in live MySQL identity/authentication integration test; step-by-step Workbench/PowerShell verification guide.

**Security reasoning:** normal application credentials receive data-manipulation privileges (SELECT/INSERT/UPDATE/DELETE) but not schema-destructive CREATE/ALTER/DROP privileges. Schema changes remain explicit administrator/migration operations.

**Verification semantics:** (1) migration success verifies schema creation; (2) connection checker verifies Python-to-MySQL connectivity and required tables; (3) live integration test verifies create-user/login/authenticate/logout behavior against MySQL. These claims are intentionally separate.

**Current status:** implementation path is ready, but the live test is not marked passed until it is executed against an actual MySQL Server. Ordinary CI skips this test unless `P001_RUN_MYSQL_TESTS=1`.


## 2026-09-24 — FD-02 opened: Examination and Question Management
**Branch:** `p001-fd02-exam-question-management`.

**Designed and implemented in this slice:** Examination and ProgrammingQuestion domain objects with validation; examination lifecycle vocabulary; MySQL migration 002 for `examinations`, `questions`, and normalized junction table `examination_questions`; unit tests for domain invariants; dedicated FD-02 design document with Figure 3.7.1 ERD increment and explanatory text.

**Design reasoning:** questions are independent/versioned entities rather than duplicated inside examination rows. The junction table represents the many-to-many relationship and carries display order and score weight. Ownership is linked to the FD-01 user identity model.

**Not yet complete:** repository, service/state-transition policy, protected examiner APIs, live MySQL migration/integration evidence, and UI. No FD-02 completion claim is permitted until those are implemented and tested.

**Documentation synchronization:** the ERD has been expanded in the FD-02 design document at the same time as migration 002. The final rendered ERD will be regenerated from the stabilized physical schema rather than allowing a stale diagram to survive.


### FD-02 continuation — repository, lifecycle and protected API
**Implemented:** MySQLExaminationRepository; ExaminationService; explicit transition matrix; owner-only modification rule; DRAFT-only question attachment; protected Examiner endpoints for examination creation, programming-question creation, attachment and lifecycle transition.

**Design artifacts updated:** FD-02 now contains Figure 3.5.2 examination lifecycle activity/state diagram and Figure 3.5.3 examiner-management sequence diagram, each introduced, captioned and explained in its relevant design narrative.

**Important boundary:** authorization at the API layer and ownership/lifecycle policy at the service layer are intentionally separate. This is defense-in-depth and separation of concerns, not duplicate logic.

**Verification status:** unit tests exist for lifecycle/ownership rules. API and live-MySQL integration verification remain pending; no pass claim has been recorded.


### FD-02 verification increment — API authorization and policy mapping
Added a dependency-injection seam to the MySQL FastAPI factory so HTTP-layer tests can use deterministic fake authentication/repositories while production still defaults to real MySQL services. Added integration tests covering Candidate denial, Examiner happy path, ownership denial, illegal lifecycle conflict and Administrator role-boundary access.

Corrected role consistency: FD-01 defined the Examiner boundary as EXAMINER or ADMINISTRATOR; FD-02 management endpoints now preserve that role policy. Ownership remains a separate service-layer constraint.

No test-pass claim is made yet. The files exist; execution evidence is still required.


### FD-02 verification gate opened — Pull Request #19
Draft Pull Request #19 (`P001 FD-02: Examination and Question Management`) was opened against `main` specifically to trigger the repository's pull-request CI path before merge. At opening, the branch contained 15 commits and 10 changed files relative to main.

GitHub Actions run #293 (`P001 EGPCV Tests`) was triggered for head `7df05f2d...`. Initial observed state: QUEUED; no conclusion recorded yet. Therefore this log does not claim a pass or failure.

The PR is intentionally draft and remains unmerged while automated verification is pending. Live MySQL execution remains a separate verification boundary even if the ordinary test suite passes.


### FD-02 CI evidence — Run #294
GitHub Actions run #294 completed successfully for PR #19. Job `test` result: SUCCESS. Pytest summary from the job log: **152 passed, 1 skipped, 1 warning in 4.85s**.

The skipped test is consistent with the opt-in live-MySQL boundary: ordinary CI does not by itself establish successful execution against the user's local MySQL Server. The warning is a Starlette TestClient/httpx deprecation warning; GitHub Actions also emitted a Node.js action-runtime deprecation warning. Neither caused test failure, but both are retained as maintenance notes.

PR #19 was rechecked after CI and GitHub reported it mergeable. It remains draft/unmerged because FD-02 still requires final completion review and live-MySQL evidence before the subsystem is represented as fully verified.


### MySQL host/account consistency correction
During pre-live-MySQL review, the application default host (`127.0.0.1`) was compared with the bootstrap account host (`'p001_app'@'localhost'`). Because MySQL account identity includes the host component and host matching can differ between TCP loopback and localhost/socket behavior, the bootstrap was corrected to create/grant `'p001_app'@'127.0.0.1'`, matching `P001_DB_HOST`'s default exactly.

This is recorded as a pre-verification defect found and corrected, not as live-database evidence. The least-privilege application account still receives only SELECT/INSERT/UPDATE/DELETE; schema DDL remains outside normal application privileges.


### FD-02 live-MySQL verification path completed in code
The local Workbench guide now applies both migration 001 and migration 002 and correctly identifies the application account as `p001_app@127.0.0.1`. The non-destructive connection checker now requires all six current operational tables: `users`, `user_roles`, `auth_sessions`, `examinations`, `questions`, and `examination_questions`.

Added opt-in live test `test_mysql_fd02_live.py`. Against a configured MySQL Server it creates a unique Examiner identity, persists an examination and programming question, attaches the question to the DRAFT examination, reads the examination back, transitions DRAFT→SCHEDULED through the service, and confirms the persisted state.

This closes the implementation gap in the verification path but does not constitute live execution evidence. The test remains skipped in ordinary CI unless `P001_RUN_MYSQL_TESTS=1`.


## 2026-10-29 — FD-02 completion increment (Claude Code, Engineering)
**Branch:** `p001-fd02-exam-question-management` (PR #19, still draft).

**CI maintenance:** cleared both warnings recorded at run #294.
- `actions/checkout` v4 → v5 and `actions/setup-python` v5 → v6, the Node 24 runtimes.
- `httpx` replaced by `httpx2` (pydantic/httpx2, which Starlette 1.x's TestClient prefers and lists in its own `full` extra). Classification: dependency issue. Application code does not import httpx directly.

**Implemented:** list/read/update/detach operations named as pending in the FD-02 design: `GET /examiner/examinations`, `GET /examiner/examinations/{id}`, `PATCH /examiner/examinations/{id}`, `GET /examiner/questions`, `DELETE /examiner/examinations/{id}/questions/{question_id}`. Examination time windows can now be set through the API. HTTP error mapping is centralised.

**Defects found in review and corrected** (classification: application bug; none had been reported by CI because the tests did not exercise these paths):
1. A whitespace-only title passed Pydantic `min_length=1` but failed domain validation. The resulting `ValueError` surfaced as HTTP 500 and now returns 422.
2. Attaching the same question twice, or reusing a display order, raised MySQL `IntegrityError`, which surfaced as 500. It now returns 409 through a service pre-check, with repository translation of `IntegrityError` as the race backstop.
3. Lifecycle transitions were read-then-write, so two concurrent requests could both pass. The UPDATE is now compare-and-set on the expected status.
4. Attach, detach and detail edits are DRAFT-guarded in SQL as well as in the service.
5. mysql-connector does not set `CLIENT_FOUND_ROWS` by default. MySQL therefore reports 0 rows for an UPDATE that writes identical values, and a no-op PATCH would have returned a false 409. Connections now set the flag. The existing `revoke_session` update is unaffected because it always changes `revoked_at`.

**Policy decision (A2, logged for AJ):** DRAFT → SCHEDULED requires at least one attached question.

**Rejected alternative:** catching `IntegrityError` only in the API layer was rejected. It would leak a MySQL-specific exception type above the persistence boundary.

**Tests:** the duplicated fake repositories in the unit and API tests were replaced by one shared `tests/examination_fakes.py`. The fake follows the repository's guarded semantics. New service, API and SQL-contract tests were added, and the live MySQL test was extended to cover every new repository operation and guard.

**Local evidence:** Windows, Python 3.14.0, `python -m pytest -q -W error::DeprecationWarning` → **176 passed, 2 skipped**. The two skips are the opt-in live MySQL tests. CI evidence is recorded separately once the run completes.

**Not verified:** live MySQL execution. No MySQL Server was available in this environment.

### FD-02 CI evidence — Run #302
GitHub Actions run #302 (`P001 EGPCV Tests`, head `5493e02`) completed with SUCCESS. Pytest summary: **176 passed, 2 skipped in 5.03s**. The Starlette httpx and Node 20 deprecation warnings from run #294 no longer appear. One informational GitHub notice remains: `ubuntu-latest` is moving to Ubuntu 26. It does not affect results and needs no action now.

This is software verification only. The two skips are the opt-in live MySQL tests, so live-MySQL verification is still outstanding.


## 2026-10-29 — FD-03 opened: Candidate Assignment, Session and Response Capture (Claude Code, Engineering)
**Branch:** `p001-fd03-candidate-sessions`. It is stacked on `p001-fd02-exam-question-management` because FD-03 depends on FD-02's examination repository. Its draft PR targets the FD-02 branch so the diff shows only FD-03.

**Designed and implemented:**
- Migration 003 (`candidate_assignments`, `examination_sessions`, `submission_responses`).
- Domain module `app/domain/candidate_session.py`.
- `CandidateSessionService` with an injectable clock.
- `MySQLCandidateSessionRepository`.
- Examiner assignment endpoints and candidate list/start/view/save/submit endpoints.
- Design document `FD03_CANDIDATE_SESSION_DESIGN.md` with Figure 3.7.2 (ERD increment), Figure 3.5.4 (session state) and Figure 3.5.5 (save sequence).
- Workbench guide and schema-check script updated for migration 003.

**Design reasoning:**
- One session per assignment, with resume on repeated start, gives the NFR-06 no-duplicate guarantee.
- Revision-number compare-and-set on saves stops a stale browser tab from silently overwriting newer work.
- Save and submit statements carry `status='IN_PROGRESS'` predicates, so a save that races a submit cannot alter locked content.
- Submit is idempotent so a retried request after a network drop succeeds.

**Test defect found and corrected:** the first version of `test_racing_start_resumes_the_winner` patched the fake's session lookup globally. That also disabled the fake's unique-key check, so the test failed by creating a second session. Classification: test bug. The corrected test blinds only the service's first lookup and keeps the uniqueness check real.

**Policy decisions logged for AJ (A2):** one session per assignment; submission allowed after `ends_at`; no auto-finalisation at close; only the latest response content is stored.

**Verification status:** service, API and SQL-contract tests added. The opt-in live MySQL test was added but not executed. No FD-03 completion claim is made beyond IMPLEMENTED / UNIT + API TESTED.

### FD-01/FD-02 live MySQL evidence (2026-10-29)
**Environment:** MySQL Community Server **8.4.9**: a disposable local instance started from the MySQL 8.4 binaries installed on AJ's Windows PC (`--initialize-insecure`, scratch data directory, 127.0.0.1:3399, X Protocol off). This is **not** AJ's own configured server on port 3307, and that server was not touched. Setup followed `database/mysql/README.md`: bootstrap 000 with a one-off generated test password, then migrations 001–003 as root. Tests connected as the least-privilege `p001_app@127.0.0.1` account (SELECT/INSERT/UPDATE/DELETE only). Python 3.14.0, mysql-connector-python 9.x.

**Result at head `409d6c5`:**
- `python -m scripts.check_mysql_connection`: `P001 MySQL FD-02 schema check: PASS`.
- `P001_RUN_MYSQL_TESTS=1 python -m pytest tests/integration/test_mysql_identity_live.py tests/integration/test_mysql_fd02_live.py`: **2 passed in 8.86s**.

This exercised every FD-02 repository operation and SQL guard against a real server:
- empty-exam scheduling refused;
- duplicate attachment translated into a domain conflict;
- detach;
- identical-value re-save found (CLIENT_FOUND_ROWS);
- stale compare-and-set refused;
- post-DRAFT attach, detach and edit refused.

**Defect found by the live run:** the documented `python scripts/check_mysql_connection.py` crashed with `ModuleNotFoundError: No module named 'app'`. Running a file puts `scripts/` on `sys.path`, not the project root. Classification: command/documentation issue; the script itself was correct. The guide now uses `python -m scripts.check_mysql_connection`.

**Status:** FD-01 and FD-02 are LIVE VERIFIED against MySQL 8.4.9 on the disposable instance described above. A run on AJ's own configured server would be additional, user-environment evidence.

### FD-03 live MySQL evidence (2026-10-29)
**Environment:** same disposable instance as the FD-01/FD-02 entry. MySQL Community Server **8.4.9**: a disposable local instance started from the MySQL 8.4 binaries installed on AJ's Windows PC (`--initialize-insecure`, scratch data directory, 127.0.0.1:3399, X Protocol off). This is **not** AJ's own configured server on port 3307, and that server was not touched. Setup followed `database/mysql/README.md`: bootstrap 000 with a one-off generated test password, then migrations 001–003 as root. Tests connected as the least-privilege `p001_app@127.0.0.1` account (SELECT/INSERT/UPDATE/DELETE only). Python 3.14.0, mysql-connector-python 9.x.

**Result on branch `p001-fd03-candidate-sessions` at `c5780a3` (FD-03 plus the merged FD-02 fixes):**
- `python -m scripts.check_mysql_connection`: `P001 MySQL FD-03 schema check: PASS` (all nine tables).
- Entire P001 suite with `P001_RUN_MYSQL_TESTS=1` (unit, API, SQL-contract and all three live MySQL tests): **206 passed, 0 skipped in 99.75s**.

The FD-03 test covered:
- only CANDIDATE-role users assignable;
- duplicate assignment refused;
- start then resume of the same session;
- revisioned saves;
- stale revision refused by the SQL compare-and-set;
- idempotent submit;
- saves refused after submit;
- saved content read back.

**Status:** FD-03 is LIVE VERIFIED against MySQL 8.4.9 on that instance.

### FD-02 — DR-011 applied (2026-10-29)
AJ resolved the FD-02 policy points. The one change is that examiners may now attach only questions they created; another examiner's question returns 404. This is implemented with `question_created_by` in the repository and fake, and covered by service, API and live tests. The other points stay as built: scheduling requires a question, and the time window is optional.

### FD-02 live MySQL re-run after DR-011 (2026-10-29)
Environment: fresh disposable MySQL 8.4.9 instance (re-initialised after migration 003 changed), same setup as TE-005: bootstrap 000, migrations 001–003, least-privilege `p001_app`. Head `c757a96`, entire P001 suite with `P001_RUN_MYSQL_TESTS=1` and deprecations treated as errors: **180 passed, 0 skipped**. This included the live check that another examiner's question cannot be attached (TE-007).

### FD-03 — DR-011 applied: auto-submit on close (2026-10-29)
AJ approved auto-finalising open sessions when an examination closes.

**Implementation:**
- `MySQLExaminationRepository.update_status` runs a second UPDATE on the same connection whenever a CLOSED compare-and-set succeeds, so both changes commit or roll back together.
- That UPDATE (`examination_sessions JOIN candidate_assignments`) sets `status='SUBMITTED'`, `submitted_at=UTC_TIMESTAMP(6)` and `submission_mode='AUTO_ON_CLOSE'`.
- Candidate submissions now record `submission_mode='CANDIDATE'`.
- Migration 003 gained the nullable `submission_mode` column. It was amended in place because it had only been applied to the disposable test instance.
- The in-memory examination fake runs `on_close` callbacks to stand in for the same-transaction update.

**Rejected alternative:** finalising sessions from the service after the close commits. If the second step failed, sessions would be stuck IN_PROGRESS on a CLOSED examination, where they can no longer be saved or submitted.

**Tests:** service, API, SQL-contract (second statement only after a successful CLOSE; none on other transitions or a lost race) and live.

The other FD-03 points stay as built: one attempt, late submit allowed, latest content only (history parked as SP-001).

### FD-03 live MySQL re-run after DR-011 (2026-10-29)
Environment: fresh disposable MySQL 8.4.9 instance (re-initialised after migration 003 changed), same setup as TE-005: bootstrap 000, migrations 001–003, least-privilege `p001_app`. Head `dbbe8eb`.
- `python -m scripts.check_mysql_connection`: PASS.
- Entire P001 suite with `P001_RUN_MYSQL_TESTS=1`: **212 passed, 0 skipped**.

The live FD-03 test confirmed on a real server that closing the examination set the open session to SUBMITTED / `AUTO_ON_CLOSE` with its saved work intact, and left the already-submitted session's `CANDIDATE` mode and timestamp unchanged (TE-008).


## 2026-10-29 — FD-04 opened: Examiner Review and Per-Question Marking (Claude Code, Engineering)
**Branch:** `p001-fd04-review-marking`, from main at `2be8416`.

**Scope decision (AJ, 2026-10-29):** build review and marking, and defer EGPCV evidence registration (FR-08) until the Examination Capability Contract exists. Section 72 of the formal research specification requires observations to be interpreted under the ECC before they carry evidential meaning.

**Implemented:**
- Migration 004 (`response_marks`).
- `app/domain/review.py`, `ReviewService`, `MySQLReviewRepository`.
- Three examiner endpoints.
- Design document `FD04_REVIEW_MARKING_DESIGN.md` with Figure 3.7.3 (ERD increment) and Figure 3.5.6 (marking sequence).
- Schema check and Workbench guide updated for migration 004.

**Design reasoning:**
- A mark keys on (session, question) rather than on a saved response, so unanswered questions can be marked.
- `response_revision` preserves which answer was read.
- Marking is limited to SUBMITTED sessions so the marked answer cannot change afterwards.
- ARCHIVED freezes marks.
- The SQL upsert repeats the status guards so a concurrent archive cannot be followed by a stray mark.

**Rejected alternatives:**
- `INSERT ... ON DUPLICATE KEY UPDATE col=VALUES(col)`: `VALUES()` is deprecated in MySQL 8.x. A derived-table alias is used instead.
- A weighted total: no aggregation rule for `score_weight` is defined, so only raw totals are reported.

**Live evidence:** full suite with `P001_RUN_MYSQL_TESTS=1` at `f9f8331`, on a fresh disposable MySQL 8.4.9 instance with migrations 001–004: **227 passed, 0 skipped** (TE-009).

### FD-04 — DR-012 applied: weighted total, mark history, results release (2026-10-29)
AJ resolved FD-04's three open points; details are in DR-012.

**Implementation:**
- `weighted_percent` in `app/domain/review.py` uses `fractions.Fraction`, so the result is exact before a single rounding.
- `response_mark_history` receives a row in the same transaction as each successful upsert. The SQL-contract test checks that no history row is written when the guard refuses.
- `examination_result_releases` is checked by both the service and a `NOT EXISTS` predicate in the upsert, so a mark cannot slip in after a concurrent release.
- Release requires CLOSED/ARCHIVED and complete marking, and is idempotent.
- The candidate result endpoint hides the marker identity and history.

**Design choice:** the release record is a separate table rather than a column on `examinations`. This keeps FD-02's schema and domain object unchanged.

**Live evidence:** full suite at `cad0a95`, fresh disposable MySQL 8.4.9 instance, migrations 001–004: **235 passed, 0 skipped** (TE-010).


## 2026-10-29 — Examination Capability Contract v0.1 drafted (Claude Code, Engineering)
**Branch:** `p001-ecc-specification`. This branch is a specification only; no code.

At AJ's request, drafted `specification/EXAMINATION_CAPABILITY_CONTRACT_SPECIFICATION.md`. It formalises PASS_003 candidate C1, the PASS_004 C1 verdict and invariant, and PASS_005 supporting mechanism #1 with its invariants. It also fits the existing `EvidenceItem.policy_version`, `assistance_context` and `POLICY_CONTEXT` fields.

**Content:**
- capability schema;
- integrity modes;
- assistance construct;
- authorized exceptions;
- binding at DRAFT → SCHEDULED (proposed);
- non-retroactive versioning;
- evidence labelling;
- interpretation rules R1–R7;
- a JSON shape;
- increments FD-05/FD-06;
- open questions Q1–Q5.

**Deliberate limits:**
- no novelty claim;
- the ECC is declarative and labelled DECLARED, NOT ENFORCED until enforcement exists;
- it produces observation labels only, never verdicts.

**Status:** PROPOSED, awaiting AJ (DR-013, A3).

### ECC approved as v1.0 (2026-10-29)
AJ approved DR-013 (Option A) and answered Q1–Q5 with the proposed defaults. The spec is now **v1.0 APPROVED** and frozen, with no content change from v0.1 beyond recording the decisions. Next increment: FD-05 (ECC management).


## 2026-10-29 — FD-05: Examination Capability Contract management (Claude Code, Engineering)
**Branch:** `p001-fd05-ecc-management`, from main at `5f8a235`. Implements the approved ECC v1.0 (DR-013).

**Implemented:**
- Migration 005 (`capability_contracts`, `contract_exceptions`).
- Domain `app/domain/capability_contract.py`: schema validation, canonical hash, policy-version label.
- `ContractService` and `MySQLContractRepository`.
- Binding inside the DRAFT → SCHEDULED transaction.
- Six endpoints.
- Design document `FD05_CAPABILITY_CONTRACT_DESIGN.md` with Figure 3.7.4 (ERD) and Figure 3.5.7 (version lifecycle).
- Schema check and Workbench guide updated for migration 005.

**Effect on earlier increments:** scheduling now requires a contract (spec §5.2). The FD-02 to FD-04 live tests were updated to store a contract first. Pre-FD-05 unit and API tests keep scheduling freely, because their in-memory examination fake only models contracts when a contract fake is attached. This is documented in the fake.

**Implementation detail recorded (not a spec change):** the binder (`bound_by_user_id`) is inside the content hash, as spec §8 requires. Because only the owner can bind, it is known when the draft is saved, so the hash is fixed before binding and does not depend on `bound_at`.

**Known limitation:** exception extra time is recorded but not applied to FD-03 deadlines, and is labelled as such. This is an open point for AJ.

**Live evidence:** full suite at `e502488`, fresh disposable MySQL 8.4.9 instance, migrations 001–005: **256 passed, 0 skipped** (TE-011).
