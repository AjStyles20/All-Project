"""Candidate A same-information baseline fixture.

This freezes baseline inputs, not an empirical finding of baseline superiority.
"""
from app.domain.baselines import run_b0_news_signal, run_b1_event_exposure, run_b2_narrative, run_b3_etec
from app.domain.enums import EdgeState, OutputClass, TransitionClass
from app.domain.models import TransitionAssessment

CASE_ID = "P003-RU-WHEAT-A"

CANDIDATE_A_ASSESSMENTS = (
    TransitionAssessment(CASE_ID, TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED, ("A-T1",), "Event anchor verified."),
    TransitionAssessment(CASE_ID, TransitionClass.T2_EXPOSURE, EdgeState.SUPPORTED, ("A-T2",), "R2 retrospective wheat exposure supported."),
    TransitionAssessment(CASE_ID, TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED, ("A-T3",), "Wheat-milling-flour/bread pathway supported with counterchannels retained."),
    TransitionAssessment(CASE_ID, TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED, ("A-T4",), "Conditional upward-pressure scenario over the frozen 3-6 month window."),
)

def candidate_a_baselines():
    b0 = run_b0_news_signal(True)
    b1 = run_b1_event_exposure(True, True)
    # B2 is a frozen *placeholder claim form*, not output from a real LLM/RAG run.
    b2 = run_b2_narrative(
        OutputClass.MECHANISM_SUPPORTED_SCENARIO,
        "Given the disruption, Nigeria's wheat exposure implies upward pressure on bread/cereal costs.",
    )
    b3, decision = run_b3_etec(CANDIDATE_A_ASSESSMENTS)
    return (b0, b1, b2, b3), decision
