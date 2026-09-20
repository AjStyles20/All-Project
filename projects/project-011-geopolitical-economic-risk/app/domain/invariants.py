"""Deterministic invariants for the first ETEC implementation slice."""
from .enums import EdgeState, OutputClass, TransitionClass
from .models import EconomicCase, EvidenceItem, TransitionAssessment

ORDER = (
    TransitionClass.T1_EVENT_VERIFICATION,
    TransitionClass.T2_EXPOSURE,
    TransitionClass.T3_DOMESTIC_TRANSMISSION,
    TransitionClass.T4_LOCAL_SCENARIO,
    TransitionClass.T5_MODEL_ESTIMATE_ELIGIBILITY,
    TransitionClass.T6_CALIBRATED_FORECAST,
)

PASSING_STATES = {EdgeState.VERIFIED, EdgeState.SUPPORTED}

OUTPUT_AFTER = {
    TransitionClass.T1_EVENT_VERIFICATION: OutputClass.VERIFIED_EVENT_ONLY,
    TransitionClass.T2_EXPOSURE: OutputClass.EXPOSURE_IDENTIFIED,
    TransitionClass.T3_DOMESTIC_TRANSMISSION: OutputClass.TRANSMISSION_SUPPORTED,
    TransitionClass.T4_LOCAL_SCENARIO: OutputClass.MECHANISM_SUPPORTED_SCENARIO,
    TransitionClass.T5_MODEL_ESTIMATE_ELIGIBILITY: OutputClass.MODEL_ESTIMATE,
    TransitionClass.T6_CALIBRATED_FORECAST: OutputClass.CALIBRATED_FORECAST,
}


def validate_evidence(case: EconomicCase, evidence: EvidenceItem) -> None:
    if evidence.case_id != case.case_id:
        raise ValueError("evidence case_id must match economic case")
    if evidence.observed_at > case.information_cutoff:
        raise ValueError("evidence observed after the case information cutoff")
    if not evidence.source_reference.strip():
        raise ValueError("source_reference is required")
    if not evidence.data_vintage.strip():
        raise ValueError("data_vintage is required")
    if not evidence.geography.strip():
        raise ValueError("geography is required")


def validate_assessment(case: EconomicCase, assessment: TransitionAssessment) -> None:
    if assessment.case_id != case.case_id:
        raise ValueError("assessment case_id must match economic case")
    if not assessment.rationale.strip():
        raise ValueError("transition rationale is required")


def weakest_link_output(assessments: tuple[TransitionAssessment, ...]) -> OutputClass:
    by_transition = {a.transition: a for a in assessments}
    strongest = OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE
    for transition in ORDER:
        assessment = by_transition.get(transition)
        if assessment is None or assessment.state not in PASSING_STATES:
            return strongest
        strongest = OUTPUT_AFTER[transition]
    return strongest
