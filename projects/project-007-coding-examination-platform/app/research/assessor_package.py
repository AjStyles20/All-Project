from dataclasses import dataclass
from app.research.pilot_cases import PilotCaseBundle

@dataclass(frozen=True)
class AssessorEvidenceView:
    evidence_id: str
    evidence_type: str
    content: str
    source_type: str

@dataclass(frozen=True)
class AssessorPackage:
    case_id: str
    case_version: str
    task_description: str
    claim_id: str
    claim_name: str
    claim_definition: str
    claim_version: str
    corpus_version: str
    evidence: tuple[AssessorEvidenceView, ...]

def build_assessor_package(bundle: PilotCaseBundle) -> AssessorPackage:
    return AssessorPackage(bundle.case.case_id, bundle.case.version, bundle.case.task_description, bundle.claim.claim_id, bundle.claim.name, bundle.claim.definition, bundle.claim.version, bundle.corpus_version, tuple(AssessorEvidenceView(item.evidence_id, item.evidence_type.value, item.content, item.source_type) for item in bundle.evidence))
