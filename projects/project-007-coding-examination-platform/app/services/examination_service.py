"""FD-02 examination lifecycle and ownership policy."""
from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion


class ExaminationNotFoundError(LookupError):
    pass


class ExaminationOwnershipError(PermissionError):
    pass


class InvalidExaminationTransition(ValueError):
    pass


ALLOWED_TRANSITIONS = {
    ExaminationStatus.DRAFT: {ExaminationStatus.SCHEDULED},
    ExaminationStatus.SCHEDULED: {ExaminationStatus.ACTIVE, ExaminationStatus.DRAFT},
    ExaminationStatus.ACTIVE: {ExaminationStatus.CLOSED},
    ExaminationStatus.CLOSED: {ExaminationStatus.ARCHIVED},
    ExaminationStatus.ARCHIVED: set(),
}


class ExaminationService:
    def __init__(self, repository):
        self.repository = repository

    def create_examination(self, exam: Examination) -> Examination:
        exam.validate()
        self.repository.create_examination(exam)
        return exam

    def create_question(self, question: ProgrammingQuestion, creator_user_id: str) -> ProgrammingQuestion:
        question.validate()
        self.repository.create_question(question, creator_user_id)
        return question

    def attach_question(self, examination_id: str, question_id: str, actor_user_id: str,
                        display_order: int, score_weight: int) -> None:
        exam = self._owned_exam(examination_id, actor_user_id)
        if exam.status is not ExaminationStatus.DRAFT:
            raise InvalidExaminationTransition("Questions may only be changed while an examination is DRAFT.")
        if self.repository.get_question(question_id) is None:
            raise LookupError("Question not found.")
        self.repository.attach_question(examination_id, question_id, display_order, score_weight)

    def transition(self, examination_id: str, actor_user_id: str,
                   target: ExaminationStatus) -> Examination:
        exam = self._owned_exam(examination_id, actor_user_id)
        if target not in ALLOWED_TRANSITIONS[exam.status]:
            raise InvalidExaminationTransition(
                f"Transition {exam.status.value} -> {target.value} is not allowed."
            )
        if not self.repository.update_status(examination_id, target):
            raise ExaminationNotFoundError(examination_id)
        return Examination(exam.examination_id, exam.title, exam.description,
                           exam.owner_user_id, target, exam.starts_at, exam.ends_at)

    def _owned_exam(self, examination_id: str, actor_user_id: str) -> Examination:
        exam = self.repository.get_examination(examination_id)
        if exam is None:
            raise ExaminationNotFoundError(examination_id)
        if exam.owner_user_id != actor_user_id:
            raise ExaminationOwnershipError("Only the owning examiner may modify this examination.")
        return exam
