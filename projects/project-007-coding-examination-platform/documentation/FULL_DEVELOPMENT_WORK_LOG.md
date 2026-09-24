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
