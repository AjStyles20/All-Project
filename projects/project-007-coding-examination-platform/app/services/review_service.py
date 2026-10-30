"""FD-04 examiner review, per-question marking and results release."""
from dataclasses import dataclass

from app.domain.candidate_session import (
    CandidateAssignment, ExaminationSession, SavedResponse, SessionStatus,
)
from app.domain.examination import Examination, ExaminationQuestionEntry, ExaminationStatus
from app.domain.review import MarkingConflictError, ResponseMark, ResultRelease, weighted_percent
from app.services.candidate_session_service import SessionNotFoundError, utc_now
from app.services.examination_service import (
    ExaminationNotFoundError, ExaminationOwnershipError, QuestionNotFoundError,
)

MARKABLE_EXAM_STATUSES = {ExaminationStatus.ACTIVE, ExaminationStatus.CLOSED}
# Release needs the examination finished; ARCHIVED is allowed so an archived but
# unreleased examination is not stuck forever.
RELEASABLE_EXAM_STATUSES = {ExaminationStatus.CLOSED, ExaminationStatus.ARCHIVED}


@dataclass(frozen=True)
class SessionSummary:
    session: ExaminationSession
    assignment: CandidateAssignment
    marked_questions: int
    total_questions: int
    raw_score: int
    raw_max: int
    weighted_percent: float | None


@dataclass(frozen=True)
class SessionReview:
    session: ExaminationSession
    assignment: CandidateAssignment
    examination: Examination
    questions: list[ExaminationQuestionEntry]
    responses: dict[str, SavedResponse]
    marks: dict[str, ResponseMark]
    history: dict[str, list[ResponseMark]]
    release: ResultRelease | None


@dataclass(frozen=True)
class CandidateResult:
    session: ExaminationSession
    examination: Examination
    questions: list[ExaminationQuestionEntry]
    marks: dict[str, ResponseMark]
    raw_score: int
    raw_max: int
    weighted_percent: float | None
    release: ResultRelease


class ReviewService:
    def __init__(self, review_repository, session_repository, examination_repository, clock=utc_now):
        self.reviews = review_repository
        self.sessions = session_repository
        self.examinations = examination_repository
        self.clock = clock

    def list_sessions(self, examination_id: str, actor_user_id: str) -> list[SessionSummary]:
        self._owned_exam(examination_id, actor_user_id)
        entries = self.examinations.list_examination_questions(examination_id)
        raw_max = sum(entry.question.max_score for entry in entries)
        summaries = []
        for session, assignment in self.reviews.list_sessions_for_examination(examination_id):
            marks = {m.question_id: m for m in self.reviews.list_marks(session.session_id)}
            summaries.append(SessionSummary(session, assignment, len(marks), len(entries),
                                            sum(mark.score for mark in marks.values()), raw_max,
                                            weighted_percent(entries, marks)))
        return summaries

    def get_review(self, session_id: str, actor_user_id: str) -> SessionReview:
        session, assignment, exam = self._owned_session(session_id, actor_user_id)
        history: dict[str, list[ResponseMark]] = {}
        for mark in self.reviews.list_mark_history(session_id):
            history.setdefault(mark.question_id, []).append(mark)
        return SessionReview(
            session, assignment, exam,
            self.examinations.list_examination_questions(exam.examination_id),
            {r.question_id: r for r in self.sessions.list_responses(session_id)},
            {m.question_id: m for m in self.reviews.list_marks(session_id)},
            history,
            self.reviews.get_release(exam.examination_id),
        )

    def mark(self, session_id: str, question_id: str, actor_user_id: str,
             score: int, comment: str) -> ResponseMark:
        session, _, exam = self._owned_session(session_id, actor_user_id)
        if session.status is not SessionStatus.SUBMITTED:
            # In-progress content can still change, so a mark would not refer to a fixed answer.
            raise MarkingConflictError("Only submitted sessions can be marked.")
        if exam.status not in MARKABLE_EXAM_STATUSES:
            raise MarkingConflictError(f"Marking is closed for a {exam.status.value} examination.")
        if self.reviews.get_release(exam.examination_id) is not None:
            raise MarkingConflictError("Results have been released; marks are locked.")
        entry = next((e for e in self.examinations.list_examination_questions(exam.examination_id)
                      if e.question.question_id == question_id), None)
        if entry is None:
            raise QuestionNotFoundError("Question is not part of this examination.")
        response = self.sessions.get_response(session_id, question_id)
        mark = ResponseMark(session_id, question_id, score, comment,
                            response.revision if response else None, actor_user_id, self.clock())
        mark.validate(entry.question.max_score)
        if not self.reviews.save_mark(mark):
            raise MarkingConflictError("Session or examination changed state; reload before marking.")
        return mark

    def release_results(self, examination_id: str, actor_user_id: str) -> ResultRelease:
        exam = self._owned_exam(examination_id, actor_user_id)
        existing = self.reviews.get_release(examination_id)
        if existing is not None:
            return existing  # idempotent: a retried release returns the original record
        if exam.status not in RELEASABLE_EXAM_STATUSES:
            raise MarkingConflictError("Results can be released only after the examination is CLOSED.")
        incomplete = [s for s in self.list_sessions(examination_id, actor_user_id)
                      if s.session.status is not SessionStatus.SUBMITTED
                      or s.marked_questions < s.total_questions]
        if incomplete:
            # Never release a partial set: every session must be fully marked first.
            raise MarkingConflictError(f"{len(incomplete)} session(s) are not fully marked.")
        release = ResultRelease(examination_id, actor_user_id, self.clock())
        if not self.reviews.create_release(release):
            return self.reviews.get_release(examination_id)
        return release

    def candidate_result(self, session_id: str, candidate_user_id: str) -> CandidateResult:
        session = self.sessions.get_session(session_id)
        assignment = None if session is None else self.sessions.get_assignment_by_id(session.assignment_id)
        if assignment is None or assignment.candidate_user_id != candidate_user_id:
            raise SessionNotFoundError("Session not found.")
        release = self.reviews.get_release(assignment.examination_id)
        if release is None:
            raise MarkingConflictError("Results have not been released yet.")
        exam = self.examinations.get_examination(assignment.examination_id)
        entries = self.examinations.list_examination_questions(exam.examination_id)
        marks = {m.question_id: m for m in self.reviews.list_marks(session_id)}
        return CandidateResult(session, exam, entries, marks,
                               sum(m.score for m in marks.values()),
                               sum(e.question.max_score for e in entries),
                               weighted_percent(entries, marks), release)

    def _owned_exam(self, examination_id: str, actor_user_id: str) -> Examination:
        exam = self.examinations.get_examination(examination_id)
        if exam is None:
            raise ExaminationNotFoundError(examination_id)
        if exam.owner_user_id != actor_user_id:
            raise ExaminationOwnershipError("Only the owning examiner may review this examination.")
        return exam

    def _owned_session(self, session_id: str, actor_user_id: str):
        session = self.sessions.get_session(session_id)
        assignment = None if session is None else self.sessions.get_assignment_by_id(session.assignment_id)
        if assignment is None:
            raise SessionNotFoundError("Session not found.")
        exam = self._owned_exam(assignment.examination_id, actor_user_id)
        return session, assignment, exam
