"""Offline comparison of capture policies on synthetic desktop sessions.

This measures storage and privacy exposure, plus a *proxy* for task resumption: whether a
kept image shows the task window as it was when the user was interrupted. Real resumption
performance needs a study with people (Pass 003); this is not that study.

Usage: python -m p009.simulate [pilot|final]
"""
import json
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from p009.exclusions import Exclusions
from p009.policies import POLICIES, Observation, change, make

PILOT_SEEDS = range(0, 5)
FINAL_SEEDS = range(100, 120)
SESSION_SECONDS = 2 * 3600

TASK_WINDOWS = [
    ("code.exe", "parser.py - thesis-tool - Visual Studio Code"),
    ("chrome.exe", "Python re module documentation - Google Chrome"),
    ("windowsterminal.exe", "pytest - Windows Terminal"),
    ("winword.exe", "Chapter 3 draft.docx - Word"),
    ("notepad.exe", "todo.txt - Notepad"),
]
INTERRUPTIONS = [
    ("ms-teams.exe", "Chat | Group project | Microsoft Teams"),
    ("chrome.exe", "YouTube - Google Chrome"),
]
# Sensitive windows the exclusion list catches.
LISTED_SENSITIVE = [
    ("keepassxc.exe", "Passwords.kdbx - KeePassXC"),
    ("chrome.exe", "Online Banking - Accounts - Google Chrome"),
]
# Sensitive windows it cannot know about (the honest miss case).
UNLISTED_SENSITIVE = [
    ("outlook.exe", "RE: test results from the clinic - Outlook"),
    ("whatsapp.exe", "WhatsApp"),
]


@dataclass
class Session:
    observations: list
    sensitive: set          # seq numbers of ticks showing sensitive content
    sensitive_segments: list  # list of sets of seqs, one per sensitive visit
    critical: list          # (window, signature) at each interruption


def generate(seed: int) -> Session:
    rng = random.Random(seed)
    exclusions = Exclusions()
    observations, sensitive, segments, critical = [], set(), [], []
    state = {}
    t, seq = 0.0, 0
    task = rng.choice(TASK_WINDOWS)

    def base(window):
        if window not in state:
            state[window] = [rng.randint(0, 255) for _ in range(256)]
        return state[window]

    def visit(window, seconds, is_sensitive=False):
        nonlocal t, seq
        sig = base(window)
        typing = rng.random() < 0.7
        since_input = 0.0
        seg = set()
        for _ in range(int(seconds)):
            t += 1
            seq += 1
            if rng.random() < (0.5 if typing else 0.1):
                since_input = 0.0
                for _ in range(3):
                    i = rng.randrange(256)
                    sig[i] = rng.randint(0, 255)
            else:
                since_input += 1
            if rng.random() < 0.02:  # scroll or page change
                for i in rng.sample(range(256), 60):
                    sig[i] = rng.randint(0, 255)
            app, title = window
            obs = Observation(seq, t, app, title, exclusions.excluded(app, title), since_input, tuple(sig),
                              max(20000, int(rng.gauss(90000, 25000))))
            observations.append(obs)
            if is_sensitive:
                sensitive.add(seq)
                seg.add(seq)
        if is_sensitive:
            segments.append(seg)

    while t < SESSION_SECONDS:
        roll = rng.random()
        if roll < 0.55:
            task = rng.choice(TASK_WINDOWS) if rng.random() < 0.3 else task
            visit(task, rng.randint(30, 600))
        elif roll < 0.8:
            # An interruption: remember what the task window looked like when the user left it.
            critical.append((task, tuple(base(task))))
            visit(rng.choice(INTERRUPTIONS), rng.randint(120, 900))
            visit(task, rng.randint(30, 300))
        elif roll < 0.9:
            visit(rng.choice(LISTED_SENSITIVE), rng.randint(10, 120), is_sensitive=True)
        else:
            visit(rng.choice(UNLISTED_SENSITIVE), rng.randint(20, 180), is_sensitive=True)
    return Session(observations, sensitive, segments, critical)


def evaluate(session: Session, policy_name: str) -> dict:
    policy = make(policy_name)
    kept = []
    started = time.perf_counter()
    for obs in session.observations:
        kept += policy.observe(obs)
    seconds = time.perf_counter() - started
    hours = session.observations[-1].t / 3600

    covered = 0
    for window, sig in session.critical:
        if any(k.window == window and change(k.signature, sig) <= 0.03 for k in kept):
            covered += 1
    windows_seen = {o.window for o in session.observations if not o.excluded}
    windows_kept = {k.window for k in kept}
    sensitive_kept = [k for k in kept if k.seq in session.sensitive]
    leaked_segments = sum(1 for seg in session.sensitive_segments if any(k.seq in seg for k in kept))
    return {
        "frames_per_hour": len(kept) / hours,
        "mb_per_hour": sum(k.size_bytes for k in kept) / 1e6 / hours,
        "sensitive_frames": len(sensitive_kept),
        "sensitive_share": len(sensitive_kept) / len(kept) if kept else 0.0,
        "sensitive_visits_exposed": leaked_segments / len(session.sensitive_segments) if session.sensitive_segments else 0.0,
        "resumption_proxy": covered / len(session.critical) if session.critical else 1.0,
        "window_coverage": len(windows_kept & windows_seen) / len(windows_seen),
        "decide_us_per_tick": seconds / len(session.observations) * 1e6,
    }


def run(seeds) -> dict:
    totals = {p: {} for p in POLICIES}
    for seed in seeds:
        session = generate(seed)
        for p in POLICIES:
            for k, v in evaluate(session, p).items():
                totals[p][k] = totals[p].get(k, 0.0) + v
    n = len(seeds)
    return {p: {k: round(v / n, 3) for k, v in m.items()} for p, m in totals.items()}


def proxy_rule(results: dict) -> dict:
    """Predeclared (docs/EVALUATION.md): resumption proxy within 0.05 of B0 and not below B3
    by more than 0.05, and either 20 % fewer frames per hour or half the sensitive frames of B3."""
    b0, b3, b4 = results["B0"], results["B3"], results["B4"]
    utility_ok = b4["resumption_proxy"] >= b0["resumption_proxy"] - 0.05 and \
        b4["resumption_proxy"] >= b3["resumption_proxy"] - 0.05
    cheaper = b4["frames_per_hour"] <= 0.8 * b3["frames_per_hour"]
    safer = b4["sensitive_frames"] <= 0.5 * b3["sensitive_frames"]
    return {"utility_within_tolerance": utility_ok, "fewer_frames_than_B3": cheaper,
            "fewer_sensitive_than_B3": safer,
            "overall": "MET ON PROXY" if utility_ok and (cheaper or safer) else "NOT MET"}


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    seeds = {"pilot": PILOT_SEEDS, "final": FINAL_SEEDS}[mode]
    results = run(seeds)
    keys = list(next(iter(results.values())))
    print("| Policy | " + " | ".join(keys) + " |")
    print("|---" * (len(keys) + 1) + "|")
    for p, m in results.items():
        print(f"| {p} | " + " | ".join(str(m[k]) for k in keys) + " |")
    rule = proxy_rule(results)
    print("\nRule:", rule)
    out = Path(__file__).resolve().parent.parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"{mode}_results.json").write_text(json.dumps({"results": results, "rule": rule}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
