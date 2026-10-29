"""SQL-contract tests for MySQLContractRepository and contract binding, without a server."""
import json
from contextlib import contextmanager
from datetime import datetime

import pytest
from mysql.connector import errors as mysql_errors

from app.domain.capability_contract import (
    CapabilityContract, ContractRequiredError, ContractStatus, IntegrityMode,
)
from app.domain.examination import ExaminationConflictError, ExaminationStatus
from app.persistence.mysql_contract_repository import MySQLContractRepository, contract_from_row
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from tests.contract_helpers import LAB_CAPABILITIES
from tests.unit.test_mysql_examination_repository import FakeDatabase

DRAFT = CapabilityContract("e1", 1, ContractStatus.DRAFT, IntegrityMode.LAB_CONTROLLED,
                           dict(LAB_CAPABILITIES), bound_by_user_id="lecturer-1")


def test_draft_update_and_insert_are_guarded_by_exam_draft_status():
    database = FakeDatabase(rowcount=0)
    assert not MySQLContractRepository(database).save_draft(DRAFT)
    update_sql, insert_sql = database.statements[0][0], database.statements[1][0]
    assert "c.status='DRAFT' AND e.status='DRAFT'" in update_sql
    assert insert_sql.endswith("WHERE examination_id=%s AND status='DRAFT'")
    # The stored document is the canonical hashed document, with its hash alongside.
    assert json.loads(database.statements[1][1][1]) == DRAFT.hashed_document()
    assert database.statements[1][1][2] == DRAFT.compute_hash()


class InsertCollides(FakeDatabase):
    """The DRAFT-only UPDATE matches nothing and the INSERT hits the primary key,
    which is what happens when that version is already BOUND."""
    @contextmanager
    def connect(self):
        with super().connect() as connection:
            make_cursor = connection.cursor

            def cursor(dictionary=False):
                inner = make_cursor(dictionary)
                execute = inner.execute

                def execute_or_collide(sql, params):
                    execute(sql, params)
                    if sql.lstrip().startswith("INSERT"):
                        raise mysql_errors.IntegrityError(msg="Duplicate entry", errno=1062)
                inner.execute = execute_or_collide
                return inner
            connection.cursor = cursor
            yield connection


def test_bound_version_is_never_rewritten():
    with pytest.raises(ExaminationConflictError):
        MySQLContractRepository(InsertCollides(rowcount=0)).save_draft(DRAFT)


def test_amend_supersedes_only_bound_version_of_scheduled_or_active_exam():
    database = FakeDatabase()
    amended = CapabilityContract("e1", 2, ContractStatus.BOUND, IntegrityMode.LAB_CONTROLLED,
                                 dict(LAB_CAPABILITIES), bound_by_user_id="lecturer-1",
                                 supersedes_version=1, amendment_reason="why")
    assert MySQLContractRepository(database).amend_bound(amended, datetime(2026, 11, 3, 10))
    supersede, insert = database.statements[0][0], database.statements[1][0]
    assert "c.status='BOUND' AND e.status IN ('SCHEDULED','ACTIVE')" in supersede
    assert insert.startswith("INSERT INTO capability_contracts") and "'BOUND'" in insert
    refused = FakeDatabase(rowcount=0)
    assert not MySQLContractRepository(refused).amend_bound(amended, datetime(2026, 11, 3, 10))
    assert len(refused.statements) == 1


def test_schedule_binds_draft_in_same_transaction():
    database = FakeDatabase(fetch_results=[(3,), (1,)])
    MySQLExaminationRepository(database).update_status("e1", ExaminationStatus.SCHEDULED,
                                                       expected=ExaminationStatus.DRAFT)
    sqls = [s for s, _ in database.statements]
    assert "FOR UPDATE" in sqls[1]
    assert sqls[2].startswith("UPDATE capability_contracts SET status='SUPERSEDED'")
    assert sqls[3].startswith("UPDATE capability_contracts SET status='BOUND'")
    assert database.statements[3][1] == ("e1", 3)


def test_schedule_without_any_contract_raises_so_the_transaction_rolls_back():
    database = FakeDatabase(fetch_results=[None, (0,)])
    with pytest.raises(ContractRequiredError):
        MySQLExaminationRepository(database).update_status("e1", ExaminationStatus.SCHEDULED,
                                                           expected=ExaminationStatus.DRAFT)


def test_row_round_trip_preserves_hash_inputs():
    row = {"document": json.dumps(DRAFT.hashed_document()), "status": "BOUND",
           "bound_at": datetime(2026, 11, 3, 9), "content_hash": DRAFT.compute_hash()}
    restored = contract_from_row(row)
    assert restored.compute_hash() == DRAFT.compute_hash() == restored.content_hash
