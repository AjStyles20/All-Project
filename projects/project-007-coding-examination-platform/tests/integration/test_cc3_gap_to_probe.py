from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector


def test_case_dev_003_gap_selects_bounded_sufficient_probe():
    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=cc3_development_probes(),
    )

    assert selection.decision == "CONTINUE_VERIFICATION"
    assert selection.selected_probe is not None
    assert selection.selected_probe.probe_id == "VP-CC3-02"
    assert "lowest-burden" in selection.rationale
