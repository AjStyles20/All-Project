from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector


def test_potentially_sufficient_but_unexecutable_probe_is_not_adequate():
    probes=cc3_development_probes()
    vp3=next(p for p in probes if p.probe_id=="VP-CC3-03")
    assert vp3.potentially_sufficient_gap_types==frozenset({"EG-T3"})
    assert vp3.executable is False

    selection=ProbeSelector().select(
        gap_type="EG-T3",claim_id="CC3",probes=probes,
        used_probe_ids=frozenset({"VP-CC3-02"}),
    )
    assert selection.selected_probe is None
    assert selection.decision=="HUMAN_REVIEW_REQUIRED"
    dispositions={d.probe_id:d.disposition for d in selection.candidate_dispositions}
    assert dispositions["VP-CC3-03"]=="REJECTED_NOT_EXECUTABLE"


def test_frozen_vp_cc3_02_remains_executable_and_selected():
    probes=cc3_development_probes()
    vp2=next(p for p in probes if p.probe_id=="VP-CC3-02")
    assert vp2.executable is True
    selection=ProbeSelector().select(gap_type="EG-T3",claim_id="CC3",probes=probes)
    assert selection.selected_probe.probe_id=="VP-CC3-02"
