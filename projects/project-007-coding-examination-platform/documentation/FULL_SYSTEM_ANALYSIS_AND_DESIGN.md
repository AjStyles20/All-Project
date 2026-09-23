# P001 Full-System Analysis and Design Baseline

## Status
Initial full-development design baseline. It extends the existing research-critical EGPCV implementation into a complete examination platform without changing the frozen research experiment.

## 1. System purpose
The Intelligent Coding Examination Platform supports creation, delivery, submission, evidence-based review, targeted verification, and auditable assessment of programming examinations. The system must separate ordinary examination/product functions from the experimental EGPCV mechanism.

## 2. Primary actors
- **Candidate/Student**: authenticates, enters an assigned examination, reads questions, writes/submits code and permitted responses, receives permitted verification prompts, and completes the session.
- **Examiner/Lecturer**: creates examinations/questions, configures assessment rules, reviews submissions/evidence, initiates or supervises permitted verification, and records/finalizes assessment decisions.
- **Administrator**: manages users, roles, courses/examinations, system configuration, access control, audit access, and operational maintenance.
- **Independent Assessor (research role)**: uses the frozen assessor package and records independent judgments under the research protocol. This role is deliberately separated from normal lecturer marking.
- **System/EGPCV Engine**: evaluates admissible evidence states, detects bounded competence gaps, selects the minimum admissible verification probe, updates evidence state, applies stopping rules, and preserves an audit trail.

## 3. Initial functional requirements
FR-01 User authentication and role-based authorization.
FR-02 User/account administration.
FR-03 Examination creation, scheduling, activation, and closure.
FR-04 Programming-question creation and versioning.
FR-05 Candidate examination-session lifecycle.
FR-06 Code/text response capture with timestamps and submission state.
FR-07 Submission persistence and retrieval.
FR-08 Evidence extraction/registration through explicitly supported adapters.
FR-09 Competence-claim and evidence-state evaluation through the existing bounded EGPCV domain.
FR-10 Gap detection and minimum admissible probe selection.
FR-11 Verification-session execution and stopping.
FR-12 Examiner review with evidence/provenance visibility.
FR-13 Immutable/append-oriented audit events for research-critical decisions.
FR-14 Results/report export subject to authorization.
FR-15 Research-mode isolation so experimental runs cannot silently contaminate operational results.
FR-16 Administrative configuration and system health visibility.

## 4. Initial non-functional requirements
NFR-01 Security: least-privilege role-based access control, secure credential handling, input validation, protected research/admin endpoints.
NFR-02 Integrity: submissions, evidence records, verification events, and research observations must preserve provenance and timestamps.
NFR-03 Auditability: research-critical state transitions must be reconstructable.
NFR-04 Reproducibility: deterministic research fixtures and frozen experiment definitions remain versioned.
NFR-05 Performance: normal local demonstration workflows should remain usable on low-resource hardware; heavy external AI services must not be required for basic operation.
NFR-06 Reliability: interrupted requests must not silently duplicate or lose finalized submissions.
NFR-07 Maintainability: modular API/domain/persistence/research boundaries and automated tests.
NFR-08 Usability: candidate examination flow must minimize navigation and expose clear save/submission state.
NFR-09 Portability: documented local setup with minimal platform-specific assumptions.
NFR-10 Privacy: collect only data required for examination/research purposes and separate operational identities from blinded research identifiers where applicable.

## 5. Use-case model
```text
Candidate
  |-- Authenticate
  |-- View assigned examination
  |-- Start examination session
  |-- Read question
  |-- Write/save response
  |-- Submit response
  |-- Respond to authorized verification probe
  '-- Finish examination

Examiner
  |-- Authenticate
  |-- Manage examination/questions
  |-- Review submission/evidence
  |-- Review/authorize verification workflow
  |-- Record assessment decision
  '-- Export authorized report

Administrator
  |-- Manage users/roles
  |-- Manage system configuration
  |-- Inspect operational/audit status
  '-- Maintain examination availability

EGPCV Engine
  |-- Evaluate evidence
  |-- Detect evidence gap
  |-- Select minimum admissible probe
  |-- Update evidence state
  '-- Apply stop rule

Independent Assessor
  |-- Receive frozen blinded package
  |-- Record independent judgment
  '-- Lock/return research response
```

