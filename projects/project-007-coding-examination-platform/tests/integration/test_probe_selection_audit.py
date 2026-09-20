from app.domain.models import ProgrammingCase
from app.persistence.database import Database
from app.persistence.probe_audit_repository import ProbeAuditRepository
from app.persistence.repositories import P001Repository
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector


def test_cc3_selection_persists_why_each_candidate_was_selected_or_rejected(tmp_path):
    db = Database(tmp_path / "probe-audit.db")
    db.initialize()
    P001Repository(db).add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even numbers",
        task_description="Return even numbers.", language="python",
    ))

    selection = ProbeSelector().select(
        gap_type="EG-T3", claim_id="CC3", probes=cc3_development_probes()
    )
    assert selection.selected_probe is not None
    assert selection.selected_probe.probe_id == "VP-CC3-02"

    repo = ProbeAuditRepository(db)
    repo.append_selection_candidates(
        event_id="AUD-003-03", case_id="CASE-DEV-003",
        claim_id="CC3", gap_type="EG-T3",
        candidates=selection.candidate_dispositions,
    )
    stored = repo.list_for_event("AUD-003-03")
    by_probe = {item.disposition.probe_id: item.disposition for item in stored}

    assert by_probe["VP-CC3-01"].disposition == "REJECTED_INSUFFICIENT"
    assert by_probe["VP-CC3-01"].admissible is True
    assert by_probe["VP-CC3-01"].potentially_sufficient is False

    assert by_probe["VP-CC3-02"].disposition == "SELECTED"
    assert by_probe["VP-CC3-02"].burden_rank == 2

    assert by_probe["VP-CC3-03"].disposition == "REJECTED_HIGHER_BURDEN"
    assert by_probe["VP-CC3-03"].potentially_sufficient is True
    assert by_probe["VP-CC3-03"].burden_rank == 3
