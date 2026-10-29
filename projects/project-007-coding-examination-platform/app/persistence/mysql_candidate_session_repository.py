"""MySQL repository for FD-03 candidate assignments, sessions and responses."""
from mysql.connector import errors as mysql_errors

from app.domain.candidate_session import (
    CandidateAssignment, ExaminationSession, SavedResponse, SessionConflictError, SessionStatus,
)
from app.persistence.mysql_database import MySQLDatabase


def _assignment(row) -> CandidateAssignment:
    return CandidateAssignment(row["assignment_id"], row["examination_id"],
                               row["candidate_user_id"], row["assigned_by_user_id"])


def _session(row) -> ExaminationSession:
    return ExaminationSession(row["session_id"], row["assignment_id"],
                              SessionStatus(row["status"]), row["started_at"], row["submitted_at"])


def _response(row) -> SavedResponse:
    return SavedResponse(row["session_id"], row["question_id"], row["content"],
                         row["revision"], row["saved_at"])


class MySQLCandidateSessionRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def _fetch_one(self, sql: str, params: tuple):
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, params)
            row = cursor.fetchone()
            cursor.close()
        return row

    def _fetch_all(self, sql: str, params: tuple) -> list:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            cursor.close()
        return rows

    def _write(self, sql: str, params: tuple, conflict_message: str) -> int:
        try:
            with self.database.connect() as connection:
                cursor = connection.cursor()
                cursor.execute(sql, params)
                changed = cursor.rowcount
                cursor.close()
        except mysql_errors.IntegrityError as exc:
            raise SessionConflictError(conflict_message) from exc
        return changed

    def is_candidate(self, user_id: str) -> bool:
        row = self._fetch_one(
            "SELECT 1 AS found FROM users u JOIN user_roles r ON r.user_id = u.user_id "
            "WHERE u.user_id=%s AND u.is_active = TRUE AND r.role='CANDIDATE'",
            (user_id,),
        )
        return row is not None

    def create_assignment(self, assignment: CandidateAssignment) -> None:
        self._write(
            "INSERT INTO candidate_assignments "
            "(assignment_id,examination_id,candidate_user_id,assigned_by_user_id) "
            "VALUES (%s,%s,%s,%s)",
            (assignment.assignment_id, assignment.examination_id,
             assignment.candidate_user_id, assignment.assigned_by_user_id),
            "Candidate is already assigned to this examination.",
        )

    def get_assignment(self, examination_id: str, candidate_user_id: str) -> CandidateAssignment | None:
        row = self._fetch_one(
            "SELECT * FROM candidate_assignments WHERE examination_id=%s AND candidate_user_id=%s",
            (examination_id, candidate_user_id),
        )
        return None if row is None else _assignment(row)

    def get_assignment_by_id(self, assignment_id: str) -> CandidateAssignment | None:
        row = self._fetch_one("SELECT * FROM candidate_assignments WHERE assignment_id=%s",
                              (assignment_id,))
        return None if row is None else _assignment(row)

    def list_assignments_for_examination(self, examination_id: str) -> list[CandidateAssignment]:
        rows = self._fetch_all(
            "SELECT * FROM candidate_assignments WHERE examination_id=%s "
            "ORDER BY assigned_at, assignment_id",
            (examination_id,),
        )
        return [_assignment(row) for row in rows]

    def list_assignments_for_candidate(self, candidate_user_id: str) -> list[CandidateAssignment]:
        rows = self._fetch_all(
            "SELECT * FROM candidate_assignments WHERE candidate_user_id=%s "
            "ORDER BY assigned_at, assignment_id",
            (candidate_user_id,),
        )
        return [_assignment(row) for row in rows]

    def create_session(self, session: ExaminationSession) -> None:
        # uq_session_assignment turns a racing second start into a conflict, not a duplicate.
        self._write(
            "INSERT INTO examination_sessions (session_id,assignment_id,status,started_at) "
            "VALUES (%s,%s,%s,%s)",
            (session.session_id, session.assignment_id, session.status.value, session.started_at),
            "A session already exists for this assignment.",
        )

    def get_session(self, session_id: str) -> ExaminationSession | None:
        row = self._fetch_one("SELECT * FROM examination_sessions WHERE session_id=%s", (session_id,))
        return None if row is None else _session(row)

    def get_session_for_assignment(self, assignment_id: str) -> ExaminationSession | None:
        row = self._fetch_one("SELECT * FROM examination_sessions WHERE assignment_id=%s",
                              (assignment_id,))
        return None if row is None else _session(row)

    def mark_submitted(self, session_id: str, submitted_at) -> bool:
        changed = self._write(
            "UPDATE examination_sessions SET status='SUBMITTED', submitted_at=%s "
            "WHERE session_id=%s AND status='IN_PROGRESS'",
            (submitted_at, session_id),
            "Session could not be submitted.",
        )
        return changed == 1

    def get_response(self, session_id: str, question_id: str) -> SavedResponse | None:
        row = self._fetch_one(
            "SELECT * FROM submission_responses WHERE session_id=%s AND question_id=%s",
            (session_id, question_id),
        )
        return None if row is None else _response(row)

    def list_responses(self, session_id: str) -> list[SavedResponse]:
        rows = self._fetch_all("SELECT * FROM submission_responses WHERE session_id=%s "
                               "ORDER BY question_id", (session_id,))
        return [_response(row) for row in rows]

    def save_response(self, response: SavedResponse, *, previous_revision: int) -> bool:
        response.validate()
        # Both statements only match an IN_PROGRESS session, so a save racing a submit
        # cannot change locked content. The revision predicate rejects stale overwrites.
        if previous_revision == 0:
            changed = self._write(
                "INSERT INTO submission_responses "
                "(session_id,question_id,content,revision,saved_at) "
                "SELECT session_id,%s,%s,%s,%s FROM examination_sessions "
                "WHERE session_id=%s AND status='IN_PROGRESS'",
                (response.question_id, response.content, response.revision, response.saved_at,
                 response.session_id),
                "A response was saved concurrently; reload before saving.",
            )
        else:
            changed = self._write(
                "UPDATE submission_responses r "
                "JOIN examination_sessions s ON s.session_id = r.session_id "
                "SET r.content=%s, r.revision=%s, r.saved_at=%s "
                "WHERE r.session_id=%s AND r.question_id=%s AND r.revision=%s "
                "AND s.status='IN_PROGRESS'",
                (response.content, response.revision, response.saved_at,
                 response.session_id, response.question_id, previous_revision),
                "Response could not be saved.",
            )
        return changed == 1
