"""In-memory stand-in for MySQLCandidateSessionRepository used by FD-03 tests.

Mirrors the repository's guards: unique assignment per candidate/examination,
one session per assignment, IN_PROGRESS-only saves and submit, and the
revision compare-and-set on response updates.
"""
from dataclasses import replace

from app.domain.candidate_session import SessionConflictError, SessionStatus


class InMemoryCandidateSessionRepository:
    def __init__(self, candidates=()):
        self.candidates = set(candidates)
        self.assignments = {}
        self.sessions = {}
        self.responses = {}

    def is_candidate(self, user_id):
        return user_id in self.candidates

    def create_assignment(self, assignment):
        if self.get_assignment(assignment.examination_id, assignment.candidate_user_id):
            raise SessionConflictError("Candidate is already assigned to this examination.")
        self.assignments[assignment.assignment_id] = assignment

    def get_assignment(self, examination_id, candidate_user_id):
        for a in self.assignments.values():
            if a.examination_id == examination_id and a.candidate_user_id == candidate_user_id:
                return a
        return None

    def get_assignment_by_id(self, assignment_id):
        return self.assignments.get(assignment_id)

    def list_assignments_for_examination(self, examination_id):
        return [a for a in self.assignments.values() if a.examination_id == examination_id]

    def list_assignments_for_candidate(self, candidate_user_id):
        return [a for a in self.assignments.values() if a.candidate_user_id == candidate_user_id]

    def create_session(self, session):
        if self.get_session_for_assignment(session.assignment_id):
            raise SessionConflictError("A session already exists for this assignment.")
        self.sessions[session.session_id] = session

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def get_session_for_assignment(self, assignment_id):
        for s in self.sessions.values():
            if s.assignment_id == assignment_id:
                return s
        return None

    def mark_submitted(self, session_id, submitted_at):
        session = self.sessions.get(session_id)
        if session is None or session.status is not SessionStatus.IN_PROGRESS:
            return False
        self.sessions[session_id] = replace(session, status=SessionStatus.SUBMITTED,
                                            submitted_at=submitted_at)
        return True

    def get_response(self, session_id, question_id):
        return self.responses.get((session_id, question_id))

    def list_responses(self, session_id):
        return [r for (sid, _), r in sorted(self.responses.items()) if sid == session_id]

    def save_response(self, response, *, previous_revision):
        response.validate()
        session = self.sessions.get(response.session_id)
        if session is None or session.status is not SessionStatus.IN_PROGRESS:
            return False
        key = (response.session_id, response.question_id)
        current = self.responses.get(key)
        if (current.revision if current else 0) != previous_revision:
            return False
        self.responses[key] = response
        return True
