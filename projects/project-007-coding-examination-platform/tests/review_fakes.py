"""In-memory stand-in for MySQLReviewRepository used by FD-04 tests.

It reads the session and examination fakes so save_mark applies the same guard as
the SQL: SUBMITTED session of an ACTIVE or CLOSED, unreleased examination, upsert per
question, and an appended history row for every successful save.
"""
from app.domain.candidate_session import SessionStatus
from app.domain.examination import ExaminationStatus


class InMemoryReviewRepository:
    def __init__(self, session_repository, examination_repository):
        self.sessions = session_repository
        self.examinations = examination_repository
        self.marks = {}
        self.history = []
        self.releases = {}

    def list_sessions_for_examination(self, examination_id):
        pairs = []
        for session in self.sessions.sessions.values():
            assignment = self.sessions.assignments[session.assignment_id]
            if assignment.examination_id == examination_id:
                pairs.append((session, assignment))
        return pairs

    def list_marks(self, session_id):
        return [m for (sid, _), m in sorted(self.marks.items()) if sid == session_id]

    def save_mark(self, mark):
        session = self.sessions.sessions.get(mark.session_id)
        if session is None or session.status is not SessionStatus.SUBMITTED:
            return False
        exam = self.examinations.exams[self.sessions.assignments[session.assignment_id].examination_id]
        if exam.status not in (ExaminationStatus.ACTIVE, ExaminationStatus.CLOSED):
            return False
        if exam.examination_id in self.releases:
            return False
        self.marks[(mark.session_id, mark.question_id)] = mark
        self.history.append(mark)
        return True

    def list_mark_history(self, session_id):
        return sorted((m for m in self.history if m.session_id == session_id),
                      key=lambda m: m.question_id)

    def get_release(self, examination_id):
        return self.releases.get(examination_id)

    def create_release(self, release):
        if release.examination_id in self.releases:
            return False
        self.releases[release.examination_id] = release
        return True
