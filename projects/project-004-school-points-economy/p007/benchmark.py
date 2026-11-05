"""Synthetic school reward economies with injected, labelled conditions (Pass 004 §11).

Written independently of the audit engines: nothing here imports p007.audit, and the
ground truth is returned separately from the Dataset the engines see (§12, §16).

Every student has an individual "engagement" drawn independently of their group, so groups
differ only where a scenario injects a difference.
"""
import random
from dataclasses import dataclass, field

from p007.domain import (Action, Dataset, IssuerContext, RewardItem, RewardPolicy,
                         RewardTransaction, StudentContext)

SCENARIOS = ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8")

SCENARIO_NAMES = {
    "S0": "Normal heterogeneous operation",
    "S1": "Unequal earning opportunity",
    "S2": "Systematic issuer disparity",
    "S3": "Legitimate high issuance",
    "S4": "Proxy / incentive gaming",
    "S5": "Category concentration",
    "S6": "Missing context",
    "S7": "Economy imbalance",
    "S8": "Multi-condition (S2 + S4)",
}

POLICIES = {
    "READ": RewardPolicy("READ", 1, "Reading log", "READING", "10 points per completed book",
                         "Read substantially more", 10, "pages"),
    "PART": RewardPolicy("PART", 1, "Class participation", "PARTICIPATION", "2 points per contribution",
                         "Contribute in class", 2),
    "SERV": RewardPolicy("SERV", 1, "Community service", "SERVICE", "15 points per session",
                         "Take part in school service", 15),
}
ISSUER_SCOPE = {"T1": {"READ", "PART"}, "T2": {"READ", "PART"}, "T3": {"PART", "SERV"}, "T4": {"PART", "SERV"}}
BASE_OPPORTUNITIES = {"READ": 6, "PART": 10, "SERV": 3}
BASE_RATE = {"READ": 0.55, "PART": 0.6, "SERV": 0.6}


@dataclass(frozen=True)
class Truth:
    scenario: str
    # Injected conditions a reviewer should be shown, by kind.
    conditions: frozenset = field(default_factory=frozenset)
    # True when the scenario is deliberately underdetermined (S6).
    expect_insufficient: bool = False


@dataclass
class Config:
    students_per_group: int = 30
    groups: tuple = ("A", "B")


def generate(scenario: str, seed: int, config: Config | None = None) -> tuple[Dataset, Truth]:
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario {scenario}")
    config = config or Config()
    rng = random.Random(f"{scenario}:{seed}")

    two = scenario in ("S2", "S8")
    gaming = scenario in ("S4", "S8")

    students = []
    engagement = {}
    for group in config.groups:
        for n in range(config.students_per_group):
            sid = f"{group}{n:03d}"
            students.append((sid, group))
            engagement[sid] = rng.uniform(0.65, 1.35)
    gamers = set(rng.sample([s for s, _ in students], k=len(students) // 4)) if gaming else set()
    generosity = {i: rng.uniform(0.85, 1.15) for i in ISSUER_SCOPE}

    contexts, transactions = [], []
    clock = 0

    def award(sid, issuer, policy_id, measure=None):
        nonlocal clock
        clock += rng.randint(1, 30)
        policy = POLICIES[policy_id]
        transactions.append(RewardTransaction(
            f"t{len(transactions):06d}", sid, issuer, policy_id, policy.version, Action.EARN,
            policy.category, policy.points_per_award, "AWARD", clock, measure))

    for sid, group in students:
        opps = {}
        for issuer, scope in ISSUER_SCOPE.items():
            for policy_id in sorted(scope):
                base = BASE_OPPORTUNITIES[policy_id]
                count = max(0, base + rng.randint(-1, 1))
                rate = min(0.95, BASE_RATE[policy_id] * engagement[sid] * generosity[issuer])
                if scenario in ("S1", "S6") and policy_id == "PART" and group == "B":
                    count = count // 2
                if scenario == "S3" and issuer == "T3" and policy_id == "PART":
                    count *= 4
                if scenario == "S5" and policy_id == "SERV":
                    count = count * 6 if group == "A" else 0
                if two and issuer == "T2" and policy_id == "PART" and group == "B":
                    rate *= 0.5
                is_gamer = sid in gamers and policy_id == "READ"
                if is_gamer:
                    count *= 3
                    rate = 0.95
                opps[(policy_id, issuer)] = count
                for _ in range(count):
                    if rng.random() < rate:
                        pages = None
                        if policy_id == "READ":
                            pages = rng.uniform(10, 30) if is_gamer else max(40.0, rng.gauss(220, 60))
                        award(sid, issuer, policy_id, pages)
        if scenario == "S6":
            # The opportunity records were never collected.
            opps = {key: None for key in opps}
        contexts.append(StudentContext(sid, group, opps))

    rng.shuffle(transactions)
    transactions.sort(key=lambda t: t.timestamp)

    issued = sum(t.amount for t in transactions)
    catalogue, redemptions = _economy(rng, issued, starved=scenario == "S7")
    for n, (sid, cost) in enumerate(_redeemers(rng, transactions, redemptions)):
        clock += 1
        transactions.append(RewardTransaction(f"r{n:06d}", sid, None, None, None, Action.REDEEM,
                                              "REDEMPTION", -cost, "REWARD", clock))

    dataset = Dataset(dict(POLICIES), contexts,
                      [IssuerContext(i, "TEACHER", frozenset(s)) for i, s in ISSUER_SCOPE.items()],
                      transactions, catalogue)
    return dataset, _truth(scenario)


def _economy(rng, issued, starved):
    """A catalogue whose remaining capacity normally exceeds outstanding points.
    S7: little stock, few redemptions, so points pile up with nothing to spend them on."""
    capacity_share, redeem_share = (0.15, 0.02) if starved else (rng.uniform(1.2, 1.6), rng.uniform(0.3, 0.5))
    items = [("R1", "Homework pass", 50), ("R2", "Library prize", 120), ("R3", "Trip voucher", 400)]
    catalogue = []
    for reward_id, name, cost in items:
        stock = max(1, int(issued * capacity_share / 3 / cost))
        catalogue.append(RewardItem(reward_id, name, cost, stock))
    return catalogue, int(issued * redeem_share)


def _redeemers(rng, transactions, budget):
    balance = {}
    for t in transactions:
        balance[t.student_id] = balance.get(t.student_id, 0) + t.amount
    spent = 0
    for sid in rng.sample(sorted(balance), k=len(balance)):
        if spent >= budget:
            break
        if balance[sid] >= 50:
            cost = 50 if balance[sid] < 120 else 120
            spent += cost
            yield sid, cost


def _truth(scenario):
    kinds = {
        "S1": {"OPPORTUNITY_GAP"},
        "S2": {"ISSUER_DISPARITY"},
        "S4": {"PROXY_GAMING"},
        "S5": {"CATEGORY_CONCENTRATION"},
        "S7": {"ECONOMY_IMBALANCE"},
        "S8": {"ISSUER_DISPARITY", "PROXY_GAMING"},
    }.get(scenario, set())
    return Truth(scenario, frozenset(kinds), expect_insufficient=scenario == "S6")
