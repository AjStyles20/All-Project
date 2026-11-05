"""Synthetic incidents with known ground truth, and the evaluation of B0, B1 and B4.

Synthetic fault injection only; never to be described as production ground truth (Pass 001).
Five services; one fault injected per incident, cascading into symptom errors in callers.

Case kinds:
  clear       one cause; its signals appear before the symptoms         truth: that cause
  red_herring as clear, plus another fault's signals only after onset   truth: the real cause
  ambiguous   two different causes both start before the symptoms       truth: UNRESOLVED
  missing     as clear, but the failing service's own logs are absent   truth: UNRESOLVED

    python -m p005.benchmark pilot | final
"""
import json
import random
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from p005.diagnose import FAULTS, diagnose, incident_onset, top_cause, _matches
from p005.logs import parse_line

PILOT_SEEDS = range(0, 10)
FINAL_SEEDS = range(100, 160)
SERVICES = ["gateway", "orders", "payments", "inventory", "postgres"]
CAUSE_LINES = {
    "db_pool": ("postgres", ["FATAL: sorry, too many clients already", "connection pool exhausted (max={n})",
                             "timeout acquiring connection after {n}ms"]),
    "downstream": ("payments", ["connection refused while calling to payments-api", "no healthy upstream payments-api"]),
    "deploy": ("orders", ["deployment orders v{n}.{n} rolled out", "configuration reloaded from /etc/orders/app.yaml"]),
    "disk": ("inventory", ["write failed: no space left on device", "disk full on /var/lib/inventory"]),
    "memory": ("orders", ["java.lang.OutOfMemoryError: Java heap space", "worker {n} OOMKilled"]),
    "cert": ("gateway", ["x509: certificate has expired or is not yet valid", "certificate verify failed for payments.internal"]),
    "dns": ("inventory", ["dial tcp: lookup catalog.internal: no such host", "temporary failure in name resolution"]),
    "rate_limit": ("payments", ["provider returned 429 Too Many Requests", "rate limit exceeded for merchant {n}"]),
}
SYMPTOMS = ["request failed: upstream timeout after {n}ms", "POST /checkout returned 500", "retrying call ({n}/3)",
            "circuit breaker open for {svc}"]
NOISE = ["cache miss for key {n}", "slow query {n}ms", "user {n} not found", "invalid coupon code"]


def _line(t, level, svc, msg, rng):
    return f"{t.strftime('%Y-%m-%dT%H:%M:%S')}Z {level} [{svc}] {msg.format(n=rng.randint(1, 900), svc=rng.choice(SERVICES))}"


def generate(kind, seed):
    """Returns (log lines, truth). truth is a fault key or 'UNRESOLVED'."""
    rng = random.Random(f"{kind}:{seed}")
    start = datetime(2026, 11, 5, 10, 0, tzinfo=timezone.utc)
    onset = start + timedelta(minutes=rng.randint(12, 18), seconds=rng.randint(0, 50))
    end = onset + timedelta(minutes=8)
    cause = rng.choice([f.key for f in FAULTS])
    other = rng.choice([f.key for f in FAULTS if f.key != cause and CAUSE_LINES[f.key][0] != CAUSE_LINES[cause][0]])
    lines = []
    t = start
    while t < end:                                  # background traffic and rare noise
        svc = rng.choice(SERVICES)
        if rng.random() < 0.03:
            lines.append(_line(t, rng.choice(["WARN", "ERROR"]), svc, rng.choice(NOISE), rng))
        else:
            lines.append(_line(t, "INFO", svc, f"GET /api/items/{{n}} 200 {{n}}ms", rng))
        t += timedelta(seconds=rng.uniform(0.5, 2.5))

    def inject(fault, first):
        svc, msgs = CAUSE_LINES[fault]
        count = 1 if fault == "deploy" else rng.randint(5, 12)
        for i in range(count):
            at = first + timedelta(seconds=i * rng.uniform(4, 20))
            level = "INFO" if fault == "deploy" else rng.choice(["ERROR", "ERROR", "WARN"])
            lines.append(_line(at, level, svc, rng.choice(msgs), rng))

    inject(cause, onset - timedelta(seconds=rng.randint(20, 120)))
    if kind == "ambiguous":
        inject(other, onset - timedelta(seconds=rng.randint(20, 120)))
    if kind == "red_herring":
        inject(other, onset + timedelta(seconds=rng.randint(90, 240)))
    # Symptoms: callers fail after onset.
    t = onset
    while t < end:
        svc = rng.choice(["gateway", "orders"])
        lines.append(_line(t, "ERROR", svc, rng.choice(SYMPTOMS), rng))
        t += timedelta(seconds=rng.uniform(1, 4))
    if kind == "missing":
        lines = [l for l in lines if f"[{CAUSE_LINES[cause][0]}]" not in l or cause == "deploy" and "deploy" not in l]
    lines.sort()
    truth = "UNRESOLVED" if kind in ("ambiguous", "missing") else cause
    return lines, truth


