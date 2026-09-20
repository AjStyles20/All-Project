"""Reviewer-response storage and agreement helpers."""
from dataclasses import dataclass
from .claim_review import ClaimJudgment


@dataclass(frozen=True)
class ReviewerResponse:
    claim_id: str
    reviewer_id: str
    judgment: ClaimJudgment
    rationale: str


def raw_agreement(a: tuple[ReviewerResponse, ...], b: tuple[ReviewerResponse, ...]) -> float | None:
    ma = {x.claim_id: x for x in a}
    mb = {x.claim_id: x for x in b}
    shared = sorted(set(ma) & set(mb))
    if not shared:
        return None
    return sum(ma[k].judgment == mb[k].judgment for k in shared) / len(shared)


def cohens_kappa(a: tuple[ReviewerResponse, ...], b: tuple[ReviewerResponse, ...]) -> float | None:
    ma = {x.claim_id: x for x in a}
    mb = {x.claim_id: x for x in b}
    shared = sorted(set(ma) & set(mb))
    if not shared:
        return None
    labels = list(ClaimJudgment)
    n = len(shared)
    po = sum(ma[k].judgment == mb[k].judgment for k in shared) / n
    pa = {label: sum(ma[k].judgment == label for k in shared) / n for label in labels}
    pb = {label: sum(mb[k].judgment == label for k in shared) / n for label in labels}
    pe = sum(pa[label] * pb[label] for label in labels)
    if pe == 1.0:
        return 1.0 if po == 1.0 else None
    return (po - pe) / (1.0 - pe)
