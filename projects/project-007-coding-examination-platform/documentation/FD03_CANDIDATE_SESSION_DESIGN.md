# FD-03 — Candidate Assignment, Examination Session and Response Capture Design

## Purpose
FD-03 adds the candidate side of the examination workflow on top of FD-01 (identity/RBAC) and FD-02 (examinations/questions). It covers baseline requirements FR-05 (candidate examination-session lifecycle), FR-06 (code/text response capture with timestamps and submission state) and FR-07 (submission persistence and retrieval) from `FULL_SYSTEM_ANALYSIS_AND_DESIGN.md`.

It implements the `CandidateAssignment`, `ExaminationSession` and `SubmissionResponse` entities from the logical data model in section 9 of that document. Evidence registration, EGPCV verification and examiner review of submissions are **out of scope** for FD-03.

## Figure 3.7.2 — ERD increment
**Figure 3.7.2 shows the operational entities added by FD-03 and how they attach to FD-01/FD-02.**

```text
users 1 ----< candidate_assignments >---- 1 examinations
  (candidate_user_id, assigned_by_user_id)     |
                    |1                          | 1
                    |                           |
                    1                           |
          examination_sessions                  |
            PK session_id                       |
            FK assignment_id (UNIQUE)           |
            status IN_PROGRESS|SUBMITTED        |
            started_at, submitted_at            |
                    |1                          |
                    |                           |
                    '----< submission_responses >---- 1 questions
                            PK/FK session_id
                            PK/FK question_id
                            content, revision, saved_at
```

*Figure 3.7.2: ERD increment for candidate assignment, examination sessions and saved responses.*

As Figure 3.7.2 shows, a candidate is linked to an examination through `candidate_assignments`. `uq_assignment_exam_candidate` prevents duplicate assignment. Each assignment has at most one session (`uq_session_assignment`). Each session holds at most one current response per question; the primary key is (`session_id`, `question_id`), and a `revision` counter records how many times the response has been saved.

### Deliberate narrowing of the logical model
The logical baseline allows `CandidateAssignment 1---* ExaminationSession`. FD-03 enforces **one session per assignment**, and a repeated start resumes that session. This meets NFR-06 ("interrupted requests must not silently duplicate or lose finalized submissions") without inventing a multi-attempt policy that no requirement defines. Multiple attempts would require relaxing `uq_session_assignment` and an explicit attempt policy. AJ approved this in DR-011 (4).

Only the latest content of each response is stored, not every revision. A full revision history may matter for later evidence and process capture (EGPCV process evidence). It is deferred rather than assumed and parked as SP-001 (DR-011 (7)).

## Figure 3.5.4 — Candidate session state diagram
**Figure 3.5.4 shows the session lifecycle and the examination conditions that gate each step.**

```text
            [assigned]
                |
                | start (exam ACTIVE, inside starts_at..ends_at)
                v
           IN_PROGRESS  <--- start again = resume same session
                |   \
                |    \ save response (exam ACTIVE, before ends_at,
                |     \  question in exam, revision matches)
                |      '--> IN_PROGRESS (revision + 1)
                |
                | submit (exam ACTIVE; allowed after ends_at)   -> mode CANDIDATE
                | or examiner closes exam (same transaction)   -> mode AUTO_ON_CLOSE
                v
            SUBMITTED  --- submit again = same result (idempotent)
                |
              [locked: no further saves]
```

*Figure 3.5.4: Candidate examination-session state diagram.*

The service, not the client, enforces every transition in Figure 3.5.4. Submitting after `ends_at` is allowed because it only locks content that was saved before the deadline. New saves are already refused once the window has ended. When the examiner closes the examination, every session still IN_PROGRESS is finalised in the same transaction as the status change. These sessions are recorded with `submission_mode = AUTO_ON_CLOSE`, as distinct from `CANDIDATE` (DR-011 (6)), so saved work is never left unsubmitted and reviewers can tell the two cases apart. A candidate's retried submit after close returns the finalised session.

## Figure 3.5.5 — Save-response sequence
**Figure 3.5.5 shows how a save travels through the layers and where each guard is applied.**

```text
Candidate     FastAPI/RBAC        SessionService           MySQL Repository          MySQL
   |  PUT response  |                   |                          |                    |
   |--------------->| CANDIDATE role    |                          |                    |
   |                |------------------>| own session? IN_PROGRESS?|                    |
   |                |                   | exam ACTIVE + in window? |                    |
   |                |                   | question in exam?        |                    |
   |                |                   | base_revision current?   |                    |
   |                |                   |------------------------->| UPDATE ... WHERE   |
   |                |                   |                          | revision=prev AND  |
   |                |                   |                          | session IN_PROGRESS|
   |                |                   |                          |------------------->|
   |                |                   |<-------------------------| rowcount == 1 ?    |
   |<---------------| 200 + revision    |                          |                    |
```

*Figure 3.5.5: Sequence diagram for saving a candidate response.*

The service checks give clear error messages. The SQL predicates are what make the result correct when requests run concurrently. A save that races a submit, or a stale browser tab, changes nothing and returns 409.

## API surface

| Method | Path | Role | Purpose |
|---|---|---|---|
| POST | `/examiner/examinations/{id}/assignments` | Examiner/Admin (owner) | assign a candidate (`candidate_user_id`) |
| GET | `/examiner/examinations/{id}/assignments` | Examiner/Admin (owner) | list assignments |
| GET | `/candidate/examinations` | Candidate | own assigned examinations (schedule metadata only) |
| POST | `/candidate/examinations/{id}/session` | Candidate | start or resume the session |
| GET | `/candidate/sessions/{session_id}` | Candidate (own) | questions plus own saved responses |
| PUT | `/candidate/sessions/{session_id}/responses/{question_id}` | Candidate (own) | save response (`content`, optional `base_revision`) |
| POST | `/candidate/sessions/{session_id}/submit` | Candidate (own) | finalise (idempotent) |

Privacy and leakage choices:
- Another candidate's session and an unassigned examination both return **404, not 403**, so identifiers cannot be probed.
- Candidates are not shown `max_score` or `score_weight`.
- Questions are shown only through a session, which can only start while the examination is ACTIVE.

## Policy summary
- Assignment: owner only, target must be an **active user holding the CANDIDATE role**, not allowed for CLOSED/ARCHIVED examinations, one assignment per candidate per examination.
- Responses: capped at `MAX_RESPONSE_CHARS` = 100,000 characters (a resource limit, PROJECT_RULES §22), checked in both the API schema and the domain.
- Times: naive UTC, as in FD-02.

## Verification status
- Service tests (`tests/unit/test_candidate_session_service.py`) use an injectable clock for window and deadline cases.
- API tests (`tests/integration/test_fd03_candidate_api.py`) cover the full flow, role boundaries, 404 isolation and validation.
- SQL-contract tests (`tests/unit/test_mysql_candidate_session_repository.py`) pin the IN_PROGRESS predicates, the revision compare-and-set and the conflict translation.
- `tests/integration/test_mysql_fd03_live.py` is opt-in. It was **executed and passed on 2026-10-29** against MySQL 8.4.9 on a disposable local instance (see the work log).

FD-03 is therefore **LIVE VERIFIED** on that instance.

## Policy decisions (DR-011, approved by AJ 2026-10-29)
1. One session per assignment, with no re-attempts. Kept.
2. Submission permitted after `ends_at`. It locks only earlier saves. Kept.
3. Open sessions are auto-submitted when the examination closes (`AUTO_ON_CLOSE`). Implemented.
4. Only the latest response content is stored; revision history is parked as SP-001.
