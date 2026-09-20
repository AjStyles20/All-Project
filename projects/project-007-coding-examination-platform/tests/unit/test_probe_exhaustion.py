from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector


def test_used_probe_is_not_selected_again():
    result = ProbeSelector().select(
        gap_type="EG-T3", claim_id="CC3", probes=cc3_development_probes(),
        used_probe_ids=frozenset({"VP-CC3-02"}),
    )
    by_id = {d.probe_id: d for d in result.candidate_dispositions}
    assert by_id["VP-CC3-02"].disposition == "REJECTED_ALREADY_USED"
    assert result.selected_probe is not None
    assert result.selected_probe.probe_id == "VP-CC3-03"


def test_exhausted_adequate_probes_require_human_review():
    result = ProbeSelector().select(
        gap_type="EG-T3", claim_id="CC3", probes=cc3_development_probes(),
        used_probe_ids=frozenset({"VP-CC3-02", "VP-CC3-03"}),
    )
    assert result.selected_probe is None
    assert result.decision == "HUMAN_REVIEW_REQUIRED"
