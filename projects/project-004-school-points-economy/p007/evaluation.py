"""Evaluation harness (Pass 004 §13–§14). Metric formulas are in docs/EVALUATION_PROTOCOL.md.

Usage:
    python -m p007.evaluation pilot      # seeds 0-4, for checking the harness only
    python -m p007.evaluation final      # seeds 1000-1019, run once with frozen thresholds
"""
import json
import sys
import time
import tracemalloc
from pathlib import Path

from p007.audit import ENGINES, State
from p007.benchmark import SCENARIOS, Config, generate

PILOT_SEEDS = range(0, 5)
FINAL_SEEDS = range(1000, 1020)

# Which signal kinds count as surfacing each injected condition. Generic kinds (a group
# disparity, an outlier) are accepted so the baselines are credited for pointing a reviewer
# at the right place even when they cannot say why.
ACCEPTED = {
    "OPPORTUNITY_GAP": {"OPPORTUNITY_GAP", "GROUP_DISPARITY"},
    "ISSUER_DISPARITY": {"ISSUER_DISPARITY", "GROUP_DISPARITY", "ISSUER_OUTLIER"},
    "PROXY_GAMING": {"PROXY_GAMING", "STUDENT_OUTLIER"},
    "CATEGORY_CONCENTRATION": {"CATEGORY_CONCENTRATION", "GROUP_DISPARITY", "OPPORTUNITY_GAP"},
    "ECONOMY_IMBALANCE": {"ECONOMY_IMBALANCE"},
}
LEGITIMATE = ("S0", "S3")


def score(cases):
    """cases: list of (truth, report). Returns M1–M5 for one engine."""
    detected = injected = withheld = 0
    false_pos = legit = 0
    unsupported = signals = 0
    insufficient_ok = underdetermined = 0
    for truth, report in cases:
        signal_kinds = [f.kind for f in report.findings if f.state is State.GOVERNANCE_SIGNAL]
        insufficient_kinds = {f.kind for f in report.findings if f.state is State.INSUFFICIENT_CONTEXT}
        allowed = set().union(*(ACCEPTED[c] for c in truth.conditions)) if truth.conditions else set()

        for condition in truth.conditions:
            injected += 1
            if any(k in ACCEPTED[condition] for k in signal_kinds):
                detected += 1
            elif insufficient_kinds & ACCEPTED[condition]:
                withheld += 1

        if truth.scenario in LEGITIMATE:
            legit += 1
            false_pos += bool(signal_kinds)

        signals += len(signal_kinds)
        unsupported += sum(1 for k in signal_kinds if k not in allowed)

        if truth.expect_insufficient:
            underdetermined += 1
            insufficient_ok += bool(insufficient_kinds) and not signal_kinds

    def rate(a, b):
        return round(a / b, 3) if b else None

    return {
        "M1_recall": rate(detected, injected),
        "M2_false_positive_rate": rate(false_pos, legit),
        "M3_unsupported_claim_rate": rate(unsupported, signals),
        "M3_unsupported_claims": unsupported,
        "M4_appropriate_insufficiency": rate(insufficient_ok, underdetermined),
        "M5_incorrect_insufficiency": rate(withheld, injected),
    }


def run(seeds, config=None):
    config = config or Config()
    cases = {name: [] for name in ENGINES}
    per_scenario = {name: {} for name in ENGINES}
    cost = {name: {"seconds": 0.0, "peak_kib": 0} for name in ENGINES}
    for scenario in SCENARIOS:
        for seed in seeds:
            dataset, truth = generate(scenario, seed, config)
            for name, engine in ENGINES.items():
                tracemalloc.start()
                started = time.perf_counter()
                report = engine(dataset)
                cost[name]["seconds"] += time.perf_counter() - started
                cost[name]["peak_kib"] = max(cost[name]["peak_kib"], tracemalloc.get_traced_memory()[1] // 1024)
                tracemalloc.stop()
                cases[name].append((truth, report))
                per_scenario[name].setdefault(scenario, []).append(report.state.value)
    results = {}
    for name in ENGINES:
        results[name] = score(cases[name])
        results[name]["M8_seconds_total"] = round(cost[name]["seconds"], 3)
        results[name]["M8_peak_kib"] = cost[name]["peak_kib"]
        results[name]["states_by_scenario"] = {s: _tally(v) for s, v in per_scenario[name].items()}
    return results


def success_rule(results):
    """The predeclared composite rule (docs/EVALUATION_PROTOCOL.md §4)."""
    b4 = results["B4"]
    verdicts = {}
    for base in ("B1", "B3"):
        other = results[base]
        better = 0
        worse = False
        for key, higher_is_better in (("M1_recall", True), ("M2_false_positive_rate", False),
                                      ("M3_unsupported_claim_rate", False), ("M4_appropriate_insufficiency", True)):
            mine, theirs = b4[key] or 0, other[key] or 0
            diff = (mine - theirs) if higher_is_better else (theirs - mine)
            better += diff >= 0.05
            worse |= diff < -0.05
        verdicts[base] = "B4 BETTER" if better >= 3 and not worse else "NOT SHOWN"
    verdicts["overall"] = "SUPPORTED" if all(v == "B4 BETTER" for v in verdicts.values()) else "NOT SUPPORTED"
    return verdicts


def _tally(states):
    out = {}
    for s in states:
        out[s] = out.get(s, 0) + 1
    return out


def table(results):
    keys = ["M1_recall", "M2_false_positive_rate", "M3_unsupported_claim_rate",
            "M4_appropriate_insufficiency", "M5_incorrect_insufficiency", "M8_seconds_total"]
    lines = ["| Engine | " + " | ".join(keys) + " |", "|---" * (len(keys) + 1) + "|"]
    for name, r in results.items():
        lines.append(f"| {name} | " + " | ".join("—" if r[k] is None else str(r[k]) for k in keys) + " |")
    return "\n".join(lines)


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    seeds = {"pilot": PILOT_SEEDS, "final": FINAL_SEEDS}[mode]
    configs = {"default": Config()}
    if mode == "final":
        # Falsification criterion 6: the effect must survive other class sizes.
        configs.update({"small_classes": Config(students_per_group=15), "large_classes": Config(students_per_group=60)})
    output = {}
    for label, config in configs.items():
        results = run(seeds, config)
        output[label] = {"results": results, "success_rule": success_rule(results)}
        print(f"\n## {mode} — {label} ({config.students_per_group} students per group, seeds {seeds.start}-{seeds.stop - 1})\n")
        print(table(results))
        print("\nSuccess rule:", output[label]["success_rule"])
    out_dir = Path(__file__).resolve().parent.parent / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{mode}_results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
