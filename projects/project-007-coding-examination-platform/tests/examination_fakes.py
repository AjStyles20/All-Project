"""In-memory stand-in for MySQLExaminationRepository used by FD-02 unit/API tests.

It mirrors the repository's guarded SQL semantics (DRAFT-only content changes,
compare-and-set status updates, unique membership/order) so service and API
tests exercise the same contract that the live MySQL test checks for real.
"""
from dataclasses import replace

from app.domain.examination import (
    ExaminationConflictError, ExaminationQuestionEntry, ExaminationStatus,
)


class InMemoryExaminationRepository:
    def __init__(self):
        self.exams = {}
        self.questions = {}
        self.question_creators = {}
        self.attachments = []

    def create_examination(self, exam):
        exam.validate()
        self.exams[exam.examination_id] = exam

    def get_examination(self, examination_id):
        return self.exams.get(examination_id)

    def list_examinations_by_owner(self, owner_user_id):
        return [e for e in self.exams.values() if e.owner_user_id == owner_user_id]

    def update_details(self, exam):
        current = self.exams.get(exam.examination_id)
        if current is None or current.status is not ExaminationStatus.DRAFT:
            return False
        self.exams[exam.examination_id] = exam
        return True

    def update_status(self, examination_id, status, *, expected):
        current = self.exams.get(examination_id)
        if current is None or current.status is not expected:
            return False
        self.exams[examination_id] = replace(current, status=status)
        return True

    def create_question(self, question, created_by_user_id):
        question.validate()
        self.questions[question.question_id] = question
        self.question_creators[question.question_id] = created_by_user_id

    def get_question(self, question_id):
        return self.questions.get(question_id)

    def list_questions_by_creator(self, created_by_user_id):
        return [q for qid, q in self.questions.items()
                if self.question_creators[qid] == created_by_user_id]

    def list_examination_questions(self, examination_id):
        rows = sorted((a for a in self.attachments if a[0] == examination_id), key=lambda a: a[2])
        return [ExaminationQuestionEntry(self.questions[qid], order, weight)
                for _, qid, order, weight in rows]

    def attach_question(self, examination_id, question_id, display_order, score_weight):
        exam = self.exams.get(examination_id)
        if exam is None or exam.status is not ExaminationStatus.DRAFT:
            raise ExaminationConflictError("Examination is no longer DRAFT.")
        for eid, qid, order, _ in self.attachments:
            if eid == examination_id and (qid == question_id or order == display_order):
                raise ExaminationConflictError("Duplicate attachment.")
        self.attachments.append((examination_id, question_id, display_order, score_weight))

    def detach_question(self, examination_id, question_id):
        exam = self.exams.get(examination_id)
        if exam is None or exam.status is not ExaminationStatus.DRAFT:
            return False
        before = len(self.attachments)
        self.attachments = [a for a in self.attachments
                            if not (a[0] == examination_id and a[1] == question_id)]
        return len(self.attachments) < before
