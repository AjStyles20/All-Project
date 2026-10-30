import sqlite3
from datetime import datetime, timezone

import pytest

from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import (
    CaseClaim,
    ClaimEvidenceLink,
    CompetenceClaim,
    EvidenceItem,
    EvidenceStateRecord,
    ProgrammingCase,
)
from app.persistence.database import Database
from app.persistence.repositories import P001Repository


@pytest.fixture
def setup_repo(tmp_path):
    database = Database(tmp_path / "constraints.db")
    database.initialize()
    repository = P001Repository(database)
    repository.add_case(
        ProgrammingCase(
            case_id="CASE-DEV-003",
            title="Find even numbers",
            task_description="Return even values.",
            language="python",
        )
    )
    repository.add_claim(
        CompetenceClaim(
            claim_id="CC3",
            name="Test Design",
            definition="Design and justify relevant tests.",
        )
    )
    return database, repository


def test_duplicate_evidence_id_is_rejected(setup_repo):
    _, repository = setup_repo
    item = EvidenceItem(
        evidence_id="EV-001",
        case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Supplied tests passed.",
        source_type="automated_test",
        created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
    )
    repository.add_evidence(item)

    with pytest.raises(sqlite3.IntegrityError):
        repository.add_evidence(item)


def test_duplicate_case_claim_mapping_is_rejected(setup_repo):
    _, repository = setup_repo
    mapping = CaseClaim(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
    )
    repository.add_case_claim(mapping)

    with pytest.raises(sqlite3.IntegrityError):
        repository.add_case_claim(mapping)


def test_duplicate_claim_evidence_link_is_rejected(setup_repo):
    _, repository = setup_repo
    item = EvidenceItem(
        evidence_id="EV-002",
        case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Supplied tests passed.",
        source_type="automated_test",
        created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
    )
    repository.add_evidence(item)
    link = ClaimEvidenceLink(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        evidence_id="EV-002",
        rationale="Relevant execution context.",
    )
    repository.link_evidence(link)

    with pytest.raises(sqlite3.IntegrityError):
        repository.link_evidence(link)


def test_failed_transaction_rolls_back(setup_repo):
    database, _ = setup_repo

    with pytest.raises(sqlite3.IntegrityError):
        with database.connect() as connection:
            connection.execute(
                """INSERT INTO evidence_items
                   (evidence_id, case_id, evidence_type, content, source_type, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    "EV-ROLLBACK",
                    "CASE-DEV-003",
                    "EXECUTION",
                    "Temporary evidence.",
                    "test",
                    "2026-09-20T09:00:00+00:00",
                ),
            )
            connection.execute(
                """INSERT INTO evidence_items
                   (evidence_id, case_id, evidence_type, content, source_type, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    "EV-ROLLBACK",
                    "CASE-DEV-003",
                    "EXECUTION",
                    "Duplicate should fail.",
                    "test",
                    "2026-09-20T09:01:00+00:00",
                ),
            )

    with database.connect() as connection:
        count = connection.execute(
            "SELECT COUNT(*) FROM evidence_items WHERE evidence_id = ?",
            ("EV-ROLLBACK",),
        ).fetchone()[0]

    assert count == 0


def test_state_history_accepts_transition_without_overwriting(setup_repo):
    _, repository = setup_repo
    first = EvidenceStateRecord(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        state=EvidenceState.UNRESOLVED,
        rationale="No independent evidence.",
        recorded_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
        source="development",
    )
    second = EvidenceStateRecord(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        state=EvidenceState.SUPPORTED,
        rationale="Independent verification supplied.",
        recorded_at=datetime(2026, 9, 20, 9, 5, tzinfo=timezone.utc),
        source="development",
    )

    repository.append_evidence_state(first)
    repository.append_evidence_state(second)

    assert repository.list_evidence_states("CASE-DEV-003", "CC3") == [first, second]
