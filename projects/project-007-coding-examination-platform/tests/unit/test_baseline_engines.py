from datetime import datetime, timezone

from app.domain.enums import EvidenceState, EvidenceType
from app.domain.models import EvidenceItem
from app.services.baseline_engines import B0Engine, B1Engine, B2Engine, B3Engine


def ev(evidence_id, evidence_type):
    return EvidenceItem(
        evidence_id=evidence_id, case_id="CASE-DEV-003",
        evidence_type=evidence_type, content=evidence_id,
        source_type="test-fixture", created_at=datetime.now(timezone.utc),
    )


def test_b0_excludes_process_policy_and_verification_evidence():
    evidence = [
        ev("A", EvidenceType.ARTIFACT), ev("X", EvidenceType.EXECUTION),
        ev("R", EvidenceType.RUBRIC), ev("P", EvidenceType.PROCESS),
        ev("V", EvidenceType.VERIFICATION), ev("C", EvidenceType.POLICY_CONTEXT),
    ]
    result = B0Engine().evaluate("CC3", evidence)
    assert result.evidence_ids == ("A", "X", "R")
    assert result.state is EvidenceState.UNRESOLVED


def test_b1_adds_process_but_not_verification():
    evidence = [
        ev("A", EvidenceType.ARTIFACT), ev("P", EvidenceType.PROCESS),
        ev("V", EvidenceType.VERIFICATION),
    ]
    result = B1Engine().evaluate("CC3", evidence)
    assert result.evidence_ids == ("A", "P")
    assert "V" not in result.evidence_ids


def test_b2_can_consume_fixed_viva_evidence_but_does_not_select_probes():
    evidence = [
        ev("A", EvidenceType.ARTIFACT), ev("P", EvidenceType.PROCESS),
        ev("V", EvidenceType.VERIFICATION),
    ]
    result = B2Engine().evaluate("CC3", evidence)
    assert result.evidence_ids == ("A", "P", "V")
    assert "no targeted selection" in result.rationale


def test_b3_excludes_verification_evidence_by_contract():
    evidence = [
        ev("A", EvidenceType.ARTIFACT), ev("P", EvidenceType.PROCESS),
        ev("V", EvidenceType.VERIFICATION),
    ]
    result = B3Engine().evaluate("CC3", evidence)
    assert result.evidence_ids == ("A", "P")
    assert "targeted verification prohibited" in result.rationale


def test_same_evidence_produces_explicitly_different_information_sets():
    evidence = [
        ev("A", EvidenceType.ARTIFACT), ev("X", EvidenceType.EXECUTION),
        ev("R", EvidenceType.RUBRIC), ev("P", EvidenceType.PROCESS),
        ev("V", EvidenceType.VERIFICATION),
    ]
    assert B0Engine().evaluate("CC3", evidence).evidence_ids == ("A", "X", "R")
    assert B1Engine().evaluate("CC3", evidence).evidence_ids == ("A", "X", "R", "P")
    assert B2Engine().evaluate("CC3", evidence).evidence_ids == ("A", "X", "R", "P", "V")
    assert B3Engine().evaluate("CC3", evidence).evidence_ids == ("A", "X", "R", "P")