## 6. High-level architecture
```text
+---------------- Presentation / Client ----------------+
| Candidate UI | Examiner UI | Admin UI | Research UI  |
+-------------------------+-----------------------------+
                          |
                          v
+---------------- Application / API --------------------+
| Auth | Exams | Sessions | Submissions | Review | API |
+-------------------------+-----------------------------+
                          |
             +------------+-------------+
             v                          v
+------ Operational Domain ------+  +--- EGPCV Domain ---+
| users/exams/questions/sessions |  | evidence/gaps      |
| submissions/results            |  | probes/stop rules  |
+---------------+----------------+  +---------+-----------+
                |                             |
                +--------------+--------------+
                               v
+---------------------- Persistence ---------------------+
| relational data | append-only audit | research records|
+---------------------------+----------------------------+
                            |
                            v
+---------------- Infrastructure ------------------------+
| CI/tests | configuration | logging | export/adapters   |
+--------------------------------------------------------+
```

## 7. Core activity: candidate examination
```text
Login
  -> authorization check
  -> select assigned active examination
  -> start/resume session
  -> load question
  -> edit/save response
  -> [more questions?] -> load next question
  -> request final submission
  -> validate session/submission rules
  -> persist final submission
  -> lock according to examination policy
  -> confirmation
```

## 8. Core activity: evidence-gap verification
```text
Submission/evidence available
  -> register admissible evidence
  -> evaluate competence claim
  -> sufficient evidence? --yes--> record supported state -> stop
                      |
                      no
                      v
                 detect gap
                      |
          admissible probe exists?
             | no              | yes
             v                 v
        unresolved/stop   select minimum probe
                                |
                           collect response
                                |
                         evaluate new evidence
                                |
                         update evidence state
                                |
                         stop rule satisfied?
                         | no          | yes
                         +--iterate    +--> stop
```

## 9. Initial logical data model / ERD
Operational entities to add around the existing research persistence:
- User
- Role / UserRole
- Course (where required)
- Examination
- Question
- ExaminationQuestion
- CandidateAssignment
- ExaminationSession
- Submission
- SubmissionResponse
- EvidenceRecord
- CompetenceClaim
- EvidenceState
- VerificationRun
- VerificationProbe
- ProbeResponse
- AssessmentDecision
- AuditEvent
- ResearchRun / blinded assessor artifacts (kept logically separated)

Key relationships:
```text
User 1---* CandidateAssignment *---1 Examination
Examination 1---* ExaminationQuestion *---1 Question
CandidateAssignment 1---* ExaminationSession
ExaminationSession 1---* SubmissionResponse *---1 Question
SubmissionResponse 1---* EvidenceRecord
EvidenceRecord *---* CompetenceClaim
CompetenceClaim 1---* EvidenceState
ExaminationSession 1---* VerificationRun
VerificationRun 1---* ProbeResponse *---1 VerificationProbe
ExaminationSession 1---* AuditEvent
ExaminationSession 1---0..1 AssessmentDecision
```

This is a logical design baseline, not yet a claim that every table exists in the current database. Physical schema/migrations must be created incrementally and kept synchronized with the ERD.

## 10. Sequence baseline: submission to verification
```text
Candidate -> UI: submit response
UI -> API: final submission request
API -> Session service: validate active session
Session service -> Persistence: store/finalize response
API -> Evidence service: register admissible evidence
Evidence service -> EGPCV engine: evaluate claim state
EGPCV engine -> Gap detector: identify bounded gap
Gap detector -> Probe selector: request minimum admissible probe
Probe selector -> Audit trail: record selection rationale
API -> UI: present permitted probe
Candidate -> UI: answer probe
UI -> API: submit probe response
API -> EGPCV engine: evaluate/update state
EGPCV engine -> Audit trail: append transition
API -> Examiner UI: expose authorized review state
```

