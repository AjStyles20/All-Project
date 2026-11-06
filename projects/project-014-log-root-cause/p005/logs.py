"""Log parsing, redaction and templating.

Logs are untrusted input (Pass 001 security requirements): lines are only ever matched and
displayed, never executed or followed as instructions; secrets are redacted before anything
is stored or shown; file sizes and line lengths are bounded.

Accepted formats, per line:
  2026-11-05T10:00:01Z ERROR [orders] message ...         (ISO time, level, [service])
  2026-11-05 10:00:01,123 WARN orders: message ...         (space-separated time, "service:")
  {"ts": "...", "level": "...", "service": "...", "msg": "..."}   (JSON lines)
"""
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

MAX_FILE_BYTES = 50 * 1024 * 1024
MAX_LINE = 4000
LEVELS = {"TRACE": 0, "DEBUG": 1, "INFO": 2, "NOTICE": 2, "WARN": 3, "WARNING": 3, "ERROR": 4, "CRITICAL": 5, "FATAL": 5}

TEXT_LINE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?)\s+"
    r"(?P<level>[A-Za-z]+)\s+(?:\[(?P<svc1>[\w.-]+)\]|(?P<svc2>[\w.-]+):)\s*(?P<msg>.*)$")

REDACTIONS = [
    (re.compile(r"(?i)\b(password|passwd|pwd|secret|token|api[_-]?key|authorization)\b(\s*[=:]\s*|\s+)(\"[^\"]*\"|'[^']*'|\S+)"),
     lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]+=*"), lambda m: "Bearer [REDACTED]"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}"), lambda m: "[REDACTED-JWT]"),
    (re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), lambda m: "[REDACTED-AWS-KEY]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), lambda m: "[EMAIL]"),
    (re.compile(r"\b\d{13,19}\b"), lambda m: "[NUMBER]"),            # card-like digit runs
]

TEMPLATE_RULES = [
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "<uuid>"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?\b"), "<ip>"),
    (re.compile(r"\b0x[0-9a-f]+\b|\b[0-9a-f]{12,}\b", re.I), "<hex>"),
    (re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?(?:ms|s|MB|KB|GB|%)?(?![A-Za-z])"), "<n>"),
    (re.compile(r"\"[^\"]{0,200}\""), "<str>"),
]


@dataclass(frozen=True)
class Event:
    source: str        # file name
    line: int          # 1-based line number in that file
    time: datetime
    level: int
    level_name: str
    service: str
    message: str       # redacted
    template: str


def redact(text: str) -> str:
    for pattern, repl in REDACTIONS:
        text = pattern.sub(repl, text)
    return text


def template(message: str) -> str:
    for pattern, repl in TEMPLATE_RULES:
        message = pattern.sub(repl, message)
    return " ".join(message.split())[:300]


def _time(text):
    text = text.replace(",", ".").replace(" ", "T", 1)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    t = datetime.fromisoformat(text)
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def parse_line(source, number, raw):
    raw = raw.rstrip("\r\n")[:MAX_LINE]
    if not raw.strip():
        return None
    ts = level = service = message = None
    if raw.lstrip().startswith("{"):
        try:
            obj = json.loads(raw)
            ts = obj.get("ts") or obj.get("time") or obj.get("timestamp")
            level = obj.get("level") or obj.get("severity") or "INFO"
            service = obj.get("service") or obj.get("svc") or obj.get("app") or "unknown"
            message = obj.get("msg") or obj.get("message") or ""
        except (ValueError, AttributeError):
            return None
    else:
        m = TEXT_LINE.match(raw)
        if not m:
            return None
        ts, level = m.group("ts"), m.group("level")
        service, message = m.group("svc1") or m.group("svc2"), m.group("msg")
    try:
        time = _time(str(ts))
    except ValueError:
        return None
    level_name = str(level).upper()
    clean = redact(str(message))
    return Event(source, number, time, LEVELS.get(level_name, 2), level_name, str(service)[:60], clean, template(clean))


def read_file(path) -> tuple[list[Event], int]:
    """Events from one file, plus the number of lines that could not be parsed."""
    path = Path(path)
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"{path.name} is larger than 50 MB.")
    events, skipped = [], 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for n, raw in enumerate(f, 1):
            e = parse_line(path.name, n, raw)
            if e is None:
                skipped += bool(raw.strip())
            else:
                events.append(e)
    return events, skipped


def read_all(paths) -> tuple[list[Event], dict]:
    events, skipped = [], {}
    for p in paths:
        ev, sk = read_file(p)
        events += ev
        skipped[Path(p).name] = sk
    events.sort(key=lambda e: (e.time, e.source, e.line))
    return events, skipped
