from dataclasses import replace
from datetime import datetime, timedelta

import pytest

from app.domain.candidate_session import MAX_RESPONSE_CHARS, SessionConflictError, SessionStatus
from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.services.candidate_session_service import (
    AssignmentNotFoundError, CandidateNotFoundError, CandidateSessionService, SessionNotFoundError,
)
from app.services.examination_service import ExaminationOwnershipError, QuestionNotFoundError
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
from tests.examination_fakes import InMemoryExaminationRepository

NOW = datetime(2026, 11, 2, 10, 0)


class Clock:
    def __init__(self, now): self.now = now
    def __call__(self): return self.now


def setup(status=ExaminationStatus.ACTIVE, starts_at=None, ends_at=None):
    exams = InMemoryExaminationRepository()
    exams.create_examination(Examination("e1", "Exam", "", "lecturer-1", status, starts_at, ends_at))
    exams.create_question(ProgrammingQuestion("q1", "Loops", "Write a loop", "python", 10), "lecturer-1")
    exams.create_question(ProgrammingQuestion("q-other", "Other", "Not in e1", "python", 5), "lecturer-1")
    exams.attachments.append(("e1", "q1", 1, 10))
    repo = InMemoryCandidateSessionRepository(candidates={"student-1", "student-2"})
    clock = Clock(NOW)
    service = CandidateSessionService(repo, exams, clock)
    return service, repo, exams, clock


def assigned(**kwargs):
    service, repo, exams, clock = setup(**kwargs)
    service.assign_candidate("e1", "student-1", "lecturer-1")
    return service, repo, exams, clock


def set_status(exams, status):
    exams.exams["e1"] = replace(exams.exams["e1"], status=status)


def test_only_owner_assigns_and_only_real_candidates():
    service, _, _, _ = setup()
    with pytest.raises(ExaminationOwnershipError):
        service.assign_candidate("e1", "student-1", "lecturer-2")
    with pytest.raises(CandidateNotFoundError):
        service.assign_candidate("e1", "lecturer-1", "lecturer-1")
    service.assign_candidate("e1", "student-1", "lecturer-1")
    with pytest.raises(SessionConflictError):
        service.assign_candidate("e1", "student-1", "lecturer-1")
    assert [a.candidate_user_id for a in service.list_assignments("e1", "lecturer-1")] == ["student-1"]


def test_closed_examination_rejects_new_assignments():
    service, _, _, _ = setup(status=ExaminationStatus.CLOSED)
    with pytest.raises(SessionConflictError):
        service.assign_candidate("e1", "student-1", "lecturer-1")


def test_unassigned_candidate_cannot_start():
    service, _, _, _ = setup()
    with pytest.raises(AssignmentNotFoundError):
        service.start_session("e1", "student-1")


def test_session_only_starts_while_active():
    service, _, exams, _ = assigned(status=ExaminationStatus.SCHEDULED)
    with pytest.raises(SessionConflictError):
        service.start_session("e1", "student-1")
    set_status(exams, ExaminationStatus.ACTIVE)
    assert service.start_session("e1", "student-1").status is SessionStatus.IN_PROGRESS


def test_time_window_is_enforced():
    service, _, _, clock = assigned(starts_at=NOW + timedelta(hours=1), ends_at=NOW + timedelta(hours=3))
    with pytest.raises(SessionConflictError):
        service.start_session("e1", "student-1")
    clock.now = NOW + timedelta(hours=1)
    session = service.start_session("e1", "student-1")
    clock.now = NOW + timedelta(hours=3)
    with pytest.raises(SessionConflictError):
        service.save_response(session.session_id, "q1", "student-1", "late")


def test_repeated_start_resumes_the_same_session():
    service, repo, _, _ = assigned()
    first = service.start_session("e1", "student-1")
    assert service.start_session("e1", "student-1").session_id == first.session_id
    assert len(repo.sessions) == 1


def test_racing_start_resumes_the_winner():
    service, repo, _, _ = assigned()
    winner = service.start_session("e1", "student-1")
    # Simulate a request whose existence check ran before the winner was stored:
    # only the service's first lookup is blinded; the unique-key check stays real.
    real_lookup = repo.get_session_for_assignment
    calls = []
    def first_lookup_misses(assignment_id):
        calls.append(assignment_id)
        return None if len(calls) == 1 else real_lookup(assignment_id)
    repo.get_session_for_assignment = first_lookup_misses
    original_create = repo.create_session
    def create_checking_real_key(session):
        if real_lookup(session.assignment_id):
            raise SessionConflictError("A session already exists for this assignment.")
        original_create(session)
    repo.create_session = create_checking_real_key
    resumed = service.start_session("e1", "student-1")
    assert resumed.session_id == winner.session_id
    assert len(repo.sessions) == 1


def test_save_increments_revision_and_detects_stale_base():
    service, _, _, _ = assigned()
    sid = service.start_session("e1", "student-1").session_id
    first = service.save_response(sid, "q1", "student-1", "for i in range(3): pass")
    assert first.revision == 1
    second = service.save_response(sid, "q1", "student-1", "v2", base_revision=1)
    assert second.revision == 2
    with pytest.raises(SessionConflictError):
        service.save_response(sid, "q1", "student-1", "stale tab", base_revision=1)


def test_save_rejects_foreign_question_oversized_content_and_other_candidate():
    service, _, _, _ = assigned()
    sid = service.start_session("e1", "student-1").session_id
    with pytest.raises(QuestionNotFoundError):
        service.save_response(sid, "q-other", "student-1", "x")
    with pytest.raises(ValueError):
        service.save_response(sid, "q1", "student-1", "x" * (MAX_RESPONSE_CHARS + 1))
    with pytest.raises(SessionNotFoundError):
        service.save_response(sid, "q1", "student-2", "not mine")


def test_submit_locks_responses_and_is_idempotent():
    service, _, _, clock = assigned()
    sid = service.start_session("e1", "student-1").session_id
    service.save_response(sid, "q1", "student-1", "answer")
    clock.now = NOW + timedelta(minutes=30)
    submitted = service.submit(sid, "student-1")
    assert submitted.status is SessionStatus.SUBMITTED
    assert submitted.submitted_at == NOW + timedelta(minutes=30)
    assert service.submit(sid, "student-1").submitted_at == submitted.submitted_at
    with pytest.raises(SessionConflictError):
        service.save_response(sid, "q1", "student-1", "after submit")
    view = service.get_session_view(sid, "student-1")
    assert view.responses["q1"].content == "answer"


def test_submit_after_deadline_locks_existing_content():
    service, _, _, clock = assigned(ends_at=NOW + timedelta(hours=1))
    sid = service.start_session("e1", "student-1").session_id
    service.save_response(sid, "q1", "student-1", "on time")
    clock.now = NOW + timedelta(hours=2)
    assert service.submit(sid, "student-1").status is SessionStatus.SUBMITTED


def test_submit_refused_once_examination_closed():
    service, _, exams, _ = assigned()
    sid = service.start_session("e1", "student-1").session_id
    set_status(exams, ExaminationStatus.CLOSED)
    with pytest.raises(SessionConflictError):
        service.submit(sid, "student-1")


def test_candidate_lists_only_own_assignments():
    service, _, _, _ = assigned()
    assert [exam.examination_id for _, exam in service.list_candidate_examinations("student-1")] == ["e1"]
    assert service.list_candidate_examinations("student-2") == []
