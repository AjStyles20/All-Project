"""APLDG trust kernel: sources, claims, derivations, artifacts, and status propagation.

Every authority or status change happens here, in deterministic code (ADR-003). Source text
is stored as data and never interpreted (SEC-R01, SEC-R02). Model or role output can only
create AI_DERIVED claims; promotion needs an explicit human decision backed by trusted
evidence (APLDG-R02, R07).

Storage is in-memory dictionaries with an append-only audit log; `store.py` persists them.
"""
import hashlib
import itertools
from dataclasses import dataclass, field

from p002.domain import (TRUSTED, ArtifactStatus, Authority, ClaimStatus, EdgeType, PolicyError, Relation)


@dataclass
class Source:
    id: str
    title: str
    version: str
    text: str
    authority: Authority
    sha256: str
    superseded_by: str | None = None


@dataclass
class Claim:
    id: str
    text: str
    authority: Authority
    created_by: str
    evidence: list = field(default_factory=list)      # [(source_id, Relation)]
    parents: list = field(default_factory=list)       # [(claim_id, EdgeType, actor)]
    rejected: bool = False


@dataclass
class Artifact:
    id: str
    kind: str
    content: str
    depends_on: list                                   # claim ids


@dataclass(frozen=True)
class Explanation:
    status: ClaimStatus
    authority: Authority
    reasons: tuple
    path: tuple


