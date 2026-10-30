from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from app.domain.enums import EvidenceState, EvidenceType
from app.domain.models import EvidenceItem, EvidenceStateRecord


def test_evidence_item_is_immutable():
    item = EvidenceItem(
        evidence_id="EV-001",
        case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Supplied tests passed.",
        source_type="automated_test",
        created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
    )

    with pytest.raises(FrozenInstanceError):
        item.content = "mutated"


def test_evidence_state_record_is_immutable():
    record = EvidenceStateRecord(
        case_id="CASE-DEV-003",
        claim_id="CC3",
        state=EvidenceState.UNRESOLVED,
        rationale="No independent test-design evidence.",
        recorded_at=datetime(2026, 9, 20, 9, 1, tzinfo=timezone.utc),
        source="B4-v1.0-development",
    )

    with pytest.raises(FrozenInstanceError):
        record.state = EvidenceState.SUPPORTED
