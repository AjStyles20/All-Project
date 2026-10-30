"""SQL-contract tests for MySQLCandidateSessionRepository without a live server."""
from datetime import datetime

import pytest
from mysql.connector import errors as mysql_errors

from app.domain.candidate_session import (
    CandidateAssignment, ExaminationSession, SavedResponse, SessionConflictError, SessionStatus,
)
from app.persistence.mysql_candidate_session_repository import MySQLCandidateSessionRepository
from tests.unit.test_mysql_examination_repository import FakeDatabase

AT = datetime(2026, 11, 2, 10, 0)


def test_first_save_inserts_only_for_in_progress_session():
    database = FakeDatabase()
    repo = MySQLCandidateSessionRepository(database)
    assert repo.save_response(SavedResponse("s1", "q1", "code", 1, AT), previous_revision=0)
    sql, params = database.statements[0]
    assert sql.startswith("INSERT INTO submission_responses")
    assert sql.endswith("WHERE session_id=%s AND status='IN_PROGRESS'")
    assert params == ("q1", "code", 1, AT, "s1")


def test_update_is_revision_compare_and_set_and_session_guarded():
    database = FakeDatabase()
    repo = MySQLCandidateSessionRepository(database)
    repo.save_response(SavedResponse("s1", "q1", "v2", 2, AT), previous_revision=1)
    sql, params = database.statements[0]
    assert "AND r.revision=%s AND s.status='IN_PROGRESS'" in sql
    assert params[-1] == 1


def test_lost_race_reports_false():
    repo = MySQLCandidateSessionRepository(FakeDatabase(rowcount=0))
    assert not repo.save_response(SavedResponse("s1", "q1", "v2", 2, AT), previous_revision=1)
    assert not repo.mark_submitted("s1", AT)


def test_submit_only_moves_in_progress_sessions():
    database = FakeDatabase()
    MySQLCandidateSessionRepository(database).mark_submitted("s1", AT)
    assert database.statements[0][0].endswith("WHERE session_id=%s AND status='IN_PROGRESS'")


@pytest.mark.parametrize("call", [
    lambda r: r.create_assignment(CandidateAssignment("a1", "e1", "c1", "l1")),
    lambda r: r.create_session(ExaminationSession("s1", "a1", SessionStatus.IN_PROGRESS, AT)),
    lambda r: r.save_response(SavedResponse("s1", "q1", "x", 1, AT), previous_revision=0),
])
def test_integrity_errors_become_session_conflicts(call):
    duplicate = mysql_errors.IntegrityError(msg="Duplicate entry", errno=1062)
    repo = MySQLCandidateSessionRepository(FakeDatabase(raise_on_execute=duplicate))
    with pytest.raises(SessionConflictError):
        call(repo)


def test_candidate_check_requires_active_user_with_candidate_role():
    database = FakeDatabase()

    class Cursor:
        def __init__(self): self.rowcount = 0
        def execute(self, sql, params): database.statements.append((" ".join(sql.split()), params))
        def fetchone(self): return None
        def close(self): pass

    class Connection:
        def cursor(self, dictionary=False): return Cursor()

    from contextlib import contextmanager
    database.connect = contextmanager(lambda: (yield Connection()))
    assert not MySQLCandidateSessionRepository(database).is_candidate("u1")
    sql = database.statements[0][0]
    assert "u.is_active = TRUE" in sql and "r.role='CANDIDATE'" in sql
