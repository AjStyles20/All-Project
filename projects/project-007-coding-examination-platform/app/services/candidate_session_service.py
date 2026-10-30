"""FD-03 candidate assignment, examination-session and response policy."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from app.domain.candidate_session import (
    CandidateAssignment, ExaminationSession, SavedResponse, SessionConflictError, SessionStatus,
)
from app.domain.examination import Examination, ExaminationQuestionEntry, ExaminationStatus
from app.services.examination_service import (
    ExaminationNotFoundError, ExaminationOwnershipError, QuestionNotFoundError,
)


class AssignmentNotFoundError(LookupError):
    pass


class CandidateNotFoundError(LookupError):
    pass


class SessionNotFoundError(LookupError):
    pass


CLOSED_TO_ASSIGNMENT = {ExaminationStatus.CLOSED, ExaminationStatus.ARCHIVED}


def utc_now() -> datetime:
    # Stored times are naive UTC (see FD-02 time values), so "now" is too.
    return datetime.now(timezone.utc).replace(tzinfo=None)


@dataclass(frozen=True)
class SessionView:
    session: ExaminationSession
    examination: Examination
    questions: list[ExaminationQuestionEntry]
    responses: dict[str, SavedResponse]
    # This candidate's deadline: the examination's ends_at plus any granted extra time.
    effective_ends_at: datetime | None = None


class CandidateSessionService:
    def __init__(self, repository, examination_repository, clock=utc_now, contract_repository=None):
        self.repository = repository
        self.examinations = examination_repository
        self.clock = clock
        # Optional: FD-05 exceptions can extend a candidate's deadline. Without it, the
        # examination's own window applies to everyone.
        self.contracts = contract_repository

    # Examiner side

    def assign_candidate(self, examination_id: str, candidate_user_id: str,
                         actor_user_id: str) -> CandidateAssignment:
        exam = self._owned_exam(examination_id, actor_user_id)
        if exam.status in CLOSED_TO_ASSIGNMENT:
            raise SessionConflictError(f"Cannot assign candidates to a {exam.status.value} examination.")
        if not self.repository.is_candidate(candidate_user_id):
            raise CandidateNotFoundError("No active candidate with that user id.")
        if self.repository.get_assignment(examination_id, candidate_user_id) is not None:
            raise SessionConflictError("Candidate is already assigned to this examination.")
        assignment = CandidateAssignment(str(uuid4()), examination_id, candidate_user_id, actor_user_id)
        self.repository.create_assignment(assignment)
        return assignment

    def list_assignments(self, examination_id: str, actor_user_id: str) -> list[CandidateAssignment]:
        self._owned_exam(examination_id, actor_user_id)
        return self.repository.list_assignments_for_examination(examination_id)

    # Candidate side

    def list_candidate_examinations(self, candidate_user_id: str) -> list[tuple[CandidateAssignment, Examination]]:
        pairs = []
        for assignment in self.repository.list_assignments_for_candidate(candidate_user_id):
            exam = self.examinations.get_examination(assignment.examination_id)
            if exam is not None:
                pairs.append((assignment, exam))
        return pairs

    def start_session(self, examination_id: str, candidate_user_id: str) -> ExaminationSession:
        assignment = self.repository.get_assignment(examination_id, candidate_user_id)
        if assignment is None:
            # Same answer whether the examination exists or not, so ids cannot be probed.
            raise AssignmentNotFoundError("No assignment for this examination.")
        self._require_open_for_work(self.examinations.get_examination(examination_id), candidate_user_id)

        existing = self.repository.get_session_for_assignment(assignment.assignment_id)
        if existing is not None:
            return existing
        session = ExaminationSession(str(uuid4()), assignment.assignment_id,
                                     SessionStatus.IN_PROGRESS, self.clock())
        try:
            self.repository.create_session(session)
        except SessionConflictError:
            # A concurrent start won the unique key; resume that session instead.
            return self.repository.get_session_for_assignment(assignment.assignment_id)
        return session

    def find_session(self, examination_id: str, candidate_user_id: str) -> ExaminationSession | None:
        """Read-only lookup of the candidate's session, without starting one (UI results view)."""
        assignment = self.repository.get_assignment(examination_id, candidate_user_id)
        if assignment is None:
            raise AssignmentNotFoundError("No assignment for this examination.")
        return self.repository.get_session_for_assignment(assignment.assignment_id)

    def get_session_view(self, session_id: str, candidate_user_id: str) -> SessionView:
        session, assignment = self._owned_session(session_id, candidate_user_id)
        exam = self.examinations.get_examination(assignment.examination_id)
        entries = self.examinations.list_examination_questions(exam.examination_id)
        responses = {r.question_id: r for r in self.repository.list_responses(session_id)}
        return SessionView(session, exam, entries, responses,
                           self.effective_ends_at(exam, assignment.candidate_user_id))

    def save_response(self, session_id: str, question_id: str, candidate_user_id: str,
                      content: str, base_revision: int | None = None) -> SavedResponse:
        session, assignment = self._owned_session(session_id, candidate_user_id)
        if session.status is not SessionStatus.IN_PROGRESS:
            raise SessionConflictError("Session has been submitted; responses are locked.")
        exam = self.examinations.get_examination(assignment.examination_id)
        self._require_open_for_work(exam, candidate_user_id)
        entries = self.examinations.list_examination_questions(exam.examination_id)
        if question_id not in {entry.question.question_id for entry in entries}:
            raise QuestionNotFoundError("Question is not part of this examination.")

        existing = self.repository.get_response(session_id, question_id)
        previous = existing.revision if existing else 0
        # base_revision lets a client detect that another tab saved newer content.
        if base_revision is not None and base_revision != previous:
            raise SessionConflictError("A newer save exists for this question; reload before saving.")
        response = SavedResponse(session_id, question_id, content, previous + 1, self.clock())
        response.validate()
        if not self.repository.save_response(response, previous_revision=previous):
            raise SessionConflictError("Response changed or session was submitted concurrently; reload.")
        return response

    def submit(self, session_id: str, candidate_user_id: str) -> ExaminationSession:
        session, assignment = self._owned_session(session_id, candidate_user_id)
        if session.status is SessionStatus.SUBMITTED:
            # Idempotent: a retried submit must not fail or create a second submission.
            return session
        exam = self.examinations.get_examination(assignment.examination_id)
        if exam.status is not ExaminationStatus.ACTIVE:
            raise SessionConflictError("Examination is not ACTIVE; submission is closed.")
        # Submitting after ends_at is allowed: it only locks content saved before the
        # deadline, because save_response already refuses new content after it.
        if not self.repository.mark_submitted(session_id, self.clock()):
            current = self.repository.get_session(session_id)
            if current is not None and current.status is SessionStatus.SUBMITTED:
                return current
            raise SessionConflictError("Session could not be submitted; reload and retry.")
        return self.repository.get_session(session_id)

    # Shared checks

    def _owned_exam(self, examination_id: str, actor_user_id: str) -> Examination:
        exam = self.examinations.get_examination(examination_id)
        if exam is None:
            raise ExaminationNotFoundError(examination_id)
        if exam.owner_user_id != actor_user_id:
            raise ExaminationOwnershipError("Only the owning examiner may manage this examination.")
        return exam

    def _owned_session(self, session_id: str, candidate_user_id: str):
        session = self.repository.get_session(session_id)
        assignment = None if session is None else self.repository.get_assignment_by_id(session.assignment_id)
        if assignment is None or assignment.candidate_user_id != candidate_user_id:
            # Another candidate's session is reported as missing, not forbidden.
            raise SessionNotFoundError("Session not found.")
        return session, assignment

    def effective_ends_at(self, exam: Examination, candidate_user_id: str) -> datetime | None:
        """ends_at plus the largest extra time granted to this candidate (FD-05 exceptions).

        The largest single grant applies rather than the sum, so re-recording an
        exception never silently stacks time; an examiner who wants more grants more.
        """
        if exam.ends_at is None or self.contracts is None:
            return exam.ends_at
        extra = max((e.extra_time_minutes for e in
                     self.contracts.list_exceptions(exam.examination_id, candidate_user_id)), default=0)
        return exam.ends_at + timedelta(minutes=extra)

    def _require_open_for_work(self, exam: Examination | None, candidate_user_id: str) -> None:
        if exam is None or exam.status is not ExaminationStatus.ACTIVE:
            raise SessionConflictError("Examination is not open.")
        now = self.clock()
        if exam.starts_at and now < exam.starts_at:
            raise SessionConflictError("Examination has not started yet.")
        deadline = self.effective_ends_at(exam, candidate_user_id)
        if deadline and now >= deadline:
            raise SessionConflictError("Examination time window has ended.")
