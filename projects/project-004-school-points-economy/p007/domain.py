"""P007 data model (Pass 004 §10). Identifiers are pseudonymous; no protected attributes are stored.

`group` is a neutral comparison label (for example a class or cohort) used for disparity checks.
"""
from dataclasses import dataclass, field
from enum import Enum


class Action(str, Enum):
    EARN = "EARN"
    REDEEM = "REDEEM"
    REVERSE = "REVERSE"


@dataclass(frozen=True)
class RewardPolicy:
    policy_id: str
    version: int
    name: str
    category: str
    earning_rule: str
    intended_objective: str
    points_per_award: int
    # The quantity the objective is about (e.g. pages read). None when the policy has none.
    objective_measure: str | None = None


@dataclass(frozen=True)
class StudentContext:
    student_id: str
    group: str
    # Eligible earning opportunities per (policy_id, issuer_id). None means the count is unknown.
    opportunities: dict = field(default_factory=dict)


@dataclass(frozen=True)
class IssuerContext:
    issuer_id: str
    role: str
    policy_scope: frozenset


@dataclass(frozen=True)
class RewardTransaction:
    transaction_id: str
    student_id: str
    issuer_id: str | None
    policy_id: str | None
    policy_version: int | None
    action: Action
    category: str
    amount: int
    reason_code: str
    timestamp: int
    measure: float | None = None


@dataclass(frozen=True)
class RewardItem:
    reward_id: str
    name: str
    point_cost: int
    stock: int


@dataclass(frozen=True)
class Dataset:
    """Everything an audit may read. Never contains benchmark ground truth."""
    policies: dict
    students: list
    issuers: list
    transactions: list
    catalogue: list
