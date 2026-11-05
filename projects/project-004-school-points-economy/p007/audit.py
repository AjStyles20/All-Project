"""Audit engines B0–B4 (Pass 004 §12). Each reads only a Dataset, never benchmark truth.

Outputs use the three canonical states (§8). There is deliberately no FAIR/UNFAIR verdict:
a GOVERNANCE_SIGNAL means "a person should look at this", nothing more.

Every threshold is a named constant in THRESHOLDS so runs are reproducible and the values
can be frozen before the final evaluation (§16).
"""
import statistics
from dataclasses import dataclass, field
from enum import Enum
from math import sqrt

from p007.domain import Action, Dataset


class State(str, Enum):
    NO_MATERIAL_SIGNAL = "NO MATERIAL SIGNAL"
    GOVERNANCE_SIGNAL = "GOVERNANCE SIGNAL"
    INSUFFICIENT_CONTEXT = "INSUFFICIENT CONTEXT"


NON_CLAIMS = ("This is not a finding of discrimination, misconduct or cheating.",
              "It does not establish a cause; it shows where a person should look.")


@dataclass(frozen=True)
class Finding:
    kind: str
    state: State
    subject: str
    observations: tuple
    comparison: str = ""
    missing_context: tuple = ()
    non_claims: tuple = NON_CLAIMS


@dataclass
class AuditReport:
    engine: str
    findings: list = field(default_factory=list)

    @property
    def state(self) -> State:
        states = {f.state for f in self.findings}
        if State.GOVERNANCE_SIGNAL in states:
            return State.GOVERNANCE_SIGNAL
        if State.INSUFFICIENT_CONTEXT in states:
            return State.INSUFFICIENT_CONTEXT
        return State.NO_MATERIAL_SIGNAL


THRESHOLDS = {
    "B1": {"group_ratio": 0.8, "issuer_vs_median": 1.5, "category_share": 0.5, "issued_points_per_student": 260},
    "B2": {"student_z": 3.0, "issuer_modified_z": 3.5},
    "B3": {"group_ratio": 0.8, "min_students": 20},
    "B4": {"opportunity_ratio": 0.8, "rate_ratio": 0.75, "z": 3.5, "min_awards": 20,
           "missing_share": 0.2, "raw_ratio": 0.8, "proxy_measure_share": 0.25, "proxy_count_factor": 1.5,
           "category_share": 0.5, "access_gap": 0.5},
}


# ---------- shared aggregates ----------

def _earns(dataset):
    return [t for t in dataset.transactions if t.action is Action.EARN]


def _net_points(dataset):
    """Points per (student, policy) after reversals."""
    totals = {}
    for t in dataset.transactions:
        if t.action in (Action.EARN, Action.REVERSE) and t.policy_id:
            key = (t.student_id, t.policy_id)
            totals[key] = totals.get(key, 0) + t.amount
    return totals


def _groups(dataset):
    groups = {}
    for s in dataset.students:
        groups.setdefault(s.group, []).append(s.student_id)
    return groups


def _mean_by_group(values_by_student, groups):
    return {g: statistics.fmean(values_by_student.get(s, 0) for s in ids) for g, ids in groups.items()}


def _ratio(means):
    low, high = min(means.values()), max(means.values())
    return 1.0 if high == 0 else low / high


def _category_shares(dataset):
    totals = {}
    for t in _earns(dataset):
        totals[t.category] = totals.get(t.category, 0) + t.amount
    whole = sum(totals.values()) or 1
    return {c: v / whole for c, v in totals.items()}


# ---------- B0: aggregate dashboard ----------

def b0_dashboard(dataset: Dataset) -> AuditReport:
    """Totals only. Never interprets them, so it never raises a signal."""
    return AuditReport("B0")


# ---------- B1: static thresholds ----------

