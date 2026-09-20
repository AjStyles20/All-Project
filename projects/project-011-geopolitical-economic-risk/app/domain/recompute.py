"""State-changing evidence updates and deterministic pathway recomputation."""
from dataclasses import dataclass

from .enums import EdgeState, OutputClass, TransitionClass
from .models import TransitionAssessment
from .progression import ProgressionDecision, evaluate_progression


@dataclass(frozen=True)
class AssessmentRevision:
    transition: TransitionClass
    previous_state: EdgeState
    new_state: EdgeState
    reason: str


@dataclass(frozen=True)
class RecomputedPathway:
    before: ProgressionDecision
    after: ProgressionDecision
    revision: AssessmentRevision


def revise_and_recompute(
    assessments: tuple[TransitionAssessment, ...],
    transition: TransitionClass,
    new_state: EdgeState,
    reason: str,
) -> RecomputedPathway:
    if not reason.strip():
        raise ValueError("revision reason is required")

    matches = [a for a in assessments if a.transition is transition]
    if len(matches) != 1:
        raise ValueError("exactly one existing transition assessment is required")

    previous = matches[0]
    before = evaluate_progression(assessments)

    revised = tuple(
        TransitionAssessment(
            case_id=a.case_id,
            transition=a.transition,
            state=new_state if a.transition is transition else a.state,
            evidence_ids=a.evidence_ids,
            rationale=reason if a.transition is transition else a.rationale,
        )
        for a in assessments
    )
    after = evaluate_progression(revised)

    return RecomputedPathway(
        before=before,
        after=after,
        revision=AssessmentRevision(
            transition=transition,
            previous_state=previous.state,
            new_state=new_state,
            reason=reason,
        ),
    )
