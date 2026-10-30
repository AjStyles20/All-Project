"""Frozen reviewer package/export primitives for P003 M9."""
from dataclasses import dataclass
from hashlib import sha256
import json
from .blinded_review import BlindedClaim
from .claim_review import ClaimJudgment


@dataclass(frozen=True)
class ReviewerPackage:
    package_id: str
    protocol_version: str
    case_id: str
    evidence_packet_id: str
    evidence_packet_hash: str
    claims: tuple[BlindedClaim, ...]
    instructions: str


@dataclass(frozen=True)
class ReviewerSubmission:
    package_id: str
    reviewer_id: str
    responses: tuple[tuple[str, ClaimJudgment, str], ...]


def reviewer_package_hash(package: ReviewerPackage) -> str:
    payload={
        "package_id":package.package_id,
        "protocol_version":package.protocol_version,
        "case_id":package.case_id,
        "evidence_packet_id":package.evidence_packet_id,
        "evidence_packet_hash":package.evidence_packet_hash,
        "claims":[{"blind_id":c.blind_id,"claim_text":c.claim_text,"claim_type":c.claim_type} for c in package.claims],
        "instructions":package.instructions,
    }
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


def validate_submission(package: ReviewerPackage, submission: ReviewerSubmission) -> None:
    if submission.package_id != package.package_id:
        raise ValueError("Submission targets the wrong reviewer package.")
    expected={c.blind_id for c in package.claims}
    received=[x[0] for x in submission.responses]
    if len(received)!=len(set(received)):
        raise ValueError("Duplicate blinded claim response.")
    if set(received)!=expected:
        raise ValueError("Reviewer must respond to exactly the frozen blinded claim set.")
    if not submission.reviewer_id.strip():
        raise ValueError("Reviewer identity is required.")
    if any(not rationale.strip() for _,_,rationale in submission.responses):
        raise ValueError("A rationale is required for every judgment.")
