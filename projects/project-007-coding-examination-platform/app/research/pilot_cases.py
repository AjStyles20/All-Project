"""Versioned constructed pilot fixtures for M8 dry runs.

These fixtures are research instruments, not observations from real students.
"""
from dataclasses import dataclass
from datetime import datetime, timezone

from app.domain.enums import ClaimApplicability, EvidenceType
from app.domain.models import (
    CaseClaim, ClaimEvidenceLink, CompetenceClaim, EvidenceItem, ProgrammingCase,
)


PILOT_CORPUS_VERSION = "PILOT-CC3-v1-candidate"
CC3_VERSION = "CC3-pilot-v1"


@dataclass(frozen=True)
class PilotCaseBundle:
    case: ProgrammingCase
    claim: CompetenceClaim
    case_claim: CaseClaim
    evidence: tuple[EvidenceItem, ...]
    links: tuple[ClaimEvidenceLink, ...]
    corpus_version: str
    construction_expectation: str


def _time() -> datetime:
    # Fixed provenance time keeps constructed fixtures deterministic.
    return datetime(2026, 9, 20, 12, 0, tzinfo=timezone.utc)


def case_pilot_001() -> PilotCaseBundle:
    case = ProgrammingCase(
        "CASE-PILOT-001",
        "count_even: supplied tests without independent test design",
        "Implement count_even(values), returning the number of even integers.",
        "Python",
        "1.0",
    )
    claim = CompetenceClaim(
        "CC3", "Test Design", "Design appropriate tests independently.", CC3_VERSION
    )
    evidence = (
        EvidenceItem(
            "P001-EV-A1", case.case_id, EvidenceType.ARTIFACT,
            "def count_even(values):\\n    count = 0\\n    for value in values:\\n        if value % 2 == 0:\\n            count += 1\\n    return count",
            "constructed_pilot_artifact", _time(),
        ),
        EvidenceItem(
            "P001-EV-X1", case.case_id, EvidenceType.EXECUTION,
            "Examiner-supplied execution record: [1, 2, 3, 4] -> 2 PASS; [2, 4, 6] -> 3 PASS; [1, 3, 5] -> 0 PASS.",
            "constructed_reference_execution", _time(),
        ),
    )
    links = tuple(
        ClaimEvidenceLink(
            case.case_id, claim.claim_id, item.evidence_id,
            "Included as admissible initial CC3 case evidence; supplied tests do not by themselves establish independent test design.",
        )
        for item in evidence
    )
    return PilotCaseBundle(
        case, claim, CaseClaim(case.case_id, claim.claim_id, ClaimApplicability.REQUIRED),
        evidence, links, PILOT_CORPUS_VERSION, "UNRESOLVED development expectation; not ground truth.",
    )


def case_pilot_003() -> PilotCaseBundle:
    case = ProgrammingCase(
        "CASE-PILOT-003",
        "count_even: incomplete independent test-design evidence",
        "Assess a frozen independent test-design response for count_even(values).",
        "Python",
        "1.0",
    )
    claim = CompetenceClaim(
        "CC3", "Test Design", "Design appropriate tests independently.", CC3_VERSION
    )
    evidence = (
        EvidenceItem(
            "P003-EV-V1", case.case_id, EvidenceType.VERIFICATION,
            "Frozen constructed response: Input: [2, 3]. Expected output: 2. Reason: this checks that the function can handle both an even and an odd number.",
            "constructed_independent_response", _time(),
        ),
    )
    links = (
        ClaimEvidenceLink(
            case.case_id, claim.claim_id, "P003-EV-V1",
            "Constructed independent response for testing PARTIAL versus UNRESOLVED rubric clarity.",
        ),
    )
    return PilotCaseBundle(
        case, claim, CaseClaim(case.case_id, claim.claim_id, ClaimApplicability.REQUIRED),
        evidence, links, PILOT_CORPUS_VERSION, "PARTIAL development expectation; assessor may disagree.",
    )


def load_bundle(repository, bundle: PilotCaseBundle) -> None:
    repository.add_case(bundle.case)
    repository.add_claim(bundle.claim)
    repository.add_case_claim(bundle.case_claim)
    for item in bundle.evidence:
        repository.add_evidence(item)
    for link in bundle.links:
        repository.link_evidence(link)
