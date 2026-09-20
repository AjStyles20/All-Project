from datetime import datetime, timezone

import pytest

from app.domain.enums import EvidenceType
from app.domain.models import EvidenceItem
from app.services.baseline_experiment_runner import BaselineExperimentRunner


def ev(evidence_id, evidence_type, case_id="CASE-DEV-003"):
    return EvidenceItem(
        evidence_id=evidence_id, case_id=case_id,
        evidence_type=evidence_type, content=evidence_id,
        source_type="experiment-fixture", created_at=datetime.now(timezone.utc),
    )


def test_runner_uses_same_case_evidence_but_preserves_method_boundaries():
    evidence = [
        ev("EV-A", EvidenceType.ARTIFACT),
        ev("EV-X", EvidenceType.EXECUTION),
        ev("EV-R", EvidenceType.RUBRIC),
        ev("EV-P", EvidenceType.PROCESS),
        ev("EV-V", EvidenceType.VERIFICATION),
        ev("EV-C", EvidenceType.POLICY_CONTEXT),
    ]

    experiment = BaselineExperimentRunner().run(
        case_id="CASE-DEV-003", claim_id="CC3", evidence=evidence,
    )

    assert tuple(r.method for r in experiment.results) == ("B0", "B1", "B2", "B3")
    assert experiment.by_method("B0").evidence_ids == ("EV-A", "EV-X", "EV-R")
    assert experiment.by_method("B1").evidence_ids == ("EV-A", "EV-X", "EV-R", "EV-P")
    assert experiment.by_method("B2").evidence_ids == (
        "EV-A", "EV-X", "EV-R", "EV-P", "EV-V"
    )
    assert experiment.by_method("B3").evidence_ids == (
        "EV-A", "EV-X", "EV-R", "EV-P"
    )


def test_runner_rejects_cross_case_evidence_contamination():
    evidence = [
        ev("EV-A", EvidenceType.ARTIFACT),
        ev("EV-OTHER", EvidenceType.PROCESS, case_id="CASE-OTHER"),
    ]

    with pytest.raises(ValueError, match="experiment case"):
        BaselineExperimentRunner().run(
            case_id="CASE-DEV-003", claim_id="CC3", evidence=evidence,
        )


def test_unknown_method_lookup_fails_explicitly():
    experiment = BaselineExperimentRunner().run(
        case_id="CASE-DEV-003", claim_id="CC3",
        evidence=[ev("EV-A", EvidenceType.ARTIFACT)],
    )
    with pytest.raises(KeyError):
        experiment.by_method("B9")
