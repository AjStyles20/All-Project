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
