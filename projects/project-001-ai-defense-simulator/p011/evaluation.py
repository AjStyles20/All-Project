"""Evaluation on generated project reports with planted issues.

    python -m p011.evaluation pilot    # dev phrasings, seeds 0-4
    python -m p011.evaluation final    # seeds 100-139, dev phrasings and held-out phrasings

B0: a fixed bank of generic defence questions (no documents).
B1: questions about randomly chosen sentences from the documents (grounded, but not targeted).
B4: questions planned from the analysis findings (this system).
Each answers: how many planted issues does a 12-question session reach?
"""
import json
import random
import sys
from pathlib import Path

from p011.analysis import analyse
from p011.ingest import sentences
from p011.reviewers import ROLES, Question, plan

PILOT_SEEDS = range(0, 5)
FINAL_SEEDS = range(100, 140)
SESSION = list(ROLES)          # all four roles, three questions each

TOPICS = [("attendance app", "teachers"), ("library chatbot", "students"), ("parking sensor", "drivers"),
          ("exam timetable planner", "administrators"), ("clinic booking system", "patients")]

DEV = {
    "UNSUPPORTED_CLAIM": ["Our {t} is the first system of its kind for {u}.", "The {t} significantly improves how {u} work.",
                          "This design is robust and scalable for any number of {u}."],
    "CONTRADICTION": ["In testing, accuracy was {a}%.", "The final accuracy was {b}% on the same data."],
    "LIMITATION": ["However, it was only tested with {n} {u}.", "Offline use is future work."],
    "NEUTRAL": ["The {t} has three screens: login, dashboard and settings.", "We met weekly with our supervisor.",
                "The interface uses large buttons and a simple layout.", "Chapter two reviews related work.",
                "The project ran from January to May."],
}
HELD_OUT = {
    "UNSUPPORTED_CLAIM": ["No other tool does what our {t} does for {u}.", "The {t} makes {u} far more productive.",
                          "It will handle any load we throw at it."],
    "CONTRADICTION": ["We measured a response time of {a} ms.", "Average response time came out at {b} ms."],
    "LIMITATION": ["We could only recruit {n} {u} for the trial.", "The {t} cannot yet work without internet."],
    "NEUTRAL": DEV["NEUTRAL"],
}
PARTS = ["login screen", "dashboard", "settings page", "database", "server", "mobile client", "report module",
         "notification service", "search page", "admin panel"]
VERBS = ["sends data to", "reads from", "is shown after", "links to", "is configured by", "stores its records in"]
FILLER = ["The {x} {v} the {y}.", "Users reach the {x} from the {y}.", "The {x} was built in the second sprint.",
          "Section four describes the {x} in detail.", "The {x} uses the same colour scheme as the {y}."]


def neutral(rng, n=60):
    out = set()
    while len(out) < n:
        x, y = rng.sample(PARTS, 2)
        out.add(rng.choice(FILLER).format(x=x, y=y, v=rng.choice(VERBS)))
    return sorted(out)


GENERIC_BANK = ["What problem does your project solve?", "Why did you choose this technology?",
                "What would you do differently?", "How did you test your system?", "What are your main contributions?",
                "Who are the users?", "What was the hardest part?", "How does this compare to existing work?",
                "What are the limitations?", "What is future work?", "How did you manage the project?",
                "What did you learn?"]


def report(seed, pool):
    """A report as paragraphs [(chunk_id, text)], and the planted issues {sentence: kind}."""
    rng = random.Random(f"{seed}:{'held-out' if pool is HELD_OUT else 'dev'}")
    t, u = rng.choice(TOPICS)
    a = rng.randint(70, 95)
    b = a + rng.choice([-7, -4, 3, 6])
    values = {"t": t, "u": u, "a": a, "b": b, "n": rng.randint(4, 12)}
    planted, lines = {}, []
    for kind in ("UNSUPPORTED_CLAIM", "CONTRADICTION", "LIMITATION"):
        for template in pool[kind]:
            s = template.format(**values)
            planted[s] = kind
            lines.append(s)
    lines += [s.format(**values) for s in pool["NEUTRAL"]] + neutral(rng)
    rng.shuffle(lines)
    paragraphs = [lines[i:i + 4] for i in range(0, len(lines), 4)]
    chunks = [(f"c{i}", " ".join(p)) for i, p in enumerate(paragraphs)]
    # Contradiction is one issue spanning two sentences; count it once.
    contradiction = [s for s, k in planted.items() if k == "CONTRADICTION"]
    issues = {s: k for s, k in planted.items() if k != "CONTRADICTION"}
    issues[" || ".join(contradiction)] = "CONTRADICTION"
    return chunks, issues