class TrustKernel:
    def __init__(self, propagate=True):
        # propagate=False is baseline B2: provenance is recorded and shown, but changes in
        # sources do not flow to dependent claims and artifacts.
        self.propagate = propagate
        self.sources, self.claims, self.artifacts = {}, {}, {}
        self.audit = []
        self._ids = {}

    def _id(self, prefix):
        counter = self._ids.setdefault(prefix, itertools.count(1))
        return f"{prefix}{next(counter)}"

    def _log(self, event, obj, reason):
        self.audit.append({"seq": len(self.audit) + 1, "event": event, "object": obj, "reason": reason})

    # ---------- sources ----------

    def add_source(self, title, version, text, authority: Authority) -> Source:
        s = Source(self._id("S"), title, version, text, Authority(authority), hashlib.sha256(text.encode()).hexdigest())
        self.sources[s.id] = s
        self._log("SOURCE_ADDED", s.id, f"{authority.name} {title} {version}")
        return s

    def supersede(self, old_id, new_id):
        old, new = self.sources[old_id], self.sources[new_id]
        if new.authority < old.authority:
            raise PolicyError("A source can only be superseded by one of equal or higher authority.")
        old.superseded_by = new.id
        self._log("SOURCE_SUPERSEDED", old.id, f"replaced by {new.id}")

    # ---------- claims ----------

    def add_claim(self, text, authority: Authority, created_by: str, evidence=()) -> Claim:
        """A claim stated by a person or curated from sources. Its authority is capped by its
        best supporting source; with no evidence it is at most a human assertion."""
        evidence = [(sid, Relation(rel)) for sid, rel in evidence]
        for sid, _ in evidence:
            if sid not in self.sources:
                raise PolicyError(f"Unknown source {sid}.")
        support = [self.sources[s].authority for s, r in evidence if r is Relation.SUPPORTS]
        ceiling = max(support) if support else Authority.HUMAN_ASSERTION
        if created_by.startswith("ai:"):
            ceiling = min(ceiling, Authority.AI_DERIVED)
        c = Claim(self._id("C"), text, Authority(min(authority, ceiling)), created_by, evidence)
        self.claims[c.id] = c
        self._log("CLAIM_ADDED", c.id, f"{c.authority.name} by {created_by}")
        return c

    def derive(self, parent_ids, text, edge: EdgeType, actor: str, actor_ceiling: Authority) -> Claim:
        """A claim made from other claims by a role (AI or human). Authority is the lowest of
        the parents, the actor's ceiling, and AI_DERIVED for AI actors: repetition and
        paraphrase never raise it (APLDG-R02, R03)."""
        if not parent_ids:
            raise PolicyError("A derived claim needs at least one parent.")
        parents = [self.claims[p] for p in parent_ids]
        authority = min([p.authority for p in parents] + [actor_ceiling])
        if actor.startswith("ai:"):
            authority = min(authority, Authority.AI_DERIVED)
        c = Claim(self._id("C"), text, Authority(authority), actor,
                  parents=[(p.id, EdgeType(edge), actor) for p in parents])
        self.claims[c.id] = c
        self._log("CLAIM_DERIVED", c.id, f"{edge.name} of {','.join(parent_ids)} by {actor}")
        return c

    def add_evidence(self, claim_id, source_id, relation: Relation):
        self.claims[claim_id].evidence.append((source_id, Relation(relation)))
        self._log("EVIDENCE_LINKED", claim_id, f"{relation.name} {source_id}")

    def promote(self, claim_id, to: Authority, approver: str, source_id: str):
        """The only way to raise authority: a named human, citing a supporting source of at
        least the target authority (APLDG-R07)."""
        c = self.claims[claim_id]
        if approver.startswith("ai:"):
            raise PolicyError("Only a person can promote a claim.")
        s = self.sources.get(source_id)
        if s is None or (source_id, Relation.SUPPORTS) not in c.evidence or s.authority < to:
            raise PolicyError("Promotion needs a linked supporting source of at least that authority.")
        c.authority = Authority(to)
        self._log("CLAIM_PROMOTED", claim_id, f"to {to.name} by {approver} citing {source_id}")

    def reject(self, claim_id, by: str):
        self.claims[claim_id].rejected = True
        self._log("CLAIM_REJECTED", claim_id, f"by {by}")

    # ---------- artifacts ----------

    def add_artifact(self, kind, content, depends_on) -> Artifact:
        for cid in depends_on:
            if cid not in self.claims:
                raise PolicyError(f"Unknown claim {cid}.")
        a = Artifact(self._id("A"), kind, content, list(depends_on))
        self.artifacts[a.id] = a
        self._log("ARTIFACT_ADDED", a.id, f"{kind} using {','.join(depends_on)}")
        return a

    # ---------- status ----------

    def explain(self, claim_id) -> Explanation:
        """Status of a claim with the reasons and the path that led to it (APLDG-R08)."""
        return self._explain(claim_id, set())

    def _explain(self, claim_id, seen):
        c = self.claims[claim_id]
        if c.rejected:
            return Explanation(ClaimStatus.REJECTED, c.authority, ("rejected by a person",), (claim_id,))
        reasons, path = [], [claim_id]
        trusted_for = [s for s, r in c.evidence if r is Relation.SUPPORTS and self.sources[s].authority in TRUSTED]
        trusted_against = [s for s, r in c.evidence if r is Relation.CONTRADICTS and self.sources[s].authority in TRUSTED]
        status = ClaimStatus.CURRENT if c.authority in TRUSTED else ClaimStatus.UNVERIFIED
        if self.propagate:
            if trusted_for and trusted_against:
                status = ClaimStatus.CONFLICTED
                reasons.append(f"trusted sources disagree: {','.join(trusted_for)} support, {','.join(trusted_against)} contradict")
            elif c.evidence and all(self.sources[s].superseded_by for s, r in c.evidence if r is Relation.SUPPORTS) \
                    and any(r is Relation.SUPPORTS for _, r in c.evidence):
                status = ClaimStatus.STALE
                old = [s for s, r in c.evidence if r is Relation.SUPPORTS]
                reasons.append(f"its sources were superseded: {', '.join(f'{s}->{self.sources[s].superseded_by}' for s in old)}")
            for pid, edge, _ in c.parents:
                if pid in seen:
                    continue
                parent = self._explain(pid, seen | {claim_id})
                if parent.status in (ClaimStatus.CONFLICTED, ClaimStatus.STALE, ClaimStatus.REJECTED):
                    worse = ClaimStatus.CONFLICTED if parent.status is ClaimStatus.CONFLICTED else ClaimStatus.STALE
                    if status in (ClaimStatus.CURRENT, ClaimStatus.UNVERIFIED) or worse is ClaimStatus.CONFLICTED:
                        status = worse
                    reasons.append(f"derived ({edge.name}) from {pid}, which is {parent.status.value}")
                    path.extend(parent.path)
        # The reason that decides the status comes first; the authority note follows.
        if c.authority not in TRUSTED:
            reasons.append(f"authority {c.authority.name}: not from a trusted source")
        if not reasons:
            reasons.append(f"supported by trusted source(s) {', '.join(trusted_for) or '-'}")
        return Explanation(status, c.authority, tuple(reasons), tuple(dict.fromkeys(path)))

    def artifact_status(self, artifact_id) -> tuple[ArtifactStatus, list]:
        a = self.artifacts[artifact_id]
        reasons, worst = [], ArtifactStatus.CURRENT
        rank = [ArtifactStatus.CURRENT, ArtifactStatus.REVIEW_REQUIRED, ArtifactStatus.STALE,
                ArtifactStatus.CONFLICTED, ArtifactStatus.INVALID]
        for cid in a.depends_on:
            e = self.explain(cid)
            mapped = {ClaimStatus.CURRENT: ArtifactStatus.CURRENT, ClaimStatus.UNVERIFIED: ArtifactStatus.REVIEW_REQUIRED,
                      ClaimStatus.STALE: ArtifactStatus.STALE, ClaimStatus.CONFLICTED: ArtifactStatus.CONFLICTED,
                      ClaimStatus.SUPERSEDED: ArtifactStatus.STALE, ClaimStatus.REJECTED: ArtifactStatus.INVALID}[e.status]
            if mapped is not ArtifactStatus.CURRENT:
                reasons.append(f"{cid} is {e.status.value}: {e.reasons[0]}")
            if rank.index(mapped) > rank.index(worst):
                worst = mapped
        return worst, reasons

    def impact_of(self, source_id) -> dict:
        """Claims and artifacts no longer CURRENT after a source change (A08)."""
        claims = [cid for cid in self.claims if self.explain(cid).status not in (ClaimStatus.CURRENT, ClaimStatus.UNVERIFIED)]
        artifacts = [aid for aid in self.artifacts if self.artifact_status(aid)[0] is not ArtifactStatus.CURRENT]
        return {"source": source_id, "claims": claims, "artifacts": artifacts}
