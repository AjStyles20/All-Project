from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector, VerificationProbe


def test_selector_rejects_cheaper_but_insufficient_probe():
    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=cc3_development_probes(),
    )

    assert selection.selected_probe is not None
    assert selection.selected_probe.probe_id == "VP-CC3-02"
    assert selection.selected_probe.probe_id != "VP-CC3-01"


def test_selector_prefers_lower_burden_between_sufficient_probes():
    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=cc3_development_probes(),
    )

    assert selection.selected_probe is not None
    assert selection.selected_probe.burden_rank == 2
    assert selection.selected_probe.probe_id != "VP-CC3-03"


def test_no_adequate_probe_requires_human_review():
    inadequate = VerificationProbe(
        probe_id="VP-X",
        name="Inadequate",
        prompt="Give an input.",
        probe_type="TEST_DESIGN",
        applicable_claims=frozenset({"CC3"}),
        gap_types=frozenset({"EG-T3"}),
        potentially_sufficient_gap_types=frozenset(),
        burden_rank=1,
    )

    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=[inadequate],
    )

    assert selection.selected_probe is None
    assert selection.decision == "HUMAN_REVIEW_REQUIRED"


def test_irrelevant_probe_is_not_admissible():
    irrelevant = VerificationProbe(
        probe_id="VP-CC2",
        name="Trace execution",
        prompt="Trace this program.",
        probe_type="TRACE",
        applicable_claims=frozenset({"CC2"}),
        gap_types=frozenset({"EG-T2"}),
        potentially_sufficient_gap_types=frozenset({"EG-T2"}),
        burden_rank=1,
    )

    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=[irrelevant],
    )

    assert selection.decision == "HUMAN_REVIEW_REQUIRED"
