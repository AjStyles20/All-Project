"""Explainable weakest-link progression for the bounded ETEC implementation."""
from dataclasses import dataclass

from .enums import EdgeState, OutputClass, TransitionClass
from .invariants import ORDER, OUTPUT_AFTER, PASSING_STATES
from .models import TransitionAssessment


@dataclass(frozen=True)
class ProgressionDecision:
    output_class: OutputClass
    passed_transitions: tuple[TransitionClass, ...]
    stopping_transition: TransitionClass | None
    stopping_state: EdgeState | None
    stopping_reason: str
    prohibited_outputs: tuple[OutputClass, ...]


def evaluate_progression(
    assessments: tuple[TransitionAssessment, ...],
) -> ProgressionDecision:
    """Evaluate transitions in order and expose the exact weakest required edge."""
    by_transition: dict[TransitionClass, TransitionAssessment] = {}
    for assessment in assessments:
        if assessment.transition in by_transition:
            raise ValueError(
                f"duplicate assessment for {assessment.transition.value}"
            )
        by_transition[assessment.transition] = assessment

    passed: list[TransitionClass] = []
    output = OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE

    for index, transition in enumerate(ORDER):
        assessment = by_transition.get(transition)
        if assessment is None:
            return _stopped(
                output, passed, transition, None,
                f"Required transition {transition.value} has no assessment.",
                index,
            )

        if assessment.state not in PASSING_STATES:
            return _stopped(
                output, passed, transition, assessment.state,
                assessment.rationale,
                index,
            )

        passed.append(transition)
        output = OUTPUT_AFTER[transition]

    return ProgressionDecision(
        output_class=output,
        passed_transitions=tuple(passed),
        stopping_transition=None,
        stopping_state=None,
        stopping_reason="All required transitions passed.",
        prohibited_outputs=(),
    )


def _stopped(
    output: OutputClass,
    passed: list[TransitionClass],
    transition: TransitionClass,
    state: EdgeState | None,
    reason: str,
    index: int,
) -> ProgressionDecision:
    prohibited = tuple(OUTPUT_AFTER[t] for t in ORDER[index:])
    return ProgressionDecision(
        output_class=output,
        passed_transitions=tuple(passed),
        stopping_transition=transition,
        stopping_state=state,
        stopping_reason=reason,
        prohibited_outputs=prohibited,
    )
