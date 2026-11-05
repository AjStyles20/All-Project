"""Evidence-bounded diagnosis (Pass 001 claim states; research verdict: engineering only).

Deterministic rules, no language model. The tool proposes competing hypotheses, shows the
log lines for and against each, says which check would best separate the leaders, and
answers UNRESOLVED or INSUFFICIENT EVIDENCE when the logs cannot decide. Nothing here can
mark a cause VERIFIED: only a check result recorded by a person can (see session.py).
"""
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum


class State(str, Enum):
    OBSERVED = "OBSERVED"
    CORRELATED = "CORRELATED"
    HYPOTHESIZED = "HYPOTHESIZED"
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    VERIFIED = "VERIFIED"
    INSUFFICIENT = "INSUFFICIENT EVIDENCE"


@dataclass(frozen=True)
class Fault:
    key: str
    title: str
    patterns: tuple
    checks: tuple          # what a person could look at to confirm or rule it out


FAULTS = [
    Fault("db_pool", "Database connections exhausted",
          (r"too many (?:client )?connections", r"connection pool (?:is )?exhausted", r"timeout acquiring (?:a )?connection",
           r"could not obtain (?:a )?(?:database )?connection"),
          ("Check the database's active connection count and max_connections for the incident window.",
           "Check whether one service holds far more connections than usual (connection leak).")),
    Fault("downstream", "A downstream service is unavailable",
          (r"connection refused", r"no healthy upstream", r"upstream (?:\w+ )?(?:is )?unavailable", r"ECONNREFUSED", r"\b503\b"),
          ("Check the health and restart history of the service being called.",
           "Check whether calls that do not touch that service also failed.")),
    Fault("deploy", "A deployment or configuration change",
          (r"\bdeploy(?:ed|ment)?\b", r"config(?:uration)? (?:reloaded|changed|updated)", r"starting version", r"rolled out"),
          ("Compare the deployed version or config diff with the last healthy one.",
           "Roll back in a test environment and see whether the errors stop.")),
    Fault("disk", "Disk full", (r"no space left on device", r"disk (?:is )?full", r"ENOSPC"),
          ("Check free disk space on the affected host at the time.",)),
    Fault("memory", "Out of memory", (r"out of memory", r"OOMKilled", r"MemoryError", r"heap space", r"cannot allocate memory"),
          ("Check memory usage and container restarts (OOM kills) for the service.",)),
    Fault("cert", "Expired or invalid TLS certificate", (r"certificate (?:has )?expired", r"\bx509\b", r"certificate verify failed"),
          ("Check the certificate's expiry date on the endpoint being called.",)),
    Fault("dns", "DNS resolution failure", (r"no such host", r"name resolution", r"NXDOMAIN", r"could not resolve"),
          ("Resolve the failing host name from the affected service's network.",)),
    Fault("rate_limit", "Rate limiting by a dependency", (r"\b429\b", r"rate limit", r"too many requests"),
          ("Check the dependency's rate-limit dashboard or quota for the window.",)),
]
FAULT = {f.key: f for f in FAULTS}
_COMPILED = {f.key: [re.compile(p, re.I) for p in f.patterns] for f in FAULTS}

PRECEDE_GRACE = timedelta(seconds=10)      # a cause seen up to this long after onset still counts as "at onset"
EFFECT_AFTER = timedelta(seconds=60)       # first seen this long after onset: more likely an effect
DEPLOY_LOOKBACK = timedelta(minutes=15)
MIN_SUPPORT = 3


@dataclass
class Hypothesis:
    key: str
    title: str
    state: State
    first_seen: object
    count: int
    services: list
    supporting: list = field(default_factory=list)       # Events (first few)
    against: list = field(default_factory=list)          # reasons, each tied to evidence
    reasons: list = field(default_factory=list)
    checks: tuple = ()


@dataclass
class Diagnosis:
    onset: object
    window: tuple
    verdict: str
    summary: str
    hypotheses: list
    discriminating_checks: list
    missing: list
    stats: dict


