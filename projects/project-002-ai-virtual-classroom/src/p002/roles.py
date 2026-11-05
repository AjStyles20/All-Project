"""Role contracts (FR-D). A role may only do what its contract permits, and nothing it
produces can rank above its authority ceiling.

No language model is connected in this version (N06: the kernel works without one). The two
AI roles are deterministic stand-ins that transform text the way a model would be asked to,
so lineage and laundering can be tested. A real provider would plug in behind `generate`.
"""
from dataclasses import dataclass

from p002.domain import Authority, EdgeType, PolicyError


@dataclass(frozen=True)
class RoleContract:
    name: str
    occupant: str          # "ai" or "human"
    purpose: str
    ceiling: Authority
    permissions: frozenset

    @property
    def actor(self):
        return f"{self.occupant}:{self.name}"


EXPLAINER = RoleContract("explainer", "ai", "Rephrase course claims for a learner", Authority.AI_DERIVED,
                         frozenset({"derive"}))
QUIZ_WRITER = RoleContract("quiz-writer", "ai", "Turn claims into practice questions", Authority.AI_DERIVED,
                           frozenset({"derive", "artifact"}))
CURATOR = RoleContract("curator", "human", "Maintain the course sources and claims", Authority.CANONICAL_APPROVED,
                       frozenset({"source", "claim", "derive", "artifact", "promote", "reject", "evidence"}))
ROLES = {r.name: r for r in (EXPLAINER, QUIZ_WRITER, CURATOR)}


def require(role: RoleContract, permission: str):
    if permission not in role.permissions:
        raise PolicyError(f"The {role.name} role may not {permission}.")


def generate(role: RoleContract, kind: str, text: str) -> str:
    """Stand-in for a model call. Output is plain text and is never interpreted as instructions."""
    if kind == "paraphrase":
        return "In other words, " + text
    if kind == "summary":
        return "Key point: " + text.split(",")[0].rstrip(".") + "."
    if kind == "question":
        return f"True or false? {text}"
    raise PolicyError(f"Unknown generation kind {kind}.")


def derive(kernel, role: RoleContract, parent_ids, kind: str, text: str | None = None, edge=EdgeType.PARAPHRASE):
    require(role, "derive")
    parents = [kernel.claims[p] for p in parent_ids]
    out = text if text is not None else generate(role, kind, parents[0].text)
    return kernel.derive(parent_ids, out, edge, role.actor, role.ceiling)
