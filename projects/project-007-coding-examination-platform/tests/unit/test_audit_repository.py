import sqlite3
from datetime import datetime, timezone

import pytest

from app.domain.audit import AuditEvent, AuditEventType
from app.domain.models import ProgrammingCase
from app.persistence.audit_repository import AuditRepository
from app.persistence.database import Database
from app.persistence.repositories import P001Repository


def make_event(event_id="AUD-001"):
    return AuditEvent(
        event_id=event_id,
        case_id="CASE-DEV-003",
        event_type=AuditEventType.PROBE_SELECTION,
        recorded_at=datetime(2026, 9, 20, 10, 30, tzinfo=timezone.utc),
        actor_type="B4_ENGINE",
        rationale="Lowest-burden adequate probe.",
        claim_id="CC3",
        gap_type="EG-T3",
        probe_id="VP-CC3-02",
        decision="CONTINUE_VERIFICATION",
        method_version="B4-v1.0-development",
    )


def test_audit_event_round_trip(tmp_path):
    db = Database(tmp_path / "audit.db")
    db.initialize()
    P001Repository(db).add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even", task_description="Return evens.", language="python"
    ))
    repo = AuditRepository(db)
    event = make_event()
    repo.append(event)
    assert repo.list_for_case("CASE-DEV-003") == [event]


def test_duplicate_audit_event_id_is_rejected(tmp_path):
    db = Database(tmp_path / "audit.db")
    db.initialize()
    P001Repository(db).add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even", task_description="Return evens.", language="python"
    ))
    repo = AuditRepository(db)
    repo.append(make_event())
    with pytest.raises(sqlite3.IntegrityError):
        repo.append(make_event())


def test_audit_event_requires_existing_case(tmp_path):
    db = Database(tmp_path / "audit.db")
    db.initialize()
    with pytest.raises(sqlite3.IntegrityError):
        AuditRepository(db).append(make_event())