def b1_static(dataset: Dataset) -> AuditReport:
    th = THRESHOLDS["B1"]
    report = AuditReport("B1")
    points = _net_points(dataset)
    groups = _groups(dataset)
    for policy_id in dataset.policies:
        means = _mean_by_group({s: points.get((s, policy_id), 0) for s in (st.student_id for st in dataset.students)}, groups)
        if _ratio(means) < th["group_ratio"]:
            report.findings.append(Finding("GROUP_DISPARITY", State.GOVERNANCE_SIGNAL, f"policy {policy_id}",
                                           (f"mean points by group: {_fmt(means)}",)))
    by_issuer = {}
    for t in _earns(dataset):
        by_issuer[t.issuer_id] = by_issuer.get(t.issuer_id, 0) + t.amount
    median = statistics.median(by_issuer.values()) if by_issuer else 0
    for issuer, total in sorted(by_issuer.items()):
        if median and total > th["issuer_vs_median"] * median:
            report.findings.append(Finding("ISSUER_OUTLIER", State.GOVERNANCE_SIGNAL, f"issuer {issuer}",
                                           (f"issued {total} points; median issuer {median:.0f}",)))
    for category, share in _category_shares(dataset).items():
        if share > th["category_share"]:
            report.findings.append(Finding("CATEGORY_CONCENTRATION", State.GOVERNANCE_SIGNAL, f"category {category}",
                                           (f"{share:.0%} of all points",)))
    issued = sum(t.amount for t in _earns(dataset))
    if dataset.students and issued / len(dataset.students) > th["issued_points_per_student"]:
        report.findings.append(Finding("ECONOMY_IMBALANCE", State.GOVERNANCE_SIGNAL, "economy",
                                       (f"{issued / len(dataset.students):.0f} points issued per student",)))
    return report


# ---------- B2: generic anomaly detection ----------

def b2_anomaly(dataset: Dataset) -> AuditReport:
    th = THRESHOLDS["B2"]
    report = AuditReport("B2")
    per_student = {}
    for t in _earns(dataset):
        per_student[t.student_id] = per_student.get(t.student_id, 0) + t.amount
    values = [per_student.get(s.student_id, 0) for s in dataset.students]
    if len(values) > 2 and statistics.pstdev(values) > 0:
        mean, sd = statistics.fmean(values), statistics.pstdev(values)
        outliers = [s.student_id for s, v in zip(dataset.students, values) if abs(v - mean) / sd > th["student_z"]]
        if outliers:
            report.findings.append(Finding("STUDENT_OUTLIER", State.GOVERNANCE_SIGNAL, f"{len(outliers)} students",
                                           (f"total points more than {th['student_z']} SD from the mean",)))
    per_issuer = {}
    for t in _earns(dataset):
        per_issuer[t.issuer_id] = per_issuer.get(t.issuer_id, 0) + t.amount
    if len(per_issuer) > 2:
        median = statistics.median(per_issuer.values())
        mad = statistics.median(abs(v - median) for v in per_issuer.values())
        for issuer, v in sorted(per_issuer.items()):
            if mad and 0.6745 * abs(v - median) / mad > th["issuer_modified_z"]:
                report.findings.append(Finding("ISSUER_OUTLIER", State.GOVERNANCE_SIGNAL, f"issuer {issuer}",
                                               (f"issued {v} points; median {median:.0f}",)))
    return report


# ---------- B3: disparity-only fairness monitoring ----------

def b3_disparity(dataset: Dataset) -> AuditReport:
    """Group disparities per policy and per issuer, with no opportunity context."""
    th = THRESHOLDS["B3"]
    report = AuditReport("B3")
    groups = _groups(dataset)
    cells = {}
    for t in _earns(dataset):
        for key in ((t.policy_id, None), (t.policy_id, t.issuer_id)):
            cells.setdefault(key, {}).setdefault(t.student_id, 0)
            cells[key][t.student_id] += t.amount
    for (policy_id, issuer), per_student in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1] or "")):
        if len(per_student) < th["min_students"]:
            continue
        means = _mean_by_group(per_student, groups)
        if _ratio(means) < th["group_ratio"]:
            where = f"policy {policy_id}" + (f", issuer {issuer}" if issuer else "")
            report.findings.append(Finding("GROUP_DISPARITY", State.GOVERNANCE_SIGNAL, where,
                                           (f"mean points by group: {_fmt(means)}",)))
    return report


# ---------- B4: contextual governance audit ----------

def b4_contextual(dataset: Dataset) -> AuditReport:
    """Interprets disparities against eligible opportunities, issuer award rates, the policy's
    own objective measure and the reward supply, and says when it cannot tell."""
    report = AuditReport("B4")
    report.findings += _opportunity_and_issuer_checks(dataset)
    report.findings += _proxy_checks(dataset)
    report.findings += _category_checks(dataset)
    report.findings += _economy_checks(dataset)
    return report


