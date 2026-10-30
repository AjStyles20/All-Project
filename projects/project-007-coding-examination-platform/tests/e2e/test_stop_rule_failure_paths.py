from app.domain.enums import ClaimApplicability, EvidenceState
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector
from app.services.stop_rule import ClaimControlInput, StopRule


def test_negative_control_all_required_supported_asks_zero_targeted_probes():
    claims = [
        ClaimControlInput("CC1", ClaimApplicability.REQUIRED, EvidenceState.SUPPORTED, False),
        ClaimControlInput("CC3", ClaimApplicability.REQUIRED, EvidenceState.SUPPORTED, False),
        ClaimControlInput("CC4", ClaimApplicability.NOT_APPLICABLE, EvidenceState.UNRESOLVED, False),
    ]

    decision = StopRule().decide(claims)

    assert decision.decision == "VERIFICATION_COMPLETE"
    assert decision.blocking_claim_ids == ()


def test_unresolved_claim_with_all_adequate_probes_exhausted_escalates():
    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=cc3_development_probes(),
        used_probe_ids=frozenset({"VP-CC3-02", "VP-CC3-03"}),
    )
    assert selection.selected_probe is None
    assert selection.decision == "HUMAN_REVIEW_REQUIRED"

    decision = StopRule().decide([
        ClaimControlInput(
            "CC3", ClaimApplicability.REQUIRED, EvidenceState.UNRESOLVED,
            has_adequate_unused_probe=False,
        )
    ])
    assert decision.decision == "HUMAN_REVIEW_REQUIRED"
    assert decision.blocking_claim_ids == ("CC3",)


def test_contradiction_escalates_without_becoming_misconduct_verdict():
    decision = StopRule().decide([
        ClaimControlInput(
            "CC3", ClaimApplicability.REQUIRED, EvidenceState.CONTRADICTED,
            has_adequate_unused_probe=True,
        )
    ])

    assert decision.decision == "HUMAN_REVIEW_REQUIRED"
    assert "misconduct" not in decision.decision.lower()
