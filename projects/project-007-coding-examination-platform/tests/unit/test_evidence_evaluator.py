from datetime import datetime, timezone

from app.domain.enums import EvidenceState, EvidenceType
from app.domain.models import EvidenceItem
from app.services.evidence_evaluator import EvidenceEvaluator


def evidence(evidence_id, evidence_type, content):
    return EvidenceItem(
        evidence_id=evidence_id,
        case_id="CASE-DEV-003",
        evidence_type=evidence_type,
        content=content,
        source_type="development_fixture",
        created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
    )


def test_supplied_tests_do_not_prove_cc3_test_design():
    evaluator = EvidenceEvaluator()
    result = evaluator.evaluate(
        "CC3",
        [
            evidence("EV-ART", EvidenceType.ARTIFACT, "Correct find_even implementation."),
            evidence("EV-EXEC", EvidenceType.EXECUTION, "All supplied tests passed."),
        ],
    )

    assert result.state is EvidenceState.UNRESOLVED
    assert "does not by itself establish CC3" in result.rationale


def test_unknown_claim_abstains_as_unresolved():
    result = EvidenceEvaluator().evaluate("CC99", [])

    assert result.state is EvidenceState.UNRESOLVED
    assert "No frozen evaluation rule" in result.rationale


def test_unstructured_verification_does_not_manufacture_supported_state():
    result = EvidenceEvaluator().evaluate(
        "CC3",
        [evidence("EV-V1", EvidenceType.VERIFICATION, "Some free-text response.")],
    )

    assert result.state is EvidenceState.UNRESOLVED
    assert "no frozen structured CC3 response rubric" in result.rationale
