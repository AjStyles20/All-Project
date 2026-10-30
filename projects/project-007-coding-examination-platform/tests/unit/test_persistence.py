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
def repository(tmp_path):
    database = Database(tmp_path / "p001-test.db")
    database.initialize()
    return P001Repository(database)


def seed_case_and_claim(repository):
    repository.add_case(
        ProgrammingCase(
            case_id="CASE-DEV-003",
            title="Find even numbers",
            task_description="Return the even numbers in a list.",
            language="python",
        )
    )
    repository.add_claim(
        CompetenceClaim(
            claim_id="CC3",
            name="Test Design",
            definition="Independently design relevant tests and justify them.",
        )
    )


def test_case_claim_applicability_round_trips(repository):
    seed_case_and_claim(repository)
    repository.add_case_claim(
        CaseClaim(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            applicability=ClaimApplicability.REQUIRED,
        )
    )

    claims = repository.get_case_claims("CASE-DEV-003")

    assert claims == [
        CaseClaim(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            applicability=ClaimApplicability.REQUIRED,
        )
    ]


def test_evidence_can_be_linked_to_claim(repository):
    seed_case_and_claim(repository)
    evidence = EvidenceItem(
        evidence_id="EV-001",
        case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Supplied tests passed.",
        source_type="automated_test",
        created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
    )
    repository.add_evidence(evidence)
    repository.link_evidence(
        ClaimEvidenceLink(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            evidence_id="EV-001",
            rationale="Execution evidence is relevant context but does not itself prove test design.",
        )
    )

    assert repository.get_evidence_for_claim("CASE-DEV-003", "CC3") == [evidence]


def test_evidence_state_history_is_append_only_in_sequence(repository):
    seed_case_and_claim(repository)
    first = EvidenceStateRecord(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        state=EvidenceState.UNRESOLVED,
        rationale="No independent test-design evidence.",
        recorded_at=datetime(2026, 9, 20, 9, 1, tzinfo=timezone.utc),
        source="B4-v1.0-development",
    )
    second = EvidenceStateRecord(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        state=EvidenceState.SUPPORTED,
        rationale="Candidate supplied a relevant independent test with expected result and justification.",
        recorded_at=datetime(2026, 9, 20, 9, 4, tzinfo=timezone.utc),
        source="B4-v1.0-development",
    )

    repository.append_evidence_state(first)
    repository.append_evidence_state(second)

    assert repository.list_evidence_states("CASE-DEV-003", "CC3") == [first, second]


def test_foreign_keys_prevent_orphan_evidence(repository):
    evidence = EvidenceItem(
        evidence_id="EV-ORPHAN",
        case_id="CASE-MISSING",
        evidence_type=EvidenceType.ARTIFACT,
        content="orphan",
        source_type="artifact",
        created_at=datetime.now(timezone.utc),
    )

    with pytest.raises(Exception):
        repository.add_evidence(evidence)
