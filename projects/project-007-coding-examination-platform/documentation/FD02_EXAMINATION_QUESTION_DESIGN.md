# FD-02 — Examination and Question Management Design

## Purpose
FD-02 introduces the first operational academic-content subsystem on top of FD-01 identity/RBAC. It covers examiner-owned examinations, reusable/versioned programming questions, and the ordered many-to-many relationship between examinations and questions.

## Why this model
A question is not embedded directly inside an examination because the same programming question may be reused or versioned independently. The junction entity `examination_questions` records membership, display order and score weight. This is a normalized relational design that avoids repeating question text for every examination.

## State model
Examinations use DRAFT → SCHEDULED → ACTIVE → CLOSED → ARCHIVED. State-transition enforcement will live in the application service, not in UI code.

## Figure 3.7.1 — ERD increment
**Figure 3.7.1 shows the current operational Entity-Relationship Diagram (ERD) after FD-02.**

```text
users
  PK user_id
     |1
     | owns/creates
     |----------------------.
     |                      |
     v                      v
examinations             questions
  PK examination_id        PK question_id
  FK owner_user_id         FK created_by_user_id
  title                    title
  description              prompt
  status                   language
  starts_at                max_score
  ends_at                  version
     |1                      |1
     |                       |
     '------< examination_questions >------'
               PK/FK examination_id
               PK/FK question_id
               display_order
               score_weight

users 1 ----< user_roles
users 1 ----< auth_sessions
```

*Figure 3.7.1: Entity-Relationship Diagram for Identity, Examination and Question Management.*

As shown in Figure 3.7.1, `examination_questions` resolves the many-to-many relationship between examinations and questions. Foreign keys preserve ownership and referential integrity, while the unique examination/display-order constraint prevents two questions occupying the same position.

## Implementation status
Domain objects and MySQL migration 002 are implemented in this increment. Repository/service/API behavior and MySQL integration tests remain to be implemented before FD-02 is complete.


## Figure 3.5.2 — Examination Lifecycle Activity Diagram
**Figure 3.5.2 shows how an examiner progresses an examination through its controlled lifecycle.**

```text
[Create Examination]
        |
        v
      DRAFT <----------------.
        |                     |
        | schedule            | return to draft
        v                     |
    SCHEDULED ----------------'
        |
        | activate
        v
      ACTIVE
        |
        | close
        v
      CLOSED
        |
        | archive
        v
     ARCHIVED
        |
       [End]
```

*Figure 3.5.2: Activity/state diagram for the controlled examination lifecycle.*

The application service, rather than the user interface, enforces these transitions. This prevents a client from bypassing lifecycle rules by calling persistence code directly. Question membership may be changed only while an examination remains in DRAFT.

## Figure 3.5.3 — Examiner Management Sequence
**Figure 3.5.3 shows the implemented interaction path for an authenticated examiner creating examination content.**

```text
Examiner       FastAPI/RBAC      ExamService       MySQL Repository       MySQL
   |                |                |                    |                  |
   | POST exam      |                |                    |                  |
   |--------------->| verify role    |                    |                  |
   |                |--------------->| validate domain    |                  |
   |                |                |------------------->| INSERT exam      |
   |                |                |                    |----------------->|
   |                |                |                    |<-----------------|
   |                |<---------------|                    |                  |
   |<---------------| 201 + exam id  |                    |                  |
```

*Figure 3.5.3: Sequence diagram for examiner examination creation.*

The same layered path is used for programming-question creation, question attachment and lifecycle transitions. Authorization is performed at the API boundary, business/lifecycle rules in the service, and SQL in the repository.

## Current FD-02 implementation boundary
Implemented: domain validation, MySQL repository, lifecycle/ownership service, MySQL schema migration and protected Examiner endpoints for creating examinations/questions, attaching questions and requesting state transitions.

Pending: API-level tests with dependency-isolated fakes, live MySQL integration evidence, list/read/update operations required by the final UI, and final rendered diagram assets. FD-02 is therefore still IN PROGRESS.


## Verification design — API boundary
The MySQL application factory now accepts explicit authentication and examination-service dependencies for tests. Production behavior is unchanged when these are omitted: the factory constructs the real MySQL-backed services. This dependency-injection seam lets API tests verify HTTP authorization and business-policy mapping without requiring a live MySQL Server.

The API test suite covers: Candidate rejection from Examiner operations (HTTP 403); Examiner creation of an examination and question; DRAFT question attachment; legal DRAFT→SCHEDULED transition; rejection of non-owner modification; illegal DRAFT→ACTIVE transition mapped to HTTP 409; and Administrator access at the role boundary.

Administrator role access is intentionally distinct from ownership. Passing the role check does not automatically make an Administrator the owner of an existing Examiner examination.

**Verification boundary:** these tests have been committed but are not recorded as passed until an actual test runner/CI execution confirms them.
