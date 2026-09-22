from datetime import datetime, timezone

import pytest

from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.probe_selector import ProbeSelection, VerificationProbe
from app.services.verification_workflow import VerificationWorkflow


def valid_response():
    return CC3ProbeResponse(
        test_input="[1, 3, 5]",
        expected_result="[]",
        usefulness_reason="Checks the no-even-values boundary.",
        input_relevant=True,
        expected_result_correct=True,
        reason_defensible=True,
    )


def test_response_cannot_be_applied_without_selected_probe():
    selection = ProbeSelection(
        gap_type="EG-T3",
        claim_id="CC3",
        selected_probe=None,
        decision="HUMAN_REVIEW_REQUIRED",
        rationale="No adequate probe.",
    )

    with pytest.raises(ValueError):
        VerificationWorkflow().apply_cc3_response(
            case_id="CASE-DEV-003",
            selection=selection,
            response=valid_response(),
            evidence_id="EV-X",
            recorded_at=datetime.now(timezone.utc),
        )


def test_cc3_workflow_rejects_wrong_claim_or_gap():
    probe = VerificationProbe(
        probe_id="VP-CC3-02",
        name="Bounded independent test design",
        prompt="Provide test, expected result, and reason.",
        probe_type="TEST_DESIGN",
        applicable_claims=frozenset({"CC3"}),
        gap_types=frozenset({"EG-T3"}),
        potentially_sufficient_gap_types=frozenset({"EG-T3"}),
        burden_rank=2,
    )
    selection = ProbeSelection(
        gap_type="EG-T2",
        claim_id="CC2",
        selected_probe=probe,
        decision="CONTINUE_VERIFICATION",
        rationale="Invalid fixture.",
    )

    with pytest.raises(ValueError):
        VerificationWorkflow().apply_cc3_response(
            case_id="CASE-DEV-003",
            selection=selection,
            response=valid_response(),
            evidence_id="EV-X",
            recorded_at=datetime.now(timezone.utc),
        )


def test_cc3_workflow_rejects_probe_without_frozen_rubric():
    probe = VerificationProbe(
        probe_id="VP-CC3-03",
        name="Comprehensive test suite",
        prompt="Design a comprehensive suite.",
        probe_type="TEST_DESIGN",
        applicable_claims=frozenset({"CC3"}),
        gap_types=frozenset({"EG-T3"}),
        potentially_sufficient_gap_types=frozenset({"EG-T3"}),
        burden_rank=3,
    )
    selection = ProbeSelection(
        gap_type="EG-T3",
        claim_id="CC3",
        selected_probe=probe,
        decision="CONTINUE_VERIFICATION",
        rationale="Fixture.",
    )

    with pytest.raises(ValueError):
        VerificationWorkflow().apply_cc3_response(
            case_id="CASE-DEV-003",
            selection=selection,
            response=valid_response(),
            evidence_id="EV-X",
            recorded_at=datetime.now(timezone.utc),
        )
