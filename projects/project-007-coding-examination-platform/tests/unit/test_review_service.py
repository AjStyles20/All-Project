from dataclasses import replace
from datetime import datetime

import pytest

from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.domain.review import MAX_COMMENT_CHARS, MarkingConflictError
from app.services.candidate_session_service import CandidateSessionService, SessionNotFoundError
from app.services.examination_service import ExaminationOwnershipError, QuestionNotFoundError
from app.services.review_service import ReviewService
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
from tests.examination_fakes import InMemoryExaminationRepository
from tests.review_fakes import InMemoryReviewRepository

NOW = datetime(2026, 11, 2, 12, 0)


def setup():
    exams = InMemoryExaminationRepository()
    exams.create_examination(Examination("e1", "Exam", "", "lecturer-1", ExaminationStatus.ACTIVE))
    exams.create_question(ProgrammingQuestion("q1", "Loops", "Write a loop", "python", 10), "lecturer-1")
    exams.create_question(ProgrammingQuestion("q2", "Lists", "Use a list", "python", 5), "lecturer-1")
    exams.attachments += [("e1", "q1", 1, 10), ("e1", "q2", 2, 5)]
    session_repo = InMemoryCandidateSessionRepository({"student-1", "student-2"})
    candidates = CandidateSessionService(session_repo, exams, lambda: NOW)
    reviews = ReviewService(InMemoryReviewRepository(session_repo, exams), session_repo, exams, lambda: NOW)
    candidates.assign_candidate("e1", "student-1", "lecturer-1")
    candidates.assign_candidate("e1", "student-2", "lecturer-1")
    submitted = candidates.start_session("e1", "student-1").session_id
    candidates.save_response(submitted, "q1", "student-1", "for i in range(5): print(i)")
    candidates.save_response(submitted, "q1", "student-1", "for i in range(1, 6): print(i)")
    candidates.submit(submitted, "student-1")
    in_progress = candidates.start_session("e1", "student-2").session_id
    return reviews, exams, submitted, in_progress


def test_mark_records_reader_revision_and_upserts():
    reviews, _, sid, _ = setup()
    first = reviews.mark(sid, "q1", "lecturer-1", 7, "Off by one at first.")
    assert first.response_revision == 2 and first.marked_at == NOW
    reviews.mark(sid, "q1", "lecturer-1", 9, "Re-marked.")
    review = reviews.get_review(sid, "lecturer-1")
    assert review.marks["q1"].score == 9 and len(review.marks) == 1
    assert review.responses["q1"].revision == 2


def test_unanswered_question_can_be_marked_without_revision():
    reviews, _, sid, _ = setup()
    assert reviews.mark(sid, "q2", "lecturer-1", 0, "No answer.").response_revision is None


def test_score_bounds_comment_limit_and_foreign_question():
    reviews, _, sid, _ = setup()
    with pytest.raises(ValueError):
        reviews.mark(sid, "q1", "lecturer-1", 11, "")
    with pytest.raises(ValueError):
        reviews.mark(sid, "q1", "lecturer-1", 5, "x" * (MAX_COMMENT_CHARS + 1))
    with pytest.raises(QuestionNotFoundError):
        reviews.mark(sid, "not-in-exam", "lecturer-1", 1, "")


def test_in_progress_session_cannot_be_marked():
    reviews, _, _, open_sid = setup()
    with pytest.raises(MarkingConflictError):
        reviews.mark(open_sid, "q1", "lecturer-1", 5, "")


def test_archived_examination_is_frozen_for_marking():
    reviews, exams, sid, _ = setup()
    exams.exams["e1"] = replace(exams.exams["e1"], status=ExaminationStatus.ARCHIVED)
    with pytest.raises(MarkingConflictError):
        reviews.mark(sid, "q1", "lecturer-1", 5, "")


def test_closed_examination_can_still_be_marked():
    reviews, exams, sid, _ = setup()
    exams.exams["e1"] = replace(exams.exams["e1"], status=ExaminationStatus.CLOSED)
    assert reviews.mark(sid, "q1", "lecturer-1", 6, "").score == 6


def test_only_owner_reviews():
    reviews, _, sid, _ = setup()
    with pytest.raises(ExaminationOwnershipError):
        reviews.get_review(sid, "lecturer-2")
    with pytest.raises(ExaminationOwnershipError):
        reviews.mark(sid, "q1", "lecturer-2", 5, "")
    with pytest.raises(ExaminationOwnershipError):
        reviews.list_sessions("e1", "lecturer-2")
    with pytest.raises(SessionNotFoundError):
        reviews.get_review("missing", "lecturer-1")


def test_session_summaries_report_raw_totals():
    reviews, _, sid, open_sid = setup()
    reviews.mark(sid, "q1", "lecturer-1", 8, "")
    summaries = {s.session.session_id: s for s in reviews.list_sessions("e1", "lecturer-1")}
    assert (summaries[sid].marked_questions, summaries[sid].raw_score, summaries[sid].raw_max) == (1, 8, 15)
    assert summaries[open_sid].marked_questions == 0 and summaries[open_sid].total_questions == 2
