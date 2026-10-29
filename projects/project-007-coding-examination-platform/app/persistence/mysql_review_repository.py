"""MySQL repository for FD-04 examiner review and marking."""
from mysql.connector import errors as mysql_errors

from app.domain.candidate_session import (
    CandidateAssignment, ExaminationSession, SessionStatus, SubmissionMode,
)
from app.domain.review import MarkingConflictError, ResponseMark, ResultRelease
from app.persistence.mysql_database import MySQLDatabase


def _mark(row) -> ResponseMark:
    return ResponseMark(row["session_id"], row["question_id"], row["score"], row["comment"],
                        row["response_revision"], row["marked_by_user_id"], row["marked_at"])


class MySQLReviewRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def list_sessions_for_examination(self, examination_id: str) -> list[tuple[ExaminationSession, CandidateAssignment]]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT s.*, a.examination_id, a.candidate_user_id, a.assigned_by_user_id "
                "FROM examination_sessions s "
                "JOIN candidate_assignments a ON a.assignment_id = s.assignment_id "
                "WHERE a.examination_id=%s ORDER BY s.started_at, s.session_id",
                (examination_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
        pairs = []
        for row in rows:
            mode = row["submission_mode"]
            session = ExaminationSession(row["session_id"], row["assignment_id"],
                                         SessionStatus(row["status"]), row["started_at"],
                                         row["submitted_at"], SubmissionMode(mode) if mode else None)
            assignment = CandidateAssignment(row["assignment_id"], row["examination_id"],
                                             row["candidate_user_id"], row["assigned_by_user_id"])
            pairs.append((session, assignment))
        return pairs

    def list_marks(self, session_id: str) -> list[ResponseMark]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM response_marks WHERE session_id=%s ORDER BY question_id",
                           (session_id,))
            rows = cursor.fetchall()
            cursor.close()
        return [_mark(row) for row in rows]

    def save_mark(self, mark: ResponseMark) -> bool:
        # The SELECT only matches a SUBMITTED session of an ACTIVE or CLOSED examination,
        # so a concurrent archive cannot be followed by a stray mark.
        try:
            with self.database.connect() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO response_marks "
                    "(session_id,question_id,score,comment,response_revision,marked_by_user_id,marked_at) "
                    "SELECT * FROM (SELECT s.session_id, %s AS question_id, %s AS score, "
                    "%s AS comment, %s AS response_revision, %s AS marked_by_user_id, "
                    "%s AS marked_at FROM examination_sessions s "
                    "JOIN candidate_assignments a ON a.assignment_id = s.assignment_id "
                    "JOIN examinations e ON e.examination_id = a.examination_id "
                    "WHERE s.session_id=%s AND s.status='SUBMITTED' "
                    "AND e.status IN ('ACTIVE','CLOSED') "
                    "AND NOT EXISTS (SELECT 1 FROM examination_result_releases r "
                    "WHERE r.examination_id = e.examination_id)) AS new "
                    "ON DUPLICATE KEY UPDATE score=new.score, comment=new.comment, "
                    "response_revision=new.response_revision, "
                    "marked_by_user_id=new.marked_by_user_id, marked_at=new.marked_at",
                    (mark.question_id, mark.score, mark.comment, mark.response_revision,
                     mark.marked_by_user_id, mark.marked_at, mark.session_id),
                )
                changed = cursor.rowcount
                if changed >= 1:
                    # DR-012 (2): same transaction, so history and current mark cannot diverge.
                    cursor.execute(
                        "INSERT INTO response_mark_history "
                        "(session_id,question_id,score,comment,response_revision,marked_by_user_id,marked_at) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (mark.session_id, mark.question_id, mark.score, mark.comment,
                         mark.response_revision, mark.marked_by_user_id, mark.marked_at),
                    )
                cursor.close()
        except mysql_errors.IntegrityError as exc:
            raise MarkingConflictError("Mark conflicts with existing data.") from exc
        # MySQL reports 1 for an insert and 2 for an update via ON DUPLICATE KEY (with
        # CLIENT_FOUND_ROWS an identical re-mark also reports 1); 0 means the guard refused.
        return changed >= 1

    def list_mark_history(self, session_id: str) -> list[ResponseMark]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM response_mark_history WHERE session_id=%s "
                           "ORDER BY question_id, history_id", (session_id,))
            rows = cursor.fetchall()
            cursor.close()
        return [_mark(row) for row in rows]

    def get_release(self, examination_id: str) -> ResultRelease | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM examination_result_releases WHERE examination_id=%s",
                           (examination_id,))
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else ResultRelease(row["examination_id"], row["released_by_user_id"],
                                                      row["released_at"])

    def create_release(self, release: ResultRelease) -> bool:
        """Returns False if the examination was already released (primary-key collision)."""
        try:
            with self.database.connect() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO examination_result_releases "
                    "(examination_id,released_by_user_id,released_at) VALUES (%s,%s,%s)",
                    (release.examination_id, release.released_by_user_id, release.released_at),
                )
                cursor.close()
        except mysql_errors.IntegrityError:
            return False
        return True
