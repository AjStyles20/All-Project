from datetime import datetime, timezone

from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import EvidenceItem
from app.services.evidence_evaluator import EvidenceEvaluator
from app.services.gap_detector import GapDetector


def test_case_dev_003_supplied_tests_lead_to_cc3_gap():
    evidence = [
        EvidenceItem(
            evidence_id="EV-EXEC-003",
            case_id="CASE-DEV-003",
            evidence_type=EvidenceType.EXECUTION,
            content="Examiner-supplied tests passed.",
            source_type="automated_test",
            created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
        )
    ]

    evaluation = EvidenceEvaluator().evaluate("CC3", evidence)
    gap = GapDetector().detect(
        claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
        state=evaluation.state,
    )

    assert evaluation.state is EvidenceState.UNRESOLVED
    assert gap is not None
    assert gap.gap_type == "EG-T3"