def incident_onset(events):
    """Start of the first error spike that lasts at least two minutes above the quiet baseline.
    A single noisy minute is not an incident (found in the pilot: it made real causes look late)."""
    errors = [e for e in events if e.level >= 4]
    if not events or not errors:
        return None
    start = events[0].time.replace(second=0, microsecond=0)
    buckets = Counter(int((e.time - start).total_seconds() // 60) for e in errors)
    minutes = int((events[-1].time - start).total_seconds() // 60) + 1
    series = [buckets.get(m, 0) for m in range(minutes)]
    head = sorted(series[: max(1, minutes // 3)])
    baseline = head[len(head) // 2]
    threshold = max(3, 3 * baseline + 1)
    for m, n in enumerate(series):
        if n >= threshold and m + 1 < len(series) and series[m + 1] >= threshold:
            in_minute = [e for e in errors if int((e.time - start).total_seconds() // 60) == m]
            return in_minute[0].time
    return None


def _matches(fault_key, event):
    return any(p.search(event.message) for p in _COMPILED[fault_key])


def diagnose(events) -> Diagnosis:
    onset = incident_onset(events)
    services = sorted({e.service for e in events})
    stats = {"events": len(events), "services": services, "errors": sum(e.level >= 4 for e in events)}
    if onset is None:
        return Diagnosis(None, None, State.INSUFFICIENT.value, "No error spike was found, so there is no incident to explain.",
                         [], [], [], stats)
    window = (onset - DEPLOY_LOOKBACK, events[-1].time)
    before_templates = {e.template for e in events if e.time < onset and e.level >= 4}
    new_errors = [e for e in events if e.time >= onset and e.level >= 4 and e.template not in before_templates]

    hypotheses = []
    for f in FAULTS:
        hits = [e for e in events if window[0] <= e.time and _matches(f.key, e)]
        if f.key != "deploy":
            hits = [e for e in hits if e.level >= 3]
        if not hits:
            continue
        first = hits[0].time
        h = Hypothesis(f.key, f.title, State.HYPOTHESIZED, first, len(hits), sorted({e.service for e in hits}),
                       hits[:5], checks=f.checks)
        h.reasons.append(f"OBSERVED: {len(hits)} matching lines in {', '.join(h.services)}; first at {first:%H:%M:%S}.")
        lead = (onset - first).total_seconds()
        if f.key == "deploy":
            if first <= onset and lead <= DEPLOY_LOOKBACK.total_seconds():
                h.reasons.append(f"CORRELATED: change logged {int(lead)} s before the errors began.")
                if new_errors:
                    h.reasons.append(f"CORRELATED: {len({e.template for e in new_errors})} kinds of error appear only after it.")
                    h.state = State.SUPPORTED
                else:
                    h.state = State.CORRELATED
            else:
                h.state = State.CONTRADICTED
                h.against.append(f"The change was logged at {first:%H:%M:%S}, after the errors began at {onset:%H:%M:%S}.")
        elif first - onset > EFFECT_AFTER:
            h.state = State.CONTRADICTED
            h.against.append(f"First seen {int((first - onset).total_seconds())} s after the errors began: more likely an effect than the cause.")
        elif first <= onset + PRECEDE_GRACE and len(hits) >= MIN_SUPPORT:
            h.state = State.SUPPORTED
            h.reasons.append(f"CORRELATED: appears {'before' if lead > 0 else 'as'} the error spike begins ({int(lead)} s lead), {len(hits)} times.")
        else:
            h.state = State.CORRELATED
            h.reasons.append("CORRELATED: present during the incident, but not clearly before it.")
        hypotheses.append(h)

    order = {State.SUPPORTED: 0, State.CORRELATED: 1, State.HYPOTHESIZED: 2, State.CONTRADICTED: 3}
    hypotheses.sort(key=lambda h: (order[h.state], h.first_seen, -h.count))
    supported = [h for h in hypotheses if h.state is State.SUPPORTED]

    # Missing telemetry: a downstream failure names a service we have no logs from.
    missing = []
    for h in hypotheses:
        if h.key == "downstream":
            named = set()
            for e in h.supporting:
                named.update(re.findall(r"(?:to|upstream|calling)\s+([a-z][\w-]+)", e.message, re.I))
            # Names in messages rarely match log labels exactly ("payments-api" vs "payments").
            known = lambda n: any(n == x or n.startswith(x) or x.startswith(n) for x in services)
            for svc in sorted(n for n in named if not known(n) and n not in {"the", "a", "service"}):
                missing.append(f"No logs from '{svc}', which other services report as failing. Its own logs would show why.")

    checks = []
    if len(supported) == 1 and not missing:
        lead = supported[0]
        verdict = "LEADING HYPOTHESIS"
        summary = (f"Most consistent with: {lead.title}. This is SUPPORTED by the logs, not verified. "
                   f"Confirm it with: {lead.checks[0]}")
        checks = [lead.checks[0]]
    elif len(supported) >= 2:
        verdict = State.INSUFFICIENT.value if missing else "UNRESOLVED"
        a, b = supported[0], supported[1]
        summary = f"UNRESOLVED: both '{a.title}' and '{b.title}' fit the logs. Check which one explains the other."
        checks = [f"To separate them: {a.checks[0]}", f"... and: {b.checks[0]}",
                  f"Order of first signals: {a.title} at {a.first_seen:%H:%M:%S}, {b.title} at {b.first_seen:%H:%M:%S}. "
                  "An earlier signal is a better candidate for the cause, not proof."]
    else:
        verdict = State.INSUFFICIENT.value
        lead = hypotheses[0].title if hypotheses else None
        summary = ("INSUFFICIENT EVIDENCE: errors spiked, but no recognised cause clearly came first."
                   + (f" Closest candidate: {lead}." if lead else ""))
        checks = [c for h in hypotheses[:2] for c in h.checks[:1]]
    if missing:
        summary += " Some telemetry is missing; see below."
    return Diagnosis(onset, window, verdict, summary, hypotheses, checks, missing, stats)


def top_cause(d: Diagnosis):
    """The single cause this diagnosis asserts, or None when it abstains."""
    return d.hypotheses[0].key if d.verdict == "LEADING HYPOTHESIS" else None
