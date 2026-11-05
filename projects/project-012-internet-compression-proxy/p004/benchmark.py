"""Benchmark B0–B4 on the corpus under the five modelled network profiles (spec §4, §7–§9).

    python -m p004.benchmark pilot   # corpus seed 0: fits B4's cost model, writes results/cost_model.json
    python -m p004.benchmark final   # corpus seeds 1-5 with the frozen cost model
"""
import json
import platform
import sys
from pathlib import Path

from p004 import corpus
from p004.policies import POLICIES, VOC, CostModel, Hints, facts_for, make
from p004.transforms import NotTransformable, faithful, fidelity, to_gzip, to_webp

PROFILES = {"N0": (1000, 1), "N1": (0.25, 300), "N2": (1.5, 100), "N3": (10, 200), "N4": (50, 20)}
RESULTS = Path(__file__).resolve().parent.parent / "results"


def completion_ms(wire_bytes, work_ms, profile):
    mbps, rtt = PROFILES[profile]
    return work_ms + rtt + wire_bytes * 8 / (mbps * 1000)


class Transformer:
    """Runs each distinct transformation once and remembers bytes, time and fidelity."""

    def __init__(self):
        self.memo = {}

    def run(self, obj, plan):
        key = (obj.sha256, plan.action, plan.quality, plan.max_width, plan.level)
        if key not in self.memo:
            try:
                if plan.action == "webp":
                    out, ms = to_webp(obj.body, plan.quality, plan.max_width)
                    scores = fidelity(obj.body, out)
                else:
                    out, ms = to_gzip(obj.body, plan.level)
                    scores = None
                self.memo[key] = (len(out), ms, scores)
            except NotTransformable:
                self.memo[key] = None
        return self.memo[key]


def evaluate(objs, model, transformer):
    rows = []
    for obj in objs:
        f = facts_for(obj.content_type, obj.body, obj.headers)
        for profile, (mbps, rtt) in PROFILES.items():
            h = Hints(downlink_mbps=mbps, rtt_ms=rtt)
            base_time = completion_ms(len(obj.body), 0, profile)
            for name in POLICIES:
                policy = make(name, model)
                plan = policy(f, h)
                wire, work, outcome, scores = len(obj.body), 0.0, None, None
                if plan.action == "abstain":
                    outcome = "ABSTAIN"
                elif plan.action == "pass":
                    outcome = "PASS_THROUGH"
                else:
                    result = transformer.run(obj, plan)
                    if result is None:
                        outcome = "PASS_THROUGH"
                    else:
                        size, work, scores = result
                        served = True
                        if name == "B4":
                            served, _ = VOC.verify(len(obj.body), size, scores)
                        if served:
                            wire = size
                            slower = completion_ms(wire, work, profile) > base_time * 1.01
                            unfaithful = scores is not None and not faithful(*scores)
                            outcome = "TRANSFORM_REGRESSION" if (size >= len(obj.body) or slower or unfaithful) \
                                else "TRANSFORM_SUCCESS"
                        else:
                            outcome = "VERIFIED_FALLBACK"   # transformed, checked, original served
                rows.append({"object": obj.name, "class": obj.cls, "profile": profile, "policy": name,
                             "action": plan.action, "outcome": outcome, "original_bytes": len(obj.body),
                             "wire_bytes": wire, "work_ms": round(work, 1),
                             "completion_ms": round(completion_ms(wire, work, profile), 1),
                             "baseline_ms": round(base_time, 1),
                             "psnr": None if not scores else round(scores[0], 2),
                             "ssim": None if not scores else round(scores[1], 4)})
    return rows


def fit(objs, transformer) -> CostModel:
    """Cost model from pilot objects. Conservative: the slowest observed rate on objects of
    real size, plus the slowest fixed cost seen on tiny objects."""
    from p004.policies import Plan
    mpx_rate, mpx_small, gz_rate, gz_small, ratios = [], [], [], [], {}
    for obj in objs:
        f = facts_for(obj.content_type, obj.body, obj.headers)
        if f.image_dims and "no-transform" not in f.headers.get("cache-control", ""):
            mpx = f.image_dims[0] * f.image_dims[1] / 1e6
            for q in (60, 80):
                r = transformer.run(obj, Plan("webp", quality=q))
                if r:
                    (mpx_rate.append(r[1] / mpx) if mpx >= 0.1 else mpx_small.append(r[1]))
                    ratios.setdefault((f.content_type, CostModel.bucket(f.size), q), []).append(r[0] / f.size)
        elif f.content_type.startswith(("text/", "application/json", "application/javascript")):
            r = transformer.run(obj, Plan("gzip", level=6))
            (gz_rate.append(r[1] / (f.size / 1e6)) if f.size >= 10_000 else gz_small.append(r[1]))
            ratios.setdefault((f.content_type, CostModel.bucket(f.size), 6), []).append(r[0] / f.size)
    mean = lambda v: sum(v) / len(v)
    return CostModel(webp_ms_per_mpx=max(mpx_rate), gzip_ms_per_mb=max(gz_rate),
                     webp_overhead_ms=max(mpx_small or [5.0]), gzip_overhead_ms=max(gz_small or [1.0]),
                     ratios={k: mean(v) for k, v in ratios.items()})