def _opportunity_and_issuer_checks(dataset):
    th = THRESHOLDS["B4"]
    findings = []
    groups = _groups(dataset)
    group_of = {s.student_id: s.group for s in dataset.students}
    awards = {}
    for t in _earns(dataset):
        key = (t.policy_id, t.issuer_id, group_of.get(t.student_id))
        awards[key] = awards.get(key, 0) + 1
    points = _net_points(dataset)

    for policy_id in sorted(dataset.policies):
        pairs = [(s, k) for s in dataset.students for k in s.opportunities if k[0] == policy_id]
        if not pairs:
            continue
        missing = sum(1 for s, k in pairs if s.opportunities[k] is None) / len(pairs)
        raw_means = _mean_by_group({s.student_id: points.get((s.student_id, policy_id), 0) for s in dataset.students}, groups)

        if missing > th["missing_share"]:
            if _ratio(raw_means) < th["raw_ratio"]:
                findings.append(Finding(
                    "GROUP_DISPARITY", State.INSUFFICIENT_CONTEXT, f"policy {policy_id}",
                    (f"mean points by group: {_fmt(raw_means)}",),
                    "Points differ between groups, but the number of eligible opportunities is unknown.",
                    (f"opportunity counts missing for {missing:.0%} of student-issuer pairs",
                     "without them, a difference in opportunity cannot be told apart from a difference in award rate")))
            continue

        opp_by_student = {}
        for s, k in pairs:
            opp_by_student[s.student_id] = opp_by_student.get(s.student_id, 0) + (s.opportunities[k] or 0)
        opp_means = _mean_by_group(opp_by_student, groups)
        opp_values = {g: [opp_by_student.get(sid, 0) for sid in ids] for g, ids in groups.items()}
        if _ratio(opp_means) < th["opportunity_ratio"] and _welch_t(*opp_values.values()) > th["z"]:
            findings.append(Finding(
                "OPPORTUNITY_GAP", State.GOVERNANCE_SIGNAL, f"policy {policy_id}",
                (f"mean eligible opportunities per student by group: {_fmt(opp_means)}",
                 f"mean points by group: {_fmt(raw_means)}"),
                "Groups had different numbers of chances to earn under this policy.",
                ("why opportunities differ (timetable, access, eligibility rules)",)))

        for issuer in sorted({k[1] for _, k in pairs}):
            exposure = {g: 0 for g in groups}
            for s, k in pairs:
                if k[1] == issuer:
                    exposure[s.group] += s.opportunities[k] or 0
            counts = {g: awards.get((policy_id, issuer, g), 0) for g in groups}
            if sum(counts.values()) < th["min_awards"] or min(exposure.values()) == 0:
                continue
            rates = {g: counts[g] / exposure[g] for g in groups}
            low, high = min(rates, key=rates.get), max(rates, key=rates.get)
            if rates[high] and rates[low] / rates[high] < th["rate_ratio"] and \
                    _two_proportion_z(counts[low], exposure[low], counts[high], exposure[high]) > th["z"]:
                findings.append(Finding(
                    "ISSUER_DISPARITY", State.GOVERNANCE_SIGNAL, f"issuer {issuer}, policy {policy_id}",
                    (f"awards per eligible opportunity by group: {_fmt(rates, '.2f')}",
                     f"opportunities by group: {_fmt(exposure, '.0f')}"),
                    "The same issuer awarded at different rates per opportunity across groups.",
                    ("differences in the work actually submitted", "class-level context the ledger does not hold")))
    return findings


