import pytest
from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.services.examination_service import (
    ExaminationOwnershipError, ExaminationService, InvalidExaminationTransition
)


class FakeRepository:
    def __init__(self):
        self.exams = {}
        self.questions = {}
        self.attachments = []

    def create_examination(self, exam): self.exams[exam.examination_id] = exam
    def get_examination(self, exam_id): return self.exams.get(exam_id)
    def update_status(self, exam_id, status):
        exam = self.exams.get(exam_id)
        if not exam: return False
        self.exams[exam_id] = Examination(exam.examination_id, exam.title, exam.description,
                                          exam.owner_user_id, status, exam.starts_at, exam.ends_at)
        return True
    def create_question(self, q, creator): self.questions[q.question_id] = q
    def get_question(self, qid): return self.questions.get(qid)
    def attach_question(self, eid, qid, order, weight): self.attachments.append((eid,qid,order,weight))


def service_with_exam():
    repo = FakeRepository()
    service = ExaminationService(repo)
    service.create_examination(Examination("e1","Exam","","lecturer-1",ExaminationStatus.DRAFT))
    return service, repo


def test_lifecycle_happy_path():
    service, _ = service_with_exam()
    assert service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED).status is ExaminationStatus.SCHEDULED
    assert service.transition("e1","lecturer-1",ExaminationStatus.ACTIVE).status is ExaminationStatus.ACTIVE
    assert service.transition("e1","lecturer-1",ExaminationStatus.CLOSED).status is ExaminationStatus.CLOSED
    assert service.transition("e1","lecturer-1",ExaminationStatus.ARCHIVED).status is ExaminationStatus.ARCHIVED


def test_illegal_transition_is_rejected():
    service, _ = service_with_exam()
    with pytest.raises(InvalidExaminationTransition):
        service.transition("e1","lecturer-1",ExaminationStatus.ACTIVE)


def test_non_owner_cannot_modify_exam():
    service, _ = service_with_exam()
    with pytest.raises(ExaminationOwnershipError):
        service.transition("e1","other",ExaminationStatus.SCHEDULED)


def test_questions_can_only_be_attached_to_draft_exam():
    service, repo = service_with_exam()
    service.create_question(ProgrammingQuestion("q1","Loops","Write loop","python",10),"lecturer-1")
    service.attach_question("e1","q1","lecturer-1",1,10)
    assert repo.attachments == [("e1","q1",1,10)]
    service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    with pytest.raises(InvalidExaminationTransition):
        service.attach_question("e1","q1","lecturer-1",2,10)
