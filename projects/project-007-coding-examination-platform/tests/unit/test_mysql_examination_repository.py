"""SQL-contract tests for MySQLExaminationRepository without a live server.

The opt-in live test proves real MySQL behaviour; these tests pin the guards
that live behaviour depends on (status predicates, error translation) so they
are checked on every CI run.
"""
from contextlib import contextmanager

import pytest
from mysql.connector import errors as mysql_errors

from app.domain.examination import Examination, ExaminationConflictError, ExaminationStatus
from app.persistence.mysql_examination_repository import MySQLExaminationRepository


class FakeCursor:
    def __init__(self, database):
        self.database = database
        self.rowcount = database.rowcount

    def execute(self, sql, params):
        self.database.statements.append((" ".join(sql.split()), params))
        if self.database.raise_on_execute:
            raise self.database.raise_on_execute

    def fetchone(self):
        # Scripted results for repository code that reads rows (e.g. contract binding).
        return self.database.fetch_results.pop(0) if self.database.fetch_results else None

    def close(self):
        pass


class FakeDatabase:
    def __init__(self, rowcount=1, raise_on_execute=None, fetch_results=None):
        self.rowcount = rowcount
        self.raise_on_execute = raise_on_execute
        self.statements = []
        self.fetch_results = list(fetch_results or [])

    @contextmanager
    def connect(self):
        database = self

        class Connection:
            def cursor(self, dictionary=False):
                return FakeCursor(database)
        yield Connection()


def test_status_update_is_compare_and_set():
    # Scheduling also binds the contract: a draft (version 1) exists, then one BOUND row.
    database = FakeDatabase(fetch_results=[(1,), (1,)])
    repo = MySQLExaminationRepository(database)
    assert repo.update_status("e1", ExaminationStatus.SCHEDULED, expected=ExaminationStatus.DRAFT)
    sql, params = database.statements[0]
    assert sql.endswith("WHERE examination_id=%s AND status=%s")
    assert params == ("SCHEDULED", "e1", "DRAFT")


def test_status_update_reports_lost_race():
    repo = MySQLExaminationRepository(FakeDatabase(rowcount=0))
    assert not repo.update_status("e1", ExaminationStatus.SCHEDULED, expected=ExaminationStatus.DRAFT)


def test_attach_only_inserts_for_draft_examination():
    database = FakeDatabase()
    MySQLExaminationRepository(database).attach_question("e1", "q1", 1, 10)
    sql, params = database.statements[0]
    assert "SELECT examination_id,%s,%s,%s FROM examinations" in sql
    assert sql.endswith("WHERE examination_id=%s AND status='DRAFT'")
    assert params == ("q1", 1, 10, "e1")


def test_attach_to_non_draft_examination_is_conflict():
    repo = MySQLExaminationRepository(FakeDatabase(rowcount=0))
    with pytest.raises(ExaminationConflictError):
        repo.attach_question("e1", "q1", 1, 10)


def test_integrity_error_becomes_conflict():
    duplicate = mysql_errors.IntegrityError(msg="Duplicate entry", errno=1062)
    repo = MySQLExaminationRepository(FakeDatabase(raise_on_execute=duplicate))
    with pytest.raises(ExaminationConflictError):
        repo.attach_question("e1", "q1", 1, 10)


def test_detach_and_detail_updates_are_draft_guarded():
    database = FakeDatabase()
    repo = MySQLExaminationRepository(database)
    repo.detach_question("e1", "q1")
    assert "status='DRAFT'" in database.statements[0][0]
    assert database.statements[0][1] == ("e1", "q1", "e1")

    repo.update_details(Examination("e1", "Renamed", "", "lecturer-1", ExaminationStatus.DRAFT))
    assert database.statements[1][0].endswith("WHERE examination_id=%s AND status='DRAFT'")


def test_close_finalises_open_sessions_in_same_transaction():
    database = FakeDatabase()
    MySQLExaminationRepository(database).update_status(
        "e1", ExaminationStatus.CLOSED, expected=ExaminationStatus.ACTIVE)
    assert len(database.statements) == 2
    sql, params = database.statements[1]
    assert "s.submission_mode='AUTO_ON_CLOSE'" in sql
    assert sql.endswith("WHERE a.examination_id=%s AND s.status='IN_PROGRESS'")
    assert params == ("e1",)


def test_other_transitions_and_lost_close_race_leave_sessions_alone():
    database = FakeDatabase()
    MySQLExaminationRepository(database).update_status(
        "e1", ExaminationStatus.ACTIVE, expected=ExaminationStatus.SCHEDULED)
    assert len(database.statements) == 1
    lost = FakeDatabase(rowcount=0)
    MySQLExaminationRepository(lost).update_status(
        "e1", ExaminationStatus.CLOSED, expected=ExaminationStatus.ACTIVE)
    assert len(lost.statements) == 1
