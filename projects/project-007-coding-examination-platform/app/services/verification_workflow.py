"""Research-critical B4 verification workflow for the first P001 vertical slice."""
from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import EvidenceState, EvidenceType
from app.domain.models import EvidenceItem, EvidenceStateRecord
from app.services.cc3_response_evaluator import (
    CC3ProbeResponse,
    CC3ResponseEvaluator,
)
from app.services.probe_selector import ProbeSelection


@dataclass(frozen=True)
class VerificationUpdate:
    evidence: EvidenceItem
    state_record: EvidenceStateRecord
    control_state: str


class VerificationWorkflow:
    def apply_cc3_response(
        self,
        *,
        case_id: str,
        selection: ProbeSelection,
        response: CC3ProbeResponse,
        evidence_id: str,
        recorded_at: datetime,
        source: str = "B4-v1.0-development",
    ) -> VerificationUpdate:
        if selection.selected_probe is None:
            raise ValueError("Cannot apply a probe response when no probe was selected.")
        if selection.claim_id != "CC3" or selection.gap_type != "EG-T3":
            raise ValueError("This development workflow only handles CC3 / EG-T3.")
        if selection.selected_probe.probe_id != "VP-CC3-02":
            raise ValueError("Only VP-CC3-02 has a frozen structured response rubric.")

        evaluation = CC3ResponseEvaluator().evaluate(response)
        evidence = EvidenceItem(
            evidence_id=evidence_id,
            case_id=case_id,
            evidence_type=EvidenceType.VERIFICATION,
            content=(
                f"input={response.test_input!r}; "
                f"expected={response.expected_result!r}; "
                f"reason={response.usefulness_reason!r}"
            ),
            source_type=selection.selected_probe.probe_id,
            created_at=recorded_at,
        )
        state_record = EvidenceStateRecord(
            case_id=case_id,
            claim_id="CC3",
            state=evaluation.state,
            rationale=evaluation.rationale,
            recorded_at=recorded_at,
            source=source,
        )
        control_state = (
            "VERIFICATION_COMPLETE"
            if evaluation.state is EvidenceState.SUPPORTED
            else "CONTINUE_VERIFICATION"
        )
        return VerificationUpdate(
            evidence=evidence,
            state_record=state_record,
            control_state=control_state,
        )
