from datetime import datetime, timezone

from app.domain.enums import EvidenceType
from app.domain.models import EvidenceItem
from app.services.baseline_engines import B0Engine, B1Engine, B2Engine, B3Engine


def ev(evidence_id, evidence_type, source_type):
    return EvidenceItem(
        evidence_id=evidence_id, case_id="CASE-DEV-003",
        evidence_type=evidence_type, content=evidence_id,
        source_type=source_type, created_at=datetime.now(timezone.utc),
    )


def test_b2_accepts_fixed_viva_but_rejects_b4_targeted_verification():
    evidence=[
        ev("A",EvidenceType.ARTIFACT,"submission"),
        ev("FV",EvidenceType.VERIFICATION,"fixed_viva"),
        ev("TV",EvidenceType.VERIFICATION,"targeted_verification"),
    ]
    result=B2Engine().evaluate("CC3",evidence)
    assert "FV" in result.evidence_ids
    assert "TV" not in result.evidence_ids


def test_b0_b1_b3_reject_all_verification_regardless_of_provenance():
    evidence=[
        ev("A",EvidenceType.ARTIFACT,"submission"),
        ev("FV",EvidenceType.VERIFICATION,"fixed_viva"),
        ev("TV",EvidenceType.VERIFICATION,"targeted_verification"),
    ]
    for engine in (B0Engine(),B1Engine(),B3Engine()):
        ids=engine.evaluate("CC3",evidence).evidence_ids
        assert "FV" not in ids and "TV" not in ids


def test_unmarked_verification_does_not_enter_b2():
    result=B2Engine().evaluate("CC3",[
        ev("V",EvidenceType.VERIFICATION,"test-fixture"),
    ])
    assert result.evidence_ids==()