## 11. Design constraints
No cheating/authorship inference is introduced by this baseline. A gap in evidence is not proof of misconduct. Operational features must not weaken the frozen research semantics, silently reinterpret assessor labels, or turn constructed expectations into ground truth.

## 12. Next design increments
The next implementation increments are authentication/RBAC, operational examination/session/submission domain, database migrations, API endpoints, then a lightweight web interface. Each increment must update this design, the RTM, tests, and work log.


## 13. Implemented design increment FD-01 — Identity and access
The operational persistence layer now contains `users`, `user_roles`, and `auth_sessions`. Roles are Candidate, Examiner, Administrator, and Independent Assessor. Authentication uses salted PBKDF2-HMAC-SHA256 password hashes. Login creates an opaque random bearer token; only its SHA-256 digest is stored with expiry/revocation state.

The platform API now exposes `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`, and initial protected role-boundary endpoints used to verify RBAC behavior. This establishes the security boundary needed before examination-management endpoints are introduced.

### Identity ERD increment
```text
User 1---* UserRole
User 1---* AuthSession

User
- user_id PK
- username UNIQUE
- password_hash
- display_name
- is_active

UserRole
- user_id FK
- role
PK(user_id, role)

AuthSession
- session_id PK
- user_id FK
- token_hash UNIQUE
- created_at
- expires_at
- revoked_at
```

**Still designed, not yet implemented:** administrator account-management UI/API, account recovery, production-grade abuse controls, and the examination/question/session entities from Section 9.


## 14. Database technology decision — MySQL Server
The canonical operational DBMS for the full platform is **MySQL Server**. **MySQL Workbench** is the developer's graphical administration and modelling client. SQLite remains useful for the historical research prototype and isolated fast tests, but it is not the target operational database.

**Rationale:** the full platform is relational and multi-user; it requires referential integrity, transactions, indexes, concurrent connections, auditable relationships, and an independently inspectable server database. MySQL fits those requirements while matching the developer's local toolchain. PostgreSQL would also be technically suitable, but no current requirement justifies introducing a second DBMS toolchain. A document/NoSQL store is not selected as the primary database because the core entities have strong relational constraints.

The first versioned MySQL migration is `database/mysql/migrations/001_identity_rbac.sql`. It materializes the FD-01 identity/RBAC tables using InnoDB, foreign keys, indexes and MySQL-compatible types. This migration is a schema contract; MySQL-backed application integration must still be implemented and tested before being marked complete.

### Figure placement
The formal diagram register is maintained in `documentation/DIAGRAM_REGISTER.md`. The current design figure set covers: system architecture, use cases, candidate activity, login sequence, Level-0 DFD, ERD, component architecture, deployment and key domain classes. These figures are target-state analysis/design artifacts unless the RTM/work log marks the represented feature as implemented.


## 15. MySQL application adapter — implemented boundary
The full-product persistence path now has a MySQL-specific connection adapter and identity repository. Database settings are read from `P001_DB_HOST`, `P001_DB_PORT`, `P001_DB_NAME`, `P001_DB_USER`, and `P001_DB_PASSWORD`. Credentials are therefore deployment configuration rather than source code.

The architecture deliberately keeps SQL dialect details below the service layer:

```text
FastAPI routes
     |
AuthService                 <- business/application behavior
     |
MySQLUserRepository         <- persistence contract implementation
     |
MySQLDatabase               <- connection/transaction boundary
     |
MySQL Connector/Python
     |
MySQL Server <---------- MySQL Workbench
```

**Why an adapter/repository boundary?** MySQL and SQLite differ in connection APIs, placeholders, types and schema mechanics. Keeping those differences in persistence code lets the authentication service express the same domain operation regardless of DBMS. It also lets the historical research prototype remain reproducible without making SQLite the production architecture.

**Current limitation:** the MySQL adapter is implemented but not yet verified against the developer's local MySQL Server. The next verification step is a live MySQL integration test using migration 001; only then will the MySQL FD-01 persistence path be marked verified.
