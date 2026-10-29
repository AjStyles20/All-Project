"""FD-02 examination lifecycle and ownership policy."""
from dataclasses import replace
from datetime import datetime

from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationQuestionEntry, ExaminationStatus,
    ProgrammingQuestion,
)


class ExaminationNotFoundError(LookupError):
    pass


class QuestionNotFoundError(LookupError):
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

    def get_examination(self, examination_id: str, actor_user_id: str) -> Examination:
        return self._owned_exam(examination_id, actor_user_id)

    def list_examinations(self, actor_user_id: str) -> list[Examination]:
        return self.repository.list_examinations_by_owner(actor_user_id)

    def list_questions(self, actor_user_id: str) -> list[ProgrammingQuestion]:
        return self.repository.list_questions_by_creator(actor_user_id)

    def list_examination_questions(self, examination_id: str,
                                   actor_user_id: str) -> list[ExaminationQuestionEntry]:
        self._owned_exam(examination_id, actor_user_id)
        return self.repository.list_examination_questions(examination_id)

    def update_details(self, examination_id: str, actor_user_id: str, *, title: str,
                       description: str, starts_at: datetime | None,
                       ends_at: datetime | None) -> Examination:
        exam = self._owned_draft_exam(examination_id, actor_user_id)
        updated = replace(exam, title=title, description=description,
                          starts_at=starts_at, ends_at=ends_at)
        updated.validate()
        # The repository only updates DRAFT rows, so a concurrent schedule wins cleanly.
        if not self.repository.update_details(updated):
            raise InvalidExaminationTransition("Examination details may only be changed while DRAFT.")
        return updated

    def attach_question(self, examination_id: str, question_id: str, actor_user_id: str,
                        display_order: int, score_weight: int) -> None:
        self._owned_draft_exam(examination_id, actor_user_id)
        if self.repository.get_question(question_id) is None:
            raise QuestionNotFoundError(question_id)
        for entry in self.repository.list_examination_questions(examination_id):
            if entry.question.question_id == question_id:
                raise ExaminationConflictError("Question is already attached to this examination.")
            if entry.display_order == display_order:
                raise ExaminationConflictError("Another question already uses that display order.")
        self.repository.attach_question(examination_id, question_id, display_order, score_weight)

    def detach_question(self, examination_id: str, question_id: str, actor_user_id: str) -> None:
        self._owned_draft_exam(examination_id, actor_user_id)
        if not self.repository.detach_question(examination_id, question_id):
            raise QuestionNotFoundError(question_id)

    def transition(self, examination_id: str, actor_user_id: str,
                   target: ExaminationStatus) -> Examination:
        exam = self._owned_exam(examination_id, actor_user_id)
        if target not in ALLOWED_TRANSITIONS[exam.status]:
            raise InvalidExaminationTransition(
                f"Transition {exam.status.value} -> {target.value} is not allowed."
            )
        if target is ExaminationStatus.SCHEDULED and not self.repository.list_examination_questions(examination_id):
            raise InvalidExaminationTransition("An examination needs at least one question before scheduling.")
        # Compare-and-set on the status read above: two racing requests cannot both apply.
        if not self.repository.update_status(examination_id, target, expected=exam.status):
            raise InvalidExaminationTransition("Examination status changed concurrently; reload and retry.")
        return replace(exam, status=target)

    def _owned_exam(self, examination_id: str, actor_user_id: str) -> Examination:
        exam = self.repository.get_examination(examination_id)
        if exam is None:
            raise ExaminationNotFoundError(examination_id)
        if exam.owner_user_id != actor_user_id:
            raise ExaminationOwnershipError("Only the owning examiner may modify this examination.")
        return exam

    def _owned_draft_exam(self, examination_id: str, actor_user_id: str) -> Examination:
        exam = self._owned_exam(examination_id, actor_user_id)
        if exam.status is not ExaminationStatus.DRAFT:
            raise InvalidExaminationTransition("Examination content may only be changed while DRAFT.")
        return exam
