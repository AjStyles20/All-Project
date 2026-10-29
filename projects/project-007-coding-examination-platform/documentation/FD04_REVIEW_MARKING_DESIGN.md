# FD-04 — Examiner Review and Per-Question Marking Design

## Purpose
FD-04 lets the owning examiner review submitted examination sessions and record a human mark per question. It implements the operational part of baseline FR-12 (examiner review with evidence/provenance visibility). It also introduces a first, minimal form of the logical `AssessmentDecision` entity from `FULL_SYSTEM_ANALYSIS_AND_DESIGN.md` §9, in the shape of per-question marks.

### Explicitly out of scope
- **EGPCV evidence registration (FR-08).** Section 72 of `FORMAL_RESEARCH_EXPERIMENT_SPECIFICATION.md` requires observations to be interpreted under the Examination Capability Contract (ECC) before they carry evidential meaning. The ECC (FR-15 in the RTM) is not implemented, and the competence-claim model is unfrozen. AJ chose on 2026-10-29 to build review and marking first and leave the evidence bridge until the ECC exists.
- **Automatic scoring, competence verdicts and misconduct findings.** A mark is an examiner's judgment of an operational answer. It is not an EGPCV evidence state.

## Figure 3.7.3 — ERD increment
**Figure 3.7.3 shows the marking table added by FD-04.**

```text
examination_sessions 1 ----< response_marks >---- 1 questions
                               PK/FK session_id
                               PK/FK question_id
                               score (0..question.max_score)
                               comment
                               response_revision (NULL = unanswered)
                               FK marked_by_user_id ---- users
                               marked_at
                |
                '--- every save also appended to ---> response_mark_history (append-only)

examinations 1 ---- 0..1 examination_result_releases
                          PK/FK examination_id, FK released_by_user_id, released_at
```

*Figure 3.7.3: ERD increment for examiner marks, mark history and results release.*

As Figure 3.7.3 shows, a mark belongs to a session and a question, not to a saved response. An unanswered question can therefore still be marked, typically with 0. `response_revision` records which saved revision the examiner read, so a reviewer can always tell which answer a mark refers to.

## Rules
- **Owner only.** Only the examiner who owns the examination can list its sessions, open a session review or mark. This matches the FD-02 ownership model.
- **Submitted only.** Marking requires a SUBMITTED session, whether submitted by the candidate or auto-submitted on close. In-progress content can still change.
- **Marking window.** Marking is open while the examination is ACTIVE (for sessions already submitted) or CLOSED. Once the examination is ARCHIVED, marks are frozen.
- **Bounds.** Each score must lie between 0 and the question's `max_score`. Comments are capped at 5,000 characters.
- **Re-marking** replaces the current mark. The earlier mark stays in `response_mark_history`, which receives every save in the same transaction as the upsert (DR-012 (2)).
- **Release** (DR-012 (3)): the owner releases results once the examination is CLOSED (or ARCHIVED) and every session is SUBMITTED and fully marked. Release is idempotent and locks further marking. The SQL upsert also refuses once a release row exists.
- **Concurrency.** The upsert's SELECT only matches a SUBMITTED session of an ACTIVE or CLOSED examination. A concurrent archive therefore cannot be followed by a stray mark. The upsert uses a derived table instead of the deprecated `VALUES()` function.

## Figure 3.5.6 — Marking sequence
**Figure 3.5.6 shows the path of a mark and where each guard is applied.**

```text
Examiner     FastAPI/RBAC      ReviewService             MySQL Review Repo              MySQL
   | PUT mark    |                   |                           |                         |
   |------------>| EXAMINER/ADMIN    |                           |                         |
   |             |------------------>| owns exam? session        |                         |
   |             |                   | SUBMITTED? exam ACTIVE/   |                         |
   |             |                   | CLOSED? question in exam? |                         |
   |             |                   | 0 <= score <= max?        |                         |
   |             |                   |-------------------------->| INSERT ... SELECT       |
   |             |                   |                           | WHERE SUBMITTED AND     |
   |             |                   |                           | exam ACTIVE/CLOSED      |
   |             |                   |                           | ON DUPLICATE KEY UPDATE |
   |             |                   |                           |------------------------>|
   |<------------| 200 + mark        |<--------------------------| rowcount >= 1 ?         |
```

*Figure 3.5.6: Sequence diagram for recording an examiner mark.*

## API surface

| Method | Path | Purpose |
|---|---|---|
| GET | `/examiner/examinations/{id}/sessions` | sessions with candidate, status, submission mode, timestamps, marked/total questions and raw totals |
| GET | `/examiner/sessions/{session_id}` | full review: each question with prompt, max score, weight, saved response (content, revision, saved_at) and current mark |
| PUT | `/examiner/sessions/{session_id}/marks/{question_id}` | record or replace a mark (`score`, `comment`) |
| POST | `/examiner/examinations/{id}/release` | release results to candidates |
| GET | `/candidate/sessions/{session_id}/result` | the candidate's own released result: per-question score, max and comment, plus raw and weighted totals |

Totals are reported two ways:
- **Raw:** Σ score out of Σ `max_score`.
- **Weighted percentage** (DR-012 (1)): Σ(score ÷ max_score × weight) ÷ Σ(weight) × 100, rounded to 2 dp. It is null until every question in the session is marked, so a half-marked session is never shown as a low percentage.

## Verification status
- Service tests: `tests/unit/test_review_service.py`.
- API tests: `tests/integration/test_fd04_review_api.py`.
- SQL-contract tests: `tests/unit/test_mysql_review_repository.py`.
- Live: `tests/integration/test_mysql_fd04_live.py` passed on 2026-10-29 against MySQL 8.4.9 on a disposable local instance: TE-009 for marking, and TE-010 after DR-012 for history, release and weighted totals.

FD-04 is **IMPLEMENTED / UNIT + API TESTED / LIVE VERIFIED** on that instance.

## Policy decisions (DR-012, approved by AJ 2026-10-29)
1. Weighted percentage as defined above, reported with the raw total.
2. Every mark is kept in an append-only history.
3. Explicit release after close and complete marking. Release locks marking; candidates then see their own result.
