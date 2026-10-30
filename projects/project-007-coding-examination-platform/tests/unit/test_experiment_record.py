import pytest

from app.domain.enums import EvidenceState
from app.services.experiment_record import (
    CaseMethodComparison, IndependentReferenceJudgment, MethodExperimentRecord,
)
from app.services.verification_burden import VerificationBurden


def record(method, state=EvidenceState.UNRESOLVED, reference=None):
    return MethodExperimentRecord(
        case_id="CASE-DEV-003", claim_id="CC3", method=method,
        method_version=f"{method}-v1", system_state=state,
        evidence_ids=("EV-1",),
        burden=VerificationBurden(0, 0.0, ()), reference=reference,
    )


def test_system_output_does_not_become_reference_judgment_implicitly():
    r = record("B3", EvidenceState.UNRESOLVED)
    assert r.reference is None
    assert r.agrees_with_reference is None


def test_agreement_is_computed_only_against_explicit_independent_reference():
    ref = IndependentReferenceJudgment(
        assessor_id="ASSESSOR-01", claim_id="CC3",
        state=EvidenceState.SUPPORTED, rationale="Independent rubric judgment.",
        rubric_version="ASSESSOR-RUBRIC-v1.0",
    )
    assert record("B4", EvidenceState.SUPPORTED, ref).agrees_with_reference is True
    assert record("B3", EvidenceState.UNRESOLVED, ref).agrees_with_reference is False


def test_reference_for_different_claim_is_rejected():
    ref = IndependentReferenceJudgment(
        assessor_id="ASSESSOR-01", claim_id="CC5",
        state=EvidenceState.SUPPORTED, rationale="Wrong claim.",
        rubric_version="ASSESSOR-RUBRIC-v1.0",
    )
    with pytest.raises(ValueError, match="same competence claim"):
        record("B4", reference=ref)


def test_case_comparison_rejects_duplicate_methods():
    with pytest.raises(ValueError, match="duplicate"):
        CaseMethodComparison(
            case_id="CASE-DEV-003", claim_id="CC3",
            records=(record("B2"), record("B2")),
        )


def test_case_comparison_rejects_cross_case_or_claim_records():
    other = MethodExperimentRecord(
        case_id="CASE-OTHER", claim_id="CC3", method="B4",
        method_version="B4-v1", system_state=EvidenceState.SUPPORTED,
        evidence_ids=(), burden=VerificationBurden(1, 30.0, ("MEDIUM",)),
    )
    with pytest.raises(ValueError, match="same case and claim"):
        CaseMethodComparison(
            case_id="CASE-DEV-003", claim_id="CC3",
            records=(record("B2"), other),
        )
