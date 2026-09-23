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
