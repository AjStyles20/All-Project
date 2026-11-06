"""Transparent founder-investor matching (Pass 003 product scope).

Each criterion is scored separately and shown with its reason. Missing data is UNKNOWN, not
zero: it is left out of the average and lowers confidence instead of counting against anyone.
An investor's declared thesis is compared with what their recent deals show.

A match score describes relevance to an investor's stated and observed focus. It is not a
prediction of investment quality or of the chance of being funded.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta

STAGES = ["pre-seed", "seed", "series-a", "series-b", "growth"]
STALE_AFTER = timedelta(days=180)
REVEALED_WINDOW = timedelta(days=3 * 365)
DISCLAIMER = ("Match scores show how closely a profile fits an investor's stated and recent focus. "
              "They do not predict investment quality or the chance of funding.")


@dataclass(frozen=True)
class Startup:
    id: int
    name: str
    sector: str | None
    stage: str | None
    country: str | None
    raising: int | None            # amount sought, in whole currency units
    updated: date


@dataclass(frozen=True)
class Deal:
    company: str
    sector: str
    stage: str
    on: date
    source: str                    # where the fact comes from (link or description)
    verified: date | None          # when someone last checked it


@dataclass(frozen=True)
class Investor:
    id: int
    name: str
    sectors: tuple                 # declared
    stages: tuple
    countries: tuple
    check_min: int | None
    check_max: int | None
    deals: tuple = ()
    updated: date = date.min


@dataclass
class Component:
    name: str
    score: float | None            # 0..1, None = unknown
    reason: str


@dataclass
class Match:
    investor_id: int
    startup_id: int
    score: float | None
    confidence: str                # high / medium / low
    components: list
    warnings: list = field(default_factory=list)


def _fit_set(name, value, declared, label, plural):
    if not value:
        return Component(name, None, f"The startup has not given its {label}.")
    if not declared:
        return Component(name, None, f"The investor has not stated a {label} preference.")
    ok = value in declared
    return Component(name, 1.0 if ok else 0.0,
                     f"{value} is {'' if ok else 'not '}among the stated {plural} ({', '.join(declared)}).")


def _fit_stage(stage, declared):
    if not stage:
        return Component("stage", None, "The startup has not given its stage.")
    if not declared:
        return Component("stage", None, "The investor has not stated a stage preference.")
    if stage in declared:
        return Component("stage", 1.0, f"{stage} is a stated stage.")
    gap = min(abs(STAGES.index(stage) - STAGES.index(s)) for s in declared if s in STAGES)
    score = 0.5 if gap == 1 else 0.0
    return Component("stage", score, f"{stage} is {gap} stage{'s' if gap > 1 else ''} from the nearest stated stage.")


def _fit_check(raising, lo, hi):
    if raising is None:
        return Component("cheque size", None, "The startup has not said how much it is raising.")
    if lo is None and hi is None:
        return Component("cheque size", None, "The investor has not stated a cheque size.")
    lo, hi = lo or 0, hi or raising
    # A typical round has several investors: a cheque between 10 % and 100 % of the round fits.
    if hi >= raising * 0.1 and lo <= raising:
        return Component("cheque size", 1.0, f"Cheques of {lo:,}–{hi:,} fit a raise of {raising:,}.")
    return Component("cheque size", 0.0, f"Cheques of {lo:,}–{hi:,} do not fit a raise of {raising:,}.")


def revealed(investor: Investor, today: date):
    """What recent deals show: share of deals per sector and per stage in the last three years."""
    recent = [d for d in investor.deals if today - d.on <= REVEALED_WINDOW]
    sectors, stages = {}, {}
    for d in recent:
        sectors[d.sector] = sectors.get(d.sector, 0) + 1
        stages[d.stage] = stages.get(d.stage, 0) + 1
    return recent, sectors, stages


def says_vs_does(investor: Investor, today: date) -> list:
    """Disagreements between the declared thesis and recent deals (needs at least four deals)."""
    recent, sectors, stages = revealed(investor, today)
    notes = []
    if len(recent) < 4:
        return notes
    off_stage = sum(n for s, n in stages.items() if s not in investor.stages)
    if investor.stages and off_stage / len(recent) >= 0.5:
        top = max(stages, key=stages.get)
        notes.append(f"States {', '.join(investor.stages)}, but {off_stage} of the last {len(recent)} deals were outside that "
                     f"(most often {top}).")
    off_sector = sum(n for s, n in sectors.items() if s not in investor.sectors)
    if investor.sectors and off_sector / len(recent) >= 0.5:
        top = max(sectors, key=sectors.get)
        notes.append(f"States {', '.join(investor.sectors)}, but {off_sector} of the last {len(recent)} deals were in other "
                     f"sectors (most often {top}).")
    return notes


def match(startup: Startup, investor: Investor, today: date) -> Match:
    comps = [
        _fit_set("sector", startup.sector, investor.sectors, "sector", "sectors"),
        _fit_stage(startup.stage, investor.stages),
        _fit_set("region", startup.country, investor.countries, "country", "countries"),
        _fit_check(startup.raising, investor.check_min, investor.check_max),
    ]
    recent, sectors, stages = revealed(investor, today)
    if len(recent) >= 2 and startup.sector and startup.stage:
        alike = sum(1 for d in recent if d.sector == startup.sector and d.stage == startup.stage)
        near = sum(1 for d in recent if d.sector == startup.sector)
        score = min(1.0, (alike + 0.5 * (near - alike)) / max(2, len(recent) * 0.3))
        comps.append(Component("recent deals", round(score, 2),
                               f"{alike} of {len(recent)} deals in the last 3 years were {startup.sector} at {startup.stage}; "
                               f"{near} were {startup.sector}."))
    else:
        comps.append(Component("recent deals", None, "Too few recorded deals to compare with."))

    known = [c.score for c in comps if c.score is not None]
    score = round(sum(known) / len(known), 2) if known else None
    warnings = says_vs_does(investor, today)
    if today - investor.updated > STALE_AFTER:
        warnings.append(f"The investor profile was last updated on {investor.updated:%d %b %Y}; it may be out of date.")
    if today - startup.updated > STALE_AFTER:
        warnings.append(f"The startup profile was last updated on {startup.updated:%d %b %Y}.")
    unverified = [d for d in recent if d.verified is None or today - d.verified > STALE_AFTER]
    if unverified:
        warnings.append(f"{len(unverified)} of the recent deals have not been verified in the last 6 months.")
    confidence = "high" if len(known) >= 4 and not warnings else "medium" if len(known) >= 3 else "low"
    if any(c.name == "sector" and c.score == 0.0 for c in comps):
        warnings.append("Outside the stated sectors.")
    return Match(investor.id, startup.id, score, confidence, comps, warnings)


def rank(startup, investors, today, include_unknown=True):
    """Best fits first; matches with no known criteria last. Ties keep a stable, name-based order."""
    results = [match(startup, inv, today) for inv in investors]
    names = {inv.id: inv.name for inv in investors}
    results.sort(key=lambda m: (m.score is None, -(m.score or 0), names[m.investor_id]))
    return results if include_unknown else [m for m in results if m.score is not None]
