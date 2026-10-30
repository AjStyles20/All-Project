"""SQL-contract tests for MySQLReviewRepository without a live server."""
from datetime import datetime

import pytest
from mysql.connector import errors as mysql_errors

from app.domain.review import MarkingConflictError, ResponseMark
from app.persistence.mysql_review_repository import MySQLReviewRepository
from tests.unit.test_mysql_examination_repository import FakeDatabase

MARK = ResponseMark("s1", "q1", 7, "ok", 2, "lecturer-1", datetime(2026, 11, 2, 12, 0))


def test_mark_upsert_is_guarded_by_session_and_exam_status():
    database = FakeDatabase()
    assert MySQLReviewRepository(database).save_mark(MARK)
    sql, params = database.statements[0]
    assert "WHERE s.session_id=%s AND s.status='SUBMITTED' AND e.status IN ('ACTIVE','CLOSED')" in sql
    assert "ON DUPLICATE KEY UPDATE score=new.score" in sql and "VALUES(" not in sql
    assert params == ("q1", 7, "ok", 2, "lecturer-1", MARK.marked_at, "s1")


def test_refused_guard_reports_false_and_update_counts_as_saved():
    assert not MySQLReviewRepository(FakeDatabase(rowcount=0)).save_mark(MARK)
    assert MySQLReviewRepository(FakeDatabase(rowcount=2)).save_mark(MARK)


def test_integrity_error_becomes_marking_conflict():
    error = mysql_errors.IntegrityError(msg="fk", errno=1452)
    with pytest.raises(MarkingConflictError):
        MySQLReviewRepository(FakeDatabase(raise_on_execute=error)).save_mark(MARK)


def test_mark_guard_excludes_released_examinations():
    database = FakeDatabase()
    MySQLReviewRepository(database).save_mark(MARK)
    assert "NOT EXISTS (SELECT 1 FROM examination_result_releases r" in database.statements[0][0]


def test_history_row_written_in_same_transaction_only_on_success():
    database = FakeDatabase()
    MySQLReviewRepository(database).save_mark(MARK)
    sql, params = database.statements[1]
    assert sql.startswith("INSERT INTO response_mark_history")
    assert params == ("s1", "q1", 7, "ok", 2, "lecturer-1", MARK.marked_at)
    refused = FakeDatabase(rowcount=0)
    MySQLReviewRepository(refused).save_mark(MARK)
    assert len(refused.statements) == 1


def test_duplicate_release_reports_false():
    from app.domain.review import ResultRelease
    release = ResultRelease("e1", "lecturer-1", MARK.marked_at)
    assert MySQLReviewRepository(FakeDatabase()).create_release(release)
    duplicate = mysql_errors.IntegrityError(msg="Duplicate entry", errno=1062)
    assert not MySQLReviewRepository(FakeDatabase(raise_on_execute=duplicate)).create_release(release)
