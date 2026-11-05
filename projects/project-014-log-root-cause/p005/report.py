"""Session file (recorded checks) and the HTML report.

Only a check result recorded by a named person can make a hypothesis VERIFIED or rule it
out. The report shows every hypothesis with the log lines behind it (file and line number),
what speaks against it, and what to check next. All log text is HTML-escaped.
"""
import html
import json
from datetime import datetime, timezone
from pathlib import Path

from p005.diagnose import FAULT, State


def new_session(paths, diagnosis):
    return {"version": 1, "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "logs": [str(p) for p in paths], "checks": []}


def record(session, hypothesis, check, result, by):
    if hypothesis not in FAULT:
        raise ValueError(f"Unknown hypothesis '{hypothesis}'. Choose from: {', '.join(FAULT)}.")
    if result not in ("confirms", "refutes"):
        raise ValueError("Result must be 'confirms' or 'refutes'.")
    if not by.strip():
        raise ValueError("Say who ran the check (--by).")
    session["checks"].append({"hypothesis": hypothesis, "check": check.strip()[:500], "result": result,
                              "by": by.strip()[:80], "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    return session


def apply_checks(diagnosis, session):
    """Recorded checks override log-based states: confirms -> VERIFIED, refutes -> CONTRADICTED."""
    for c in session.get("checks", []):
        for h in diagnosis.hypotheses:
            if h.key == c["hypothesis"]:
                if c["result"] == "confirms":
                    h.state = State.VERIFIED
                    h.reasons.append(f"VERIFIED by {c['by']} at {c['at']}: {c['check']}")
                else:
                    h.state = State.CONTRADICTED
                    h.against.append(f"Ruled out by {c['by']} at {c['at']}: {c['check']}")
    verified = [h for h in diagnosis.hypotheses if h.state is State.VERIFIED]
    if len(verified) == 1:
        diagnosis.verdict = "VERIFIED CAUSE"
        diagnosis.summary = f"VERIFIED: {verified[0].title}, by a recorded check (not by this tool)."
    elif len(verified) > 1:
        diagnosis.verdict = "MULTIPLE VERIFIED"
        diagnosis.summary = "More than one cause has been confirmed by recorded checks; the incident may have several causes."
    return diagnosis


def save(path, session):
    Path(path).write_text(json.dumps(session, indent=2), encoding="utf-8")


def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("checks"), list):
        raise ValueError("Not a P005 session file.")
    return data


def text_summary(d):
    out = [d.summary, ""]
    if d.onset:
        out.append(f"Errors began: {d.onset:%Y-%m-%d %H:%M:%S %Z}   ({d.stats['events']} events, {d.stats['errors']} errors, "
                   f"services: {', '.join(d.stats['services'])})")
    for h in d.hypotheses:
        out.append(f"  [{h.state.value}] {h.title}: {h.count} lines, first {h.first_seen:%H:%M:%S}")
        for e in h.supporting[:2]:
            out.append(f"      {e.source}:{e.line}  {e.message[:110]}")
        for a in h.against:
            out.append(f"      against: {a}")
    if d.discriminating_checks:
        out += ["", "Next checks:"] + [f"  - {c}" for c in d.discriminating_checks]
    if d.missing:
        out += ["", "Missing evidence:"] + [f"  - {m}" for m in d.missing]
    return "\n".join(out)


def html_report(d, session):
    e = html.escape
    rows = []
    for h in d.hypotheses:
        lines = "".join(f"<li><code>{e(x.source)}:{x.line}</code> <span class='meta'>{x.time:%H:%M:%S} {e(x.service)} "
                        f"{e(x.level_name)}</span> {e(x.message)}</li>" for x in h.supporting)
        reasons = "".join(f"<li>{e(r)}</li>" for r in h.reasons)
        against = "".join(f"<li>{e(a)}</li>" for a in h.against) or "<li class='meta'>Nothing found against it yet.</li>"
        checks = "".join(f"<li>{e(c)}</li>" for c in h.checks)
        rows.append(f"""<section class="card"><h3>{e(h.title)} <span class="state s-{h.state.name.lower()}">{e(h.state.value)}</span></h3>
<h4>Why it is on the list</h4><ul>{reasons}</ul>
<h4>Log lines</h4><ul class="lines">{lines}</ul>
<h4>Against it</h4><ul>{against}</ul>
<h4>How to confirm or rule it out</h4><ul>{checks}</ul>
<p class="meta">Record a result: <code>python -m p005 record SESSION --hypothesis {e(h.key)} --result confirms|refutes --check "..." --by NAME</code></p></section>""")
    next_checks = "".join(f"<li>{e(c)}</li>" for c in d.discriminating_checks)
    missing = "".join(f"<li>{e(m)}</li>" for m in d.missing)
    recorded = "".join(f"<li>{e(c['at'])} {e(c['by'])}: {e(c['result'])} <b>{e(c['hypothesis'])}</b> — {e(c['check'])}</li>"
                       for c in session.get("checks", [])) or "<li class='meta'>None yet.</li>"
    onset = f"{d.onset:%Y-%m-%d %H:%M:%S %Z}" if d.onset else "no incident found"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>Incident report</title><style>
:root{{--bg:#fff;--fg:#1b1d21;--muted:#5a6070;--card:#f4f5f7;--line:#d6d9e0;--ok:#1d6b35;--bad:#a01c1c;--warn:#8a4b00}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15171b;--fg:#e8eaee;--muted:#a2a8b6;--card:#1f2228;--line:#343843;--ok:#7fd49a;--bad:#ff8a8a;--warn:#ffbf66}}}}
body{{margin:0;font:16px/1.5 system-ui,sans-serif;background:var(--bg);color:var(--fg)}}main{{max-width:1000px;margin:0 auto;padding:0 16px 32px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 16px;margin:12px 0}}
.meta{{color:var(--muted)}}code{{font-size:.85em;word-break:break-all}}.lines li{{margin:4px 0}}
.state{{font-size:.8rem;border:1px solid currentColor;border-radius:4px;padding:1px 6px;margin-left:6px}}
.s-supported,.s-verified{{color:var(--ok)}}.s-contradicted{{color:var(--bad)}}.s-correlated,.s-hypothesized{{color:var(--warn)}}
.verdict{{font-size:1.1rem;font-weight:600}}</style></head><body><main>
<h1>Incident report</h1>
<p class="verdict">{e(d.summary if d.summary.upper().startswith(d.verdict.split()[0]) else d.verdict + ": " + d.summary)}</p>
<p class="meta">Errors began: {e(onset)}. {d.stats['events']} events, {d.stats['errors']} errors, services: {e(', '.join(d.stats['services']))}.
Logs: {e(', '.join(session.get('logs', [])))}. Secrets, e-mail addresses and long numbers are redacted.</p>
<p class="meta">States: OBSERVED in the logs → CORRELATED in time → SUPPORTED (appears before the errors, repeatedly) → VERIFIED only by a recorded check. CONTRADICTED means evidence speaks against it.</p>
<h2>Next checks</h2><ul>{next_checks or "<li class='meta'>None.</li>"}</ul>
{f"<h2>Missing evidence</h2><ul>{missing}</ul>" if missing else ""}
<h2>Hypotheses</h2>{''.join(rows) or "<p class='meta'>No recognised cause signals in the logs.</p>"}
<h2>Recorded checks</h2><ul>{recorded}</ul>
</main></body></html>"""
