"""Evaluation of B0–B4 on the speech benchmark (Pass 003 metrics). Protocol: docs/EVALUATION.md.

    python -m p010.evaluation pilot    # dev templates, seeds 10-14
    python -m p010.evaluation final    # dev seeds 100-119, held-out paraphrases, and noisy held-out
"""
import json
import sys
import time
from pathlib import Path

from p010.arbiter import PENALTIES, Ruling, engines
from p010.benchmark import generate

TRAIN_SEEDS = range(0, 10)
PILOT_SEEDS = range(10, 15)
FINAL_SEEDS = range(100, 120)
SEVERE = {Ruling.HIGH_CONFIDENCE_VIOLATION, Ruling.ESCALATE}


def macro_f1(pairs):
    labels = {e for e, _ in pairs}
    scores = []
    for label in labels:
        tp = sum(1 for e, p in pairs if e == label and p == label)
        fp = sum(1 for e, p in pairs if e != label and p == label)
        fn = sum(1 for e, p in pairs if e == label and p != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores)


def score(cases, method):
    started = time.perf_counter()
    predictions = [method(c.utterance).ruling for c in cases]
    latency = (time.perf_counter() - started) / len(cases) * 1000
    pairs = [(c.expected, p) for c, p in zip(cases, predictions)]
    innocent = [(e, p) for e, p in pairs if e not in PENALTIES]
    severe = [(e, p) for e, p in pairs if e in SEVERE]
    unsure = [(e, p) for e, p in pairs if e is Ruling.INSUFFICIENT_EVIDENCE]
    decidable = [(e, p) for e, p in pairs if e is not Ruling.INSUFFICIENT_EVIDENCE]
    groups = {}
    for c, p in zip(cases, predictions):
        groups.setdefault(c.group, []).append(p == c.expected)
    return {
        "macro_f1": round(macro_f1(pairs), 3),
        "accuracy": round(sum(e == p for e, p in pairs) / len(pairs), 3),
        "false_penalty_rate": round(sum(p in PENALTIES for _, p in innocent) / len(innocent), 3),
        "missed_severe_rate": round(sum(p is Ruling.NO_VIOLATION for _, p in severe) / len(severe), 3),
        "appropriate_abstention": round(sum(p is Ruling.INSUFFICIENT_EVIDENCE for _, p in unsure) / len(unsure), 3),
        "incorrect_abstention": round(sum(p is Ruling.INSUFFICIENT_EVIDENCE for _, p in decidable) / len(decidable), 3),
        "policy_consistency": round(sum(all(v) for v in groups.values()) / len(groups), 3),
        "ms_per_ruling": round(latency, 3),
    }


def run(sets):
    training = [(c.utterance, c.expected) for c in generate("dev", TRAIN_SEEDS)]
    methods = engines(training)
    return {label: {name: score(cases, m) for name, m in methods.items()} for label, cases in sets.items()}


def rule(results):
    """Predeclared (docs/EVALUATION.md §4)."""
    dev = results["dev"]
    others = [m for m in dev if m != "B4"]
    b4 = dev["B4"]
    best_f1 = max(dev[m]["macro_f1"] for m in others)
    checks = {
        "f1_beats_best_other_by_0.05": b4["macro_f1"] >= best_f1 + 0.05,
        "false_penalty_at_most_0.05": b4["false_penalty_rate"] <= 0.05,
        "missed_severe_at_most_0.05": b4["missed_severe_rate"] <= 0.05,
    }
    if "held_out_noisy" in results:
        checks["noisy_paraphrase_f1_drop_at_most_0.15"] = b4["macro_f1"] - results["held_out_noisy"]["B4"]["macro_f1"] <= 0.15
    checks["overall"] = "SUPPORTED" if all(checks.values()) else "NOT SUPPORTED"
    return checks


def table(results):
    keys = list(next(iter(next(iter(results.values())).values())))
    lines = []
    for label, by_method in results.items():
        lines += [f"\n### {label}\n", "| Method | " + " | ".join(keys) + " |", "|---" * (len(keys) + 1) + "|"]
        for m, r in by_method.items():
            lines.append(f"| {m} | " + " | ".join(str(r[k]) for k in keys) + " |")
    return "\n".join(lines)


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    if mode == "pilot":
        sets = {"dev": generate("dev", PILOT_SEEDS)}
    else:
        sets = {"dev": generate("dev", FINAL_SEEDS), "held_out": generate("held_out", FINAL_SEEDS),
                "held_out_noisy": generate("held_out", FINAL_SEEDS, noise=True)}
    results = run(sets)
    verdict = rule(results)
    print(table(results))
    print("\nRule:", verdict)
    out = Path(__file__).resolve().parent.parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"{mode}_results.json").write_text(json.dumps({"results": results, "rule": verdict}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
