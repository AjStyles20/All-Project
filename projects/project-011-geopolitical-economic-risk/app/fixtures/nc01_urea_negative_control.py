"""NC-01 R2 negative-control fixture.

Constructed from the frozen retrospective research packet. This fixture tests
the narrow direct-Russian-urea-dependence pathway only.
"""
from app.domain.enums import EdgeState, OutputClass, TransitionClass
from app.domain.models import TransitionAssessment
from app.domain.baselines import run_b0_news_signal, run_b1_event_exposure, run_b2_narrative, run_b3_etec

CASE_ID = "P003-NC01-RU-UREA"
REPLAY_MODE = "R2"

ASSESSMENTS = (
    TransitionAssessment(CASE_ID, TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED, ("NC01-T1",), "24-Feb-2022 event boundary verified."),
    TransitionAssessment(CASE_ID, TransitionClass.T2_EXPOSURE, EdgeState.INSUFFICIENT, ("NC01-T2",), "Direct Russia-to-Nigeria HS310210 exposure is non-zero but negligible for a material direct-dependence warning."),
)

def nc01_baselines():
    b0 = run_b0_news_signal(True)
    # B1 receives event plus the exposure screen; it must not convert negligible
    # direct exposure into a material local exposure claim.
    b1 = run_b1_event_exposure(True, False)
    # Placeholder only: a deliberately tempting narrative claim used to test the
    # comparison pipeline. It is NOT a real LLM/RAG generation.
    b2 = run_b2_narrative(
        OutputClass.MECHANISM_SUPPORTED_SCENARIO,
        "Russia's fertilizer shock creates a material Nigerian urea risk because Nigeria depends on Russian urea imports.",
    )
    b3, decision = run_b3_etec(ASSESSMENTS)
    return (b0, b1, b2, b3), decision
