from datetime import datetime, timezone

from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import (
    CaseClaim,
    ClaimEvidenceLink,
    CompetenceClaim,
    EvidenceItem,
    EvidenceStateRecord,
    ProgrammingCase,
)
from app.persistence.database import Database
from app.persistence.repositories import P001Repository
from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.evidence_evaluator import EvidenceEvaluator
from app.services.gap_detector import GapDetector
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector
from app.services.verification_workflow import VerificationWorkflow


def test_case_dev_003_persists_unresolved_to_supported_history(tmp_path):
    database = Database(tmp_path / "p001-e2e.db")
    database.initialize()
    repository = P001Repository(database)

    repository.add_case(
        ProgrammingCase(
            case_id="CASE-DEV-003",
            title="Find even numbers",
            task_description="Return the even numbers in a list.",
            language="python",
        )
    )
    repository.add_claim(
        CompetenceClaim(
            claim_id="CC3",
            name="Test Design",
            definition="Independently design relevant tests and justify them.",
        )
    )
    repository.add_case_claim(
        CaseClaim(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            applicability=ClaimApplicability.REQUIRED,
        )
    )

    supplied_test_evidence = EvidenceItem(
        evidence_id="EV-EXEC-003",
        case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Examiner-supplied tests passed.",
        source_type="automated_test",
        created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
    )
    repository.add_evidence(supplied_test_evidence)
    repository.link_evidence(
        ClaimEvidenceLink(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            evidence_id="EV-EXEC-003",
            rationale="Execution evidence is relevant but does not establish independent test design.",
        )
    )

    initial = EvidenceEvaluator().evaluate(
        "CC3", repository.get_evidence_for_claim("CASE-DEV-003", "CC3")
    )
    assert initial.state is EvidenceState.UNRESOLVED
    repository.append_evidence_state(
        EvidenceStateRecord(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            state=initial.state,
            rationale=initial.rationale,
            recorded_at=datetime(2026, 9, 20, 9, 1, tzinfo=timezone.utc),
            source="B4-v1.0-development",
        )
    )

    gap = GapDetector().detect(
        claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
        state=initial.state,
    )
    assert gap is not None

    selection = ProbeSelector().select(
        gap_type=gap.gap_type,
        claim_id=gap.claim_id,
        probes=cc3_development_probes(),
    )
    assert selection.selected_probe is not None
    assert selection.selected_probe.probe_id == "VP-CC3-02"

    update = VerificationWorkflow().apply_cc3_response(
        case_id="CASE-DEV-003",
        selection=selection,
        response=CC3ProbeResponse(
            test_input="[1, 3, 5]",
            expected_result="[]",
            usefulness_reason="Checks behavior when there are no even values.",
            input_relevant=True,
            expected_result_correct=True,
            reason_defensible=True,
        ),
        evidence_id="EV-VERIFY-003-01",
        recorded_at=datetime(2026, 9, 20, 9, 10, tzinfo=timezone.utc),
    )

    repository.add_evidence(update.evidence)
    repository.link_evidence(
        ClaimEvidenceLink(
            case_id="CASE-DEV-003",
            claim_id="CC3",
            evidence_id=update.evidence.evidence_id,
            rationale="Targeted independent verification evidence for EG-T3.",
        )
    )
    repository.append_evidence_state(update.state_record)

    history = repository.list_evidence_states("CASE-DEV-003", "CC3")
    assert [record.state for record in history] == [
        EvidenceState.UNRESOLVED,
        EvidenceState.SUPPORTED,
    ]
    assert update.control_state == "VERIFICATION_COMPLETE"

    stored_evidence = repository.get_evidence_for_claim("CASE-DEV-003", "CC3")
    assert [item.evidence_id for item in stored_evidence] == [
        "EV-EXEC-003",
        "EV-VERIFY-003-01",
    ]