def reached(questions, issues):
    hit = set()
    for q in questions:
        for key, kind in issues.items():
            if any(part and part in q.quote for part in key.split(" || ")):
                hit.add(key)
    return hit


def b0(chunks, rng):
    return [Question("any", "GENERAL", q, (), "", False) for q in GENERIC_BANK]


def b1(chunks, rng):
    pool = [(cid, s) for cid, text in chunks for s in sentences(text)]
    return [Question("any", "RANDOM", f"Tell me more about this: \"{s}\"", (cid,), s, True)
            for cid, s in rng.sample(pool, min(12, len(pool)))]


def b4(chunks, rng):
    return plan(SESSION, analyse(chunks), per_role=3)


def run(seeds, pool):
    out = {}
    for name, method in (("B0", b0), ("B1", b1), ("B4", b4)):
        reached_n = total = grounded_ok = grounded_n = false_alarm = findings_n = 0
        by_kind = {}
        for seed in seeds:
            chunks, issues = report(seed, pool)
            rng = random.Random(seed)
            questions = method(chunks, rng)
            hit = reached(questions, issues)
            reached_n += len(hit)
            total += len(issues)
            for key, kind in issues.items():
                k = by_kind.setdefault(kind, [0, 0])
                k[0] += key in hit
                k[1] += 1
            texts = dict(chunks)
            for q in questions:
                if q.grounded:
                    grounded_n += 1
                    grounded_ok += any(q.quote in texts.get(c, "") for c in q.chunk_ids)
            if name == "B4":
                planted = set(" ".join(issues).split(" || ")) | set(issues)
                for f in analyse(chunks):
                    if f.kind in ("UNSUPPORTED_CLAIM", "LIMITATION", "CONTRADICTION"):
                        findings_n += 1
                        false_alarm += not any(f.sentence in p or p in f.sentence for p in planted)
        out[name] = {
            "issues_reached": round(reached_n / total, 3),
            "by_kind": {k: round(v[0] / v[1], 3) for k, v in by_kind.items()},
            "grounded_share": round(grounded_n / (len(seeds) * 12), 3),
            "quote_found_in_cited_chunk": round(grounded_ok / grounded_n, 3) if grounded_n else None,
        }
        if name == "B4":
            out[name]["finding_false_alarm_rate"] = round(false_alarm / findings_n, 3) if findings_n else None
    return out


def role_difference(seeds):
    """Share of category labels each role uses that no other role used, averaged over reports."""
    shares = []
    for seed in seeds:
        chunks, _ = report(seed, DEV)
        qs = plan(SESSION, analyse(chunks), per_role=3)
        cats = {r: {q.category for q in qs if q.role == r} for r in SESSION}
        for r in SESSION:
            others = set().union(*(cats[o] for o in SESSION if o != r))
            shares.append(len(cats[r] - others) / len(cats[r]) if cats[r] else 0)
    return round(sum(shares) / len(shares), 3)


def main(argv):
    mode = argv[1] if len(argv) > 1 else "pilot"
    seeds = {"pilot": PILOT_SEEDS, "final": FINAL_SEEDS}[mode]
    result = {"dev_phrasing": run(seeds, DEV), "role_unique_category_share": role_difference(seeds)}
    if mode == "final":
        result["held_out_phrasing"] = run(seeds, HELD_OUT)
    print(json.dumps(result, indent=2))
    out = Path(__file__).resolve().parent.parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"{mode}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