def summarise(rows):
    out = {}
    for name in POLICIES:
        mine = [r for r in rows if r["policy"] == name]
        counts = {}
        for r in mine:
            counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
        by_profile = {}
        for p in PROFILES:
            sel = [r for r in mine if r["profile"] == p]
            original = sum(r["original_bytes"] for r in sel)
            by_profile[p] = {
                "bytes_saved": original - sum(r["wire_bytes"] for r in sel),
                "bytes_saved_share": round(1 - sum(r["wire_bytes"] for r in sel) / original, 3),
                "total_ms": round(sum(r["completion_ms"] for r in sel)),
                "baseline_ms": round(sum(r["baseline_ms"] for r in sel)),
            }
        out[name] = {"outcomes": counts, "by_profile": by_profile}
    return out


def verdict(rows, summary):
    regressions = {p: summary[p]["outcomes"].get("TRANSFORM_REGRESSION", 0) for p in POLICIES}
    q1 = regressions["B4"] <= 0.5 * min(regressions[p] for p in ("B1", "B2", "B3"))
    q2 = all(summary["B4"]["by_profile"][p]["bytes_saved"] >= 0.8 * summary["B3"]["by_profile"][p]["bytes_saved"]
             for p in ("N1", "N2"))
    restricted = [r for r in rows if r["policy"] == "B4" and r["class"] in ("K7", "K8")]
    q3 = all(r["outcome"] in ("ABSTAIN", "PASS_THROUGH") or r["object"] in ("k7-private.json", "k7-no-store.png")
             for r in restricted) and all(r["wire_bytes"] == r["original_bytes"] for r in restricted
                                          if r["object"] in ("k7-no-transform.jpg", "k8-huge.png", "k8-broken.jpg"))
    eligible = [(r["object"], r["profile"]) for r in rows if r["policy"] == "B3" and r["action"] in ("webp", "gzip")]
    b3 = {(r["object"], r["profile"]): r["action"] in ("webp", "gzip") for r in rows if r["policy"] == "B3"}
    b4 = {(r["object"], r["profile"]): r["action"] in ("webp", "gzip") for r in rows if r["policy"] == "B4"}
    pairs = [k for k in b3 if b3[k] or b4[k]]
    same = sum(b3[k] == b4[k] for k in pairs) / len(pairs) if pairs else 1.0
    return {"Q1_regressions": regressions, "Q1_met": q1, "Q2_met": q2, "Q3_met": q3,
            "B4_same_decision_as_B3": round(same, 3), "kill_check_behaves_like_B3": same >= 0.9,
            "eligible_pairs": len(eligible)}


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    RESULTS.mkdir(exist_ok=True)
    transformer = Transformer()
    env = {"python": platform.python_version(), "machine": platform.machine(), "processor": platform.processor(),
           "system": platform.platform()}
    if mode == "pilot":
        objs = corpus.build(0)
        model = fit(objs, transformer)
        (RESULTS / "cost_model.json").write_text(json.dumps(
            {"webp_ms_per_mpx": model.webp_ms_per_mpx, "gzip_ms_per_mb": model.gzip_ms_per_mb,
             "webp_overhead_ms": model.webp_overhead_ms, "gzip_overhead_ms": model.gzip_overhead_ms,
             "ratios": [[k[0], k[1], k[2], v] for k, v in model.ratios.items()], "environment": env}, indent=2))
        print("cost model fitted on seed 0:", model)
        return
    model = CostModel.load(RESULTS / "cost_model.json")
    objs = [o for seed in range(1, 6) for o in corpus.build(seed)]
    rows = evaluate(objs, model, transformer)
    summary = summarise(rows)
    result = verdict(rows, summary)
    (RESULTS / "corpus_manifest.json").write_text(json.dumps(
        {seed: corpus.manifest(corpus.build(seed)) for seed in range(0, 6)}, indent=2))
    (RESULTS / "final_rows.json").write_text(json.dumps(rows, indent=1))
    (RESULTS / "final_summary.json").write_text(json.dumps({"summary": summary, "verdict": result, "environment": env}, indent=2))
    for name, s in summary.items():
        print(name, s["outcomes"])
        for p, v in s["by_profile"].items():
            print("   ", p, v)
    print("\nVerdict:", result)


if __name__ == "__main__":
    main(sys.argv)
