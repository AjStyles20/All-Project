"""Frozen constructed F1 missing-link fixture."""
from datetime import datetime, timezone

from app.domain.enums import EdgeState, SourceAuthorityTier, TransitionClass
from app.domain.models import EconomicCase, EvidenceItem, TransitionAssessment

CUT = datetime(2026, 1, 1, tzinfo=timezone.utc)

CASE_F1_001 = EconomicCase(
    case_id="CASE-F1-001",
    target_country="Nigeria",
    event_type="constructed_export_restriction",
    information_cutoff=CUT,
    version="F1-v1",
)

F1_EVIDENCE = (
    EvidenceItem(
        evidence_id="EV-F1-EVENT",
        case_id=CASE_F1_001.case_id,
        transition=TransitionClass.T1_EVENT_VERIFICATION,
        authority_tier=SourceAuthorityTier.OFFICIAL_PRIMARY,
        source_reference="constructed://official-event-fixture",
        observed_at=datetime(2025, 12, 1, tzinfo=timezone.utc),
        data_vintage="F1-v1",
        geography="source-country",
        content_hash="constructed-event-hash",
    ),
    EvidenceItem(
        evidence_id="EV-F1-EXPOSURE",
        case_id=CASE_F1_001.case_id,
        transition=TransitionClass.T2_EXPOSURE,
        authority_tier=SourceAuthorityTier.STATISTICAL_INSTITUTION,
        source_reference="constructed://nigeria-exposure-fixture",
        observed_at=datetime(2025, 12, 15, tzinfo=timezone.utc),
        data_vintage="F1-v1",
        geography="Nigeria",
        economic_identifier="HS-CONSTRUCTED-001",
        classification_version="constructed-hs",
        content_hash="constructed-exposure-hash",
    ),
)

F1_ASSESSMENTS = (
    TransitionAssessment(
        CASE_F1_001.case_id,
        TransitionClass.T1_EVENT_VERIFICATION,
        EdgeState.VERIFIED,
        ("EV-F1-EVENT",),
        "Constructed authoritative event fixture is present.",
    ),
    TransitionAssessment(
        CASE_F1_001.case_id,
        TransitionClass.T2_EXPOSURE,
        EdgeState.VERIFIED,
        ("EV-F1-EXPOSURE",),
        "Constructed Nigeria exposure fixture is present.",
    ),
    TransitionAssessment(
        CASE_F1_001.case_id,
        TransitionClass.T3_DOMESTIC_TRANSMISSION,
        EdgeState.INSUFFICIENT,
        (),
        "No admissible product-to-sector mapping is present.",
    ),
)
