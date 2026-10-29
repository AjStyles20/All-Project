"""SQL-contract tests for MySQLResearchRepository without a live server."""
from datetime import datetime

from mysql.connector import errors as mysql_errors

from app.domain.research_bridge import BridgeOutcome, BridgeRecord
from app.persistence.mysql_research_repository import MySQLResearchRepository
from tests.unit.test_mysql_examination_repository import FakeDatabase

AT = datetime(2026, 11, 4, 9)
DUPLICATE = mysql_errors.IntegrityError(msg="Duplicate entry", errno=1062)


def test_current_consent_is_the_latest_event():
    database = FakeDatabase()
    MySQLResearchRepository(database).current_consent("e1", "s1")
    assert database.statements[0][0].endswith("ORDER BY event_id DESC LIMIT 1")


def test_duplicate_code_and_bridge_record_report_false_instead_of_raising():
    assert not MySQLResearchRepository(FakeDatabase(raise_on_execute=DUPLICATE)).create_research_code("e1", "s1", "R-1", AT)
    record = BridgeRecord("sess", "q1", "link", BridgeOutcome.BRIDGED, "op-R-1-q1", 1, "ecc:e1@v1#abc", AT)
    assert not MySQLResearchRepository(FakeDatabase(raise_on_execute=DUPLICATE)).save_bridge_record(record)
    assert MySQLResearchRepository(FakeDatabase()).save_bridge_record(record)


def test_withdrawal_forgets_records_and_code_link_in_one_transaction():
    database = FakeDatabase()
    MySQLResearchRepository(database).complete_withdrawal("e1", "s1", "R-1", 2, 0, AT)
    sqls = [sql for sql, _ in database.statements]
    assert sqls[0].startswith("DELETE b FROM research_bridge_records b")
    assert sqls[1].startswith("DELETE FROM research_identities")
    assert sqls[2].startswith("INSERT INTO research_withdrawal_log")
    # The log row carries the pseudonymous code and counts only, no user id.
    assert database.statements[2][1] == ("e1", "R-1", 2, 0, AT)
    no_code = FakeDatabase()
    MySQLResearchRepository(no_code).complete_withdrawal("e1", "s1", None, 0, 0, AT)
    assert len(no_code.statements) == 2
