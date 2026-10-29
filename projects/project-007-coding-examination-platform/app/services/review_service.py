"""FD-04 examiner review of submitted sessions and per-question marking."""
from dataclasses import dataclass

from app.domain.candidate_session import (
    CandidateAssignment, ExaminationSession, SavedResponse, SessionStatus,
)
from app.domain.examination import Examination, ExaminationQuestionEntry, ExaminationStatus
from app.domain.review import MarkingConflictError, ResponseMark
from app.services.candidate_session_service import SessionNotFoundError, utc_now
from app.services.examination_service import (
    ExaminationNotFoundError, ExaminationOwnershipError, QuestionNotFoundError,
)

MARKABLE_EXAM_STATUSES = {ExaminationStatus.ACTIVE, ExaminationStatus.CLOSED}


@dataclass(frozen=True)
class SessionSummary:
    session: ExaminationSession
    assignment: CandidateAssignment
    marked_questions: int
    total_questions: int
    raw_score: int
    raw_max: int


@dataclass(frozen=True)
class SessionReview:
    session: ExaminationSession
    assignment: CandidateAssignment
    examination: Examination
    questions: list[ExaminationQuestionEntry]
    responses: dict[str, SavedResponse]
    marks: dict[str, ResponseMark]


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
            marks = self.reviews.list_marks(session.session_id)
            summaries.append(SessionSummary(session, assignment, len(marks), len(entries),
                                            sum(mark.score for mark in marks), raw_max))
        return summaries

    def get_review(self, session_id: str, actor_user_id: str) -> SessionReview:
        session, assignment, exam = self._owned_session(session_id, actor_user_id)
        return SessionReview(
            session, assignment, exam,
            self.examinations.list_examination_questions(exam.examination_id),
            {r.question_id: r for r in self.sessions.list_responses(session_id)},
            {m.question_id: m for m in self.reviews.list_marks(session_id)},
        )

    def mark(self, session_id: str, question_id: str, actor_user_id: str,
             score: int, comment: str) -> ResponseMark:
        session, _, exam = self._owned_session(session_id, actor_user_id)
        if session.status is not SessionStatus.SUBMITTED:
            # In-progress content can still change, so a mark would not refer to a fixed answer.
            raise MarkingConflictError("Only submitted sessions can be marked.")
        if exam.status not in MARKABLE_EXAM_STATUSES:
            raise MarkingConflictError(f"Marking is closed for a {exam.status.value} examination.")
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
