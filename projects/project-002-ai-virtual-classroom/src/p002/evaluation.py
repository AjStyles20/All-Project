"""Evaluation against the Pass 017 §14 gates and the Pass 018 baselines.

    python -m p002.evaluation pilot    # seeds 0-4
    python -m p002.evaluation final    # seeds 100-149

APLDG: random course graphs with source supersessions and trusted contradictions. Expected
statuses come from `reference_flags`, a forward propagation written separately from the
kernel's backward explanation. B4 (propagation on) is compared with B2 (provenance recorded
and shown, no propagation).

PGAIC: simulated learners with a known true mastery. B4 (assistance contract) is compared
with B3 (an adaptive tutor that counts correct answers). A learner here is a simulation, not a
person: this measures the policy, not learning (Pass 017 §12).
"""
import json
import random
import sys
from pathlib import Path

from p002.domain import TRUSTED, Assistance, Authority, EdgeType, Mastery, Relation
from p002.mastery import MasteryKernel
from p002.provenance import TrustKernel
from p002.roles import CURATOR, EXPLAINER, QUIZ_WRITER, derive

PILOT_SEEDS = range(0, 5)
FINAL_SEEDS = range(100, 150)


# ---------- APLDG ----------

def random_course(seed, propagate):
    rng = random.Random(seed)
    k = TrustKernel(propagate=propagate)
    trusted = [k.add_source(f"Ref {i}", "v1", f"text {seed}-{i}", rng.choice([Authority.TRUSTED_REFERENCE,
                                                                              Authority.CANONICAL_APPROVED]))
               for i in range(rng.randint(3, 6))]
    community = [k.add_source(f"Forum {i}", "-", f"post {i}", Authority.COMMUNITY_ASSERTION) for i in range(2)]
    base = []
    for i in range(20):
        refs = rng.sample(trusted, rng.randint(1, 2))
        c = k.add_claim(f"fact {i}", Authority.CANONICAL_APPROVED, CURATOR.actor, [(s.id, Relation.SUPPORTS) for s in refs])
        if rng.random() < 0.2:
            k.add_evidence(c.id, rng.choice(community).id, Relation.CONTRADICTS)
        base.append(c.id)
    unsupported = [k.add_claim(f"ai guess {i}", Authority.CANONICAL_APPROVED, EXPLAINER.actor).id for i in range(3)]
    claims = base + unsupported
    for _ in range(25):
        role = rng.choice([EXPLAINER, QUIZ_WRITER, CURATOR])
        parents = rng.sample(claims, rng.choice([1, 1, 2]))
        claims.append(derive(k, role, parents, "paraphrase", text=f"derived from {','.join(parents)}",
                             edge=rng.choice([EdgeType.PARAPHRASE, EdgeType.SUMMARY, EdgeType.INFERENCE])).id)
    for i in range(15):
        k.add_artifact(rng.choice(["lesson", "quiz"]), f"artifact {i}", rng.sample(claims, rng.randint(1, 3)))

    # Events: some sources get a new version that re-confirms only part of what they supported.
    for old in rng.sample(trusted, rng.randint(1, 2)):
        new = k.add_source(old.title, "v2", old.text + " (revised)", old.authority)
        for cid in base:
            if (old.id, Relation.SUPPORTS) in k.claims[cid].evidence and rng.random() < 0.5:
                k.add_evidence(cid, new.id, Relation.SUPPORTS)
        k.supersede(old.id, new.id)
    contra = k.add_source("Other textbook", "v1", "disagrees", Authority.TRUSTED_REFERENCE)
    for cid in rng.sample(base, rng.randint(1, 3)):
        k.add_evidence(cid, contra.id, Relation.CONTRADICTS)
    return k


def reference_flags(k):
    """Independent expectation: which claims are STALE or CONFLICTED, by forward propagation."""
    def trusted(sid):
        return k.sources[sid].authority in TRUSTED
    flagged = {}
    for cid, c in k.claims.items():
        support = [s for s, r in c.evidence if r is Relation.SUPPORTS]
        against = [s for s, r in c.evidence if r is Relation.CONTRADICTS and trusted(s)]
        if any(trusted(s) for s in support) and against:
            flagged[cid] = "CONFLICTED"
        elif support and all(k.sources[s].superseded_by for s in support):
            flagged[cid] = "STALE"
    children = {}
    for cid, c in k.claims.items():
        for pid, _, _ in c.parents:
            children.setdefault(pid, []).append(cid)
    queue = list(flagged)
    while queue:
        cid = queue.pop()
        for child in children.get(cid, []):
            new = "CONFLICTED" if "CONFLICTED" in (flagged.get(child), flagged[cid]) else "STALE"
            if flagged.get(child) != new and flagged.get(child) != "CONFLICTED":
                flagged[child] = new
                queue.append(child)
    artifacts = {aid for aid, a in k.artifacts.items() if any(c in flagged for c in a.depends_on)}
    return flagged, artifacts


