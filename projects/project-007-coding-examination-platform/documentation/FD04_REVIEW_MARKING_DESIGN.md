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
```

*Figure 3.7.3: ERD increment for examiner marks.*

As Figure 3.7.3 shows, a mark belongs to a session and a question, not to a saved response. An unanswered question can therefore still be marked, typically with 0. `response_revision` records which saved revision the examiner read, so a reviewer can always tell which answer a mark refers to.

## Rules
- **Owner only.** Only the examiner who owns the examination can list its sessions, open a session review or mark. This matches the FD-02 ownership model.
- **Submitted only.** Marking requires a SUBMITTED session, whether submitted by the candidate or auto-submitted on close. In-progress content can still change.
- **Marking window.** Marking is open while the examination is ACTIVE (for sessions already submitted) or CLOSED. Once the examination is ARCHIVED, marks are frozen.
- **Bounds.** Each score must lie between 0 and the question's `max_score`. Comments are capped at 5,000 characters.
- **Re-marking** replaces the current mark and updates the marker and time.
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

The totals are **raw**: the sum of marked scores out of the sum of `max_score`. A weighted total is not computed, because FD-02's `score_weight` has no defined aggregation rule. Defining one is an open point.

## Verification status
- Service tests: `tests/unit/test_review_service.py`.
- API tests: `tests/integration/test_fd04_review_api.py`.
- SQL-contract tests: `tests/unit/test_mysql_review_repository.py`.
- Live: `tests/integration/test_mysql_fd04_live.py` passed on 2026-10-29 against MySQL 8.4.9 on a disposable local instance (TE-009).

FD-04 is **IMPLEMENTED / UNIT + API TESTED / LIVE VERIFIED** on that instance.

## Open points for AJ
1. **Weighted total.** How should `score_weight` combine with per-question scores? One candidate formula is Σ (score / max_score × weight). It is not implemented.
2. **Mark history.** Re-marking currently overwrites the previous mark. Should earlier marks be kept for audit?
3. **Release to candidates.** Candidates cannot see marks. Is a release step wanted, and when?
