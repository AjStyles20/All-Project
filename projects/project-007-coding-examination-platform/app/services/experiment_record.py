"""Method-level experiment records for P001 comparative evaluation.

System output, verification burden and independent reference judgment are kept
as separate fields so the system cannot grade itself.
"""
from dataclasses import dataclass
from app.domain.enums import EvidenceState
from app.services.verification_burden import VerificationBurden


@dataclass(frozen=True)
class IndependentReferenceJudgment:
    assessor_id: str
    claim_id: str
    state: EvidenceState
    rationale: str
    rubric_version: str


@dataclass(frozen=True)
class MethodExperimentRecord:
    case_id: str
    claim_id: str
    method: str
    method_version: str
    system_state: EvidenceState
    evidence_ids: tuple[str, ...]
    burden: VerificationBurden
    reference: IndependentReferenceJudgment | None = None

    def __post_init__(self):
        if self.reference is not None and self.reference.claim_id != self.claim_id:
            raise ValueError("Reference judgment must concern the same competence claim.")

    @property
    def agrees_with_reference(self) -> bool | None:
        if self.reference is None:
            return None
        return self.system_state is self.reference.state


@dataclass(frozen=True)
class CaseMethodComparison:
    case_id: str
    claim_id: str
    records: tuple[MethodExperimentRecord, ...]

    def __post_init__(self):
        if not self.records:
            raise ValueError("At least one method record is required.")
        if any(r.case_id != self.case_id or r.claim_id != self.claim_id for r in self.records):
            raise ValueError("All records must concern the same case and claim.")
        methods = [r.method for r in self.records]
        if len(methods) != len(set(methods)):
            raise ValueError("A comparison cannot contain duplicate method records.")

    def record_for(self, method: str) -> MethodExperimentRecord:
        for record in self.records:
            if record.method == method:
                return record
        raise KeyError(method)
