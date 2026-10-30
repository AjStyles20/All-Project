"""Bounded baseline contracts for later B0-B3 comparative evaluation.

These adapters intentionally expose claim ceilings. They do not implement live news,
LLM retrieval, or empirical scoring yet.
"""
from dataclasses import dataclass

from .enums import OutputClass
from .models import TransitionAssessment
from .progression import ProgressionDecision, evaluate_progression


@dataclass(frozen=True)
class BaselineResult:
    baseline_id: str
    output_class: OutputClass
    rationale: str
    structurally_gated: bool


def run_b0_news_signal(signal_present: bool) -> BaselineResult:
    """B0: news/GPR-like signal has no Nigeria transmission evidence contract."""
    return BaselineResult(
        "B0",
        OutputClass.VERIFIED_EVENT_ONLY if signal_present else OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE,
        "Constructed news-intensity/event signal only; no Nigeria transmission chain.",
        False,
    )


def run_b1_event_exposure(event_verified: bool, exposure_identified: bool) -> BaselineResult:
    """B1: event + direct Nigeria exposure, deliberately no downstream contract."""
    if not event_verified:
        output = OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE
    elif exposure_identified:
        output = OutputClass.EXPOSURE_IDENTIFIED
    else:
        output = OutputClass.VERIFIED_EVENT_ONLY
    return BaselineResult(
        "B1", output,
        "Event/exposure baseline; no domestic-transmission evidence contract.",
        False,
    )


def run_b2_narrative(proposed_output: OutputClass, rationale: str) -> BaselineResult:
    """B2 placeholder: records an ungated narrative claim for later real LLM/RAG adapter."""
    if not rationale.strip():
        raise ValueError("B2 narrative rationale is required")
    return BaselineResult("B2", proposed_output, rationale, False)


def run_b3_etec(assessments: tuple[TransitionAssessment, ...]) -> tuple[BaselineResult, ProgressionDecision]:
    """B3: deterministic ETEC progression over the same frozen case information."""
    decision = evaluate_progression(assessments)
    return (
        BaselineResult(
            "B3", decision.output_class,
            decision.stopping_reason,
            True,
        ),
        decision,
    )