def events_of(lines):
    return [e for n, l in enumerate(lines, 1) if (e := parse_line("synthetic.log", n, l))]


# ---------- baselines ----------

def b0_keywords(events):
    """Most frequent cause keyword anywhere in the logs. Always answers."""
    counts = Counter(f.key for e in events for f in FAULTS if _matches(f.key, e))
    return counts.most_common(1)[0][0] if counts else None


def b1_anomaly_temporal(events):
    """The first service to spike after onset, and the most frequent cause keyword in it. Always answers."""
    onset = incident_onset(events)
    if onset is None:
        return None
    near = [e for e in events if e.level >= 3 and onset - timedelta(minutes=3) <= e.time]
    for e in near:
        counts = Counter(f.key for x in near if x.service == e.service for f in FAULTS if _matches(f.key, x))
        if counts:
            return counts.most_common(1)[0][0]
    return None


def b4_evidence_bounded(events):
    return top_cause(diagnose(events))


METHODS = {"B0": b0_keywords, "B1": b1_anomaly_temporal, "B4": b4_evidence_bounded}
KINDS = ("clear", "red_herring", "ambiguous", "missing")


def evaluate(seeds):
    out = {}
    for name, method in METHODS.items():
        correct = asserted_wrong = abstained_right = abstained_wrong = answerable = unanswerable = 0
        provenance_ok = provenance_n = 0
        for kind in KINDS:
            for seed in seeds:
                lines, truth = generate(kind, seed)
                events = events_of(lines)
                answer = method(events)
                if truth == "UNRESOLVED":
                    unanswerable += 1
                    if answer is None:
                        abstained_right += 1
                    else:
                        asserted_wrong += 1
                else:
                    answerable += 1
                    if answer == truth:
                        correct += 1
                    elif answer is None:
                        abstained_wrong += 1
                    else:
                        asserted_wrong += 1
                if name == "B4":
                    d = diagnose(events)
                    for h in d.hypotheses:
                        provenance_n += 1
                        provenance_ok += all(e.source and e.line for e in h.supporting) and bool(h.supporting)
        total = answerable + unanswerable
        out[name] = {
            "correct_when_answerable": round(correct / answerable, 3),
            "unsupported_assertion_rate": round(asserted_wrong / total, 3),
            "correct_abstention": round(abstained_right / unanswerable, 3),
            "abstained_when_answerable": round(abstained_wrong / answerable, 3),
        }
        if name == "B4":
            out[name]["evidence_with_file_and_line"] = round(provenance_ok / provenance_n, 3) if provenance_n else None
    return out


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    seeds = {"pilot": PILOT_SEEDS, "final": FINAL_SEEDS}[mode]
    result = evaluate(seeds)
    print(json.dumps(result, indent=2))
    out = Path(__file__).resolve().parent.parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"{mode}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