def _proxy_checks(dataset):
    """Students who earn often while each award reflects very little of the policy's own
    objective measure (e.g. many very short books)."""
    th = THRESHOLDS["B4"]
    findings = []
    for policy in dataset.policies.values():
        if not policy.objective_measure:
            continue
        measures, counts = {}, {}
        for t in _earns(dataset):
            if t.policy_id == policy.policy_id and t.measure is not None:
                measures.setdefault(t.student_id, []).append(t.measure)
                counts[t.student_id] = counts.get(t.student_id, 0) + 1
        if len(measures) < 5:
            continue
        typical_measure = statistics.median(statistics.median(v) for v in measures.values())
        typical_count = statistics.median(counts.values())
        flagged = [s for s, v in measures.items()
                   if statistics.median(v) < th["proxy_measure_share"] * typical_measure
                   and counts[s] > th["proxy_count_factor"] * typical_count]
        if flagged:
            findings.append(Finding(
                "PROXY_GAMING", State.GOVERNANCE_SIGNAL, f"policy {policy.policy_id}",
                (f"{len(flagged)} students earn often with a median of under "
                 f"{th['proxy_measure_share']:.0%} of the typical {policy.objective_measure} per award",
                 f"typical: {typical_measure:.0f} {policy.objective_measure} per award, {typical_count:.0f} awards"),
                f"The earning rule is met while the objective ('{policy.intended_objective}') is barely advanced.",
                ("whether the policy meant to allow this (the rule may need changing, not the students)",),
                NON_CLAIMS + ("Students following a badly designed rule are not cheating.",)))
    return findings


def _category_checks(dataset):
    th = THRESHOLDS["B4"]
    findings = []
    groups = _groups(dataset)
    for category, share in _category_shares(dataset).items():
        if share <= th["category_share"]:
            continue
        policy_ids = {p.policy_id for p in dataset.policies.values() if p.category == category}
        access, unknown = {g: 0 for g in groups}, False
        for s in dataset.students:
            counts = [c for k, c in s.opportunities.items() if k[0] in policy_ids]
            if any(c is None for c in counts):
                unknown = True
            elif sum(counts) > 0:
                access[s.group] += 1
        if unknown:
            findings.append(Finding("CATEGORY_CONCENTRATION", State.INSUFFICIENT_CONTEXT, f"category {category}",
                                    (f"{share:.0%} of all points",), "Who could earn in this category is unknown.",
                                    ("opportunity records for this category",)))
            continue
        shares = {g: access[g] / len(ids) for g, ids in groups.items()}
        if max(shares.values()) - min(shares.values()) > th["access_gap"]:
            findings.append(Finding(
                "CATEGORY_CONCENTRATION", State.GOVERNANCE_SIGNAL, f"category {category}",
                (f"{share:.0%} of all points", f"share of students with any opportunity: {_fmt(shares, '.0%')}"),
                "One category dominates points and is open to some groups far more than others.",
                ("why access differs",)))
    return findings


def _economy_checks(dataset):
    issued = sum(t.amount for t in dataset.transactions if t.action in (Action.EARN, Action.REVERSE))
    redeemed = -sum(t.amount for t in dataset.transactions if t.action is Action.REDEEM)
    outstanding = issued - redeemed
    capacity = sum(item.point_cost * item.stock for item in dataset.catalogue)
    if outstanding > capacity:
        return [Finding("ECONOMY_IMBALANCE", State.GOVERNANCE_SIGNAL, "economy",
                        (f"outstanding points {outstanding}", f"remaining reward capacity {capacity} points",
                         f"redeemed {redeemed} of {issued} issued"),
                        "Students hold more points than the catalogue can absorb.",
                        ("planned restocking", "whether points are meant to be saved"))]
    return []


# ---------- statistics ----------

def _welch_t(a, b):
    if len(a) < 2 or len(b) < 2:
        return 0.0
    va, vb = statistics.variance(a), statistics.variance(b)
    se = sqrt(va / len(a) + vb / len(b))
    if se == 0:
        return float("inf") if statistics.fmean(a) != statistics.fmean(b) else 0.0
    return abs(statistics.fmean(a) - statistics.fmean(b)) / se


def _two_proportion_z(x1, n1, x2, n2):
    # Award counts can exceed 1 per opportunity in principle, so clamp the pooled rate.
    p = min((x1 + x2) / (n1 + n2), 0.999)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return 0.0 if se == 0 else abs(x1 / n1 - x2 / n2) / se


def _fmt(values, spec=".1f"):
    return ", ".join(f"{k} {format(v, spec)}" for k, v in sorted(values.items()))


ENGINES = {"B0": b0_dashboard, "B1": b1_static, "B2": b2_anomaly, "B3": b3_disparity, "B4": b4_contextual}