def apldg(seeds):
    out = {}
    for name, propagate in (("B2", False), ("B4", True)):
        tp = fp = fn = 0
        claim_ok = claim_total = invalid_false = invalid_total = 0
        laundering = escalations = 0
        for seed in seeds:
            k = random_course(seed, propagate)
            ref = random_course(seed, True)
            flagged, expected_artifacts = reference_flags(ref)
            got = {aid for aid in k.artifacts if k.artifact_status(aid)[0].value in ("STALE", "CONFLICTED")}
            tp += len(got & expected_artifacts)
            fp += len(got - expected_artifacts)
            fn += len(expected_artifacts - got)
            invalid_false += len(got - expected_artifacts)
            invalid_total += len(set(k.artifacts) - expected_artifacts)
            for cid in k.claims:
                claim_total += 1
                status = k.explain(cid).status.value
                claim_ok += (flagged.get(cid) == status) if cid in flagged else status not in ("STALE", "CONFLICTED")
            # Laundering: nothing that descends from an AI claim may rank above AI_DERIVED.
            for cid, c in k.claims.items():
                if _descends_from_ai(k, cid):
                    escalations += 1
                    laundering += c.authority > Authority.AI_DERIVED
        out[name] = {
            "artifact_precision": round(tp / (tp + fp), 3) if tp + fp else None,
            "artifact_recall": round(tp / (tp + fn), 3) if tp + fn else None,
            "false_invalidation_rate": round(invalid_false / invalid_total, 3) if invalid_total else 0.0,
            "claim_status_agreement": round(claim_ok / claim_total, 3),
            "laundering_cases": laundering, "ai_descendants_checked": escalations,
        }
    return out


def _descends_from_ai(k, cid, seen=None):
    seen = seen or set()
    c = k.claims[cid]
    if c.created_by.startswith("ai:"):
        return True
    return any(p not in seen and _descends_from_ai(k, p, seen | {cid}) for p, _, _ in c.parents)


# ---------- PGAIC ----------

def learners(seed, n=300):
    rng = random.Random(f"learners:{seed}")
    return [(f"L{i}", rng.random() < 0.5) for i in range(n)], rng


def pgaic(seeds):
    out = {}
    for name, contract in (("B3", False), ("B4", True)):
        false_mastery = true_mastered = reported_true = missed = l6_independent = l6_cases = 0
        for seed in seeds:
            pool, rng = learners(seed)
            k = MasteryKernel(contract=contract)
            for learner, knows in pool:
                for _ in range(3):
                    level = Assistance(rng.choice([0, 0, 1, 2, 3, 4, 5, 6, 6, 6]))
                    p = 0.9 if knows else min(0.95, 0.15 + 0.13 * int(level))
                    steps = [(Assistance(lv), "learner asked") for lv in range(1, int(level) + 1)]
                    k.record(learner, "join", "practice", rng.random() < p, steps)
                if contract and k.needs_verification(learner, "join"):
                    k.record(learner, "join", "check", rng.random() < (0.9 if knows else 0.15), verification=True)
                state = k.state(learner, "join").mastery
                independent = state is Mastery.INDEPENDENT
                if knows:
                    true_mastered += 1
                    reported_true += independent
                    missed += not independent
                else:
                    false_mastery += independent
            # Gate: an L6 success alone never yields independent mastery.
            g = MasteryKernel(contract=contract)
            for i in range(50):
                steps = [(Assistance(lv), "asked") for lv in range(1, 7)]
                for _ in range(3):
                    g.record(f"g{i}", "join", "practice", True, steps)
                l6_cases += 1
                l6_independent += g.state(f"g{i}", "join").mastery is Mastery.INDEPENDENT
        not_mastered = len(seeds) * 300 - true_mastered
        out[name] = {
            "false_mastery_rate": round(false_mastery / not_mastered, 3),
            "missed_mastery_rate": round(missed / true_mastered, 3),
            "l6_only_reported_independent": round(l6_independent / l6_cases, 3),
        }
    return out


def gates(a, p):
    """Pass 017 §14 gates that can be checked automatically."""
    b4 = a["B4"]
    return {
        "no_laundering": b4["laundering_cases"] == 0,
        "propagation_precision_>=0.95": (b4["artifact_precision"] or 0) >= 0.95,
        "propagation_recall_>=0.95": (b4["artifact_recall"] or 0) >= 0.95,
        "false_invalidation_<=0.05": b4["false_invalidation_rate"] <= 0.05,
        "l6_never_independent": p["B4"]["l6_only_reported_independent"] == 0,
        "measurable_benefit_over_baselines": (b4["artifact_recall"] or 0) > (a["B2"]["artifact_recall"] or 0)
        and p["B4"]["false_mastery_rate"] < p["B3"]["false_mastery_rate"],
    }


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    seeds = {"pilot": PILOT_SEEDS, "final": FINAL_SEEDS}[mode]
    a, p = apldg(seeds), pgaic(seeds)
    result = {"apldg": a, "pgaic": p, "gates": gates(a, p)}
    print(json.dumps(result, indent=2))
    out = Path(__file__).resolve().parents[2] / "benchmark" / "results"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{mode}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
