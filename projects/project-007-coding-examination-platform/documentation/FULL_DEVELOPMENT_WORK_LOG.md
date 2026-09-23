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
