"""Auditable end-to-end ETEC decision records."""
from dataclasses import dataclass
from datetime import datetime, timezone

from .enums import EdgeState, OutputClass, TransitionClass
from .models import EconomicCase, EvidenceItem, TransitionAssessment
from .progression import ProgressionDecision, evaluate_progression


@dataclass(frozen=True)
class AuditTrace:
    case_id: str
    generated_at: datetime
    evidence_ids: tuple[str, ...]
    passed_transitions: tuple[TransitionClass, ...]
    stopping_transition: TransitionClass | None
    stopping_state: EdgeState | None
    stopping_reason: str
    released_output: OutputClass
    prohibited_outputs: tuple[OutputClass, ...]


def build_audit_trace(
    case: EconomicCase,
    evidence: tuple[EvidenceItem, ...],
    assessments: tuple[TransitionAssessment, ...],
    generated_at: datetime | None = None,
) -> tuple[ProgressionDecision, AuditTrace]:
    decision = evaluate_progression(assessments)
    trace = AuditTrace(
        case_id=case.case_id,
        generated_at=generated_at or datetime.now(timezone.utc),
        evidence_ids=tuple(item.evidence_id for item in evidence),
        passed_transitions=decision.passed_transitions,
        stopping_transition=decision.stopping_transition,
        stopping_state=decision.stopping_state,
        stopping_reason=decision.stopping_reason,
        released_output=decision.output_class,
        prohibited_outputs=decision.prohibited_outputs,
    )
    return decision, trace
