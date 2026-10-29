import pytest
from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationStatus, ProgrammingQuestion,
)
from app.services.examination_service import (
    ExaminationNotFoundError, ExaminationOwnershipError, ExaminationService,
    InvalidExaminationTransition, QuestionNotFoundError,
)
from tests.examination_fakes import InMemoryExaminationRepository


def service_with_exam():
    repo = InMemoryExaminationRepository()
    service = ExaminationService(repo)
    service.create_examination(Examination("e1","Exam","","lecturer-1",ExaminationStatus.DRAFT))
    return service, repo


def service_with_question():
    service, repo = service_with_exam()
    service.create_question(ProgrammingQuestion("q1","Loops","Write loop","python",10),"lecturer-1")
    return service, repo


def test_lifecycle_happy_path():
    service, _ = service_with_question()
    service.attach_question("e1","q1","lecturer-1",1,10)
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
    service, repo = service_with_question()
    service.attach_question("e1","q1","lecturer-1",1,10)
    assert repo.attachments == [("e1","q1",1,10)]
    service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    with pytest.raises(InvalidExaminationTransition):
        service.attach_question("e1","q1","lecturer-1",2,10)


def test_empty_examination_cannot_be_scheduled():
    service, repo = service_with_exam()
    with pytest.raises(InvalidExaminationTransition):
        service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    assert repo.exams["e1"].status is ExaminationStatus.DRAFT


def test_stale_status_loses_compare_and_set():
    service, repo = service_with_question()
    service.attach_question("e1","q1","lecturer-1",1,10)
    stale = repo.exams["e1"]
    service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    # A second request that read DRAFT before the first one committed must not apply.
    repo.get_examination = lambda eid: stale
    with pytest.raises(InvalidExaminationTransition):
        service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    assert repo.exams["e1"].status is ExaminationStatus.SCHEDULED


def test_duplicate_question_or_display_order_is_a_conflict():
    service, _ = service_with_question()
    service.create_question(ProgrammingQuestion("q2","Lists","Use a list","python",5),"lecturer-1")
    service.attach_question("e1","q1","lecturer-1",1,10)
    with pytest.raises(ExaminationConflictError):
        service.attach_question("e1","q1","lecturer-1",2,10)
    with pytest.raises(ExaminationConflictError):
        service.attach_question("e1","q2","lecturer-1",1,5)


def test_unknown_question_and_examination_are_not_found():
    service, _ = service_with_exam()
    with pytest.raises(QuestionNotFoundError):
        service.attach_question("e1","missing","lecturer-1",1,10)
    with pytest.raises(ExaminationNotFoundError):
        service.get_examination("missing","lecturer-1")


def test_examiner_cannot_attach_another_examiners_question():
    service, repo = service_with_exam()
    service.create_question(ProgrammingQuestion("q-foreign","Theirs","Not mine","python",5),"lecturer-2")
    with pytest.raises(QuestionNotFoundError):
        service.attach_question("e1","q-foreign","lecturer-1",1,5)
    assert repo.attachments == []


def test_detach_only_while_draft():
    service, repo = service_with_question()
    service.attach_question("e1","q1","lecturer-1",1,10)
    service.detach_question("e1","q1","lecturer-1")
    assert repo.attachments == []
    with pytest.raises(QuestionNotFoundError):
        service.detach_question("e1","q1","lecturer-1")
    service.attach_question("e1","q1","lecturer-1",1,10)
    service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    with pytest.raises(InvalidExaminationTransition):
        service.detach_question("e1","q1","lecturer-1")


def test_update_details_validates_and_requires_draft():
    service, _ = service_with_question()
    updated = service.update_details("e1","lecturer-1",title="Renamed",description="d",
                                     starts_at=None,ends_at=None)
    assert updated.title == "Renamed"
    with pytest.raises(ValueError):
        service.update_details("e1","lecturer-1",title="   ",description="",starts_at=None,ends_at=None)
    service.attach_question("e1","q1","lecturer-1",1,10)
    service.transition("e1","lecturer-1",ExaminationStatus.SCHEDULED)
    with pytest.raises(InvalidExaminationTransition):
        service.update_details("e1","lecturer-1",title="Late",description="",starts_at=None,ends_at=None)


def test_reads_are_scoped_to_the_owner():
    service, _ = service_with_question()
    service.create_examination(Examination("e2","Other","","lecturer-2",ExaminationStatus.DRAFT))
    assert [e.examination_id for e in service.list_examinations("lecturer-1")] == ["e1"]
    assert [q.question_id for q in service.list_questions("lecturer-1")] == ["q1"]
    assert service.list_questions("lecturer-2") == []
    with pytest.raises(ExaminationOwnershipError):
        service.get_examination("e2","lecturer-1")
    with pytest.raises(ExaminationOwnershipError):
        service.list_examination_questions("e2","lecturer-1")
