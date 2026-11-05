"""Finds what a reviewer would challenge in the user's own documents.

Deterministic rules, no model: every finding points at one sentence in one chunk, so the
question built from it is grounded by construction and can be checked by a person.
"""
import re
from dataclasses import dataclass

from p011.ingest import sentences

STRONG = re.compile(r"\b(first|novel|unique|state[- ]of[- ]the[- ]art|significantly|outperforms?|proves?|guarantees?|"
                    r"always|never|eliminates?|robust|secure|scalable|real[- ]time|improves?|better than|best)\b", re.I)
EVIDENCE = re.compile(r"(\[\d+\]|\([A-Z][A-Za-z-]+(?: et al\.)?,? \d{4}\)|\b(table|figure|fig\.|appendix|section) \d|"
                      r"\bp ?[<=] ?0\.\d|\bn ?= ?\d|\d+(\.\d+)? ?%)", re.I)
LIMIT = re.compile(r"\b(limitation|limited to|only (?:tested|evaluated|works)|not yet|future work|however|"
                   r"does not (?:support|handle)|out of scope|small sample)\b", re.I)
REQUIREMENT = re.compile(r"\b(must|shall|is required to|needs to)\b", re.I)
METHOD = re.compile(r"\b(we (?:used|use|evaluated|evaluate|measured|collected|trained|surveyed|interviewed)|dataset|"
                    r"participants?|sample of|baseline|experiment)\b", re.I)
SECURITY = re.compile(r"\b(password|personal data|api key|token|upload|encrypt\w*|authentication|login|"
                      r"gdpr|privacy|student data)\b", re.I)
METRIC = re.compile(r"\b(accuracy|precision|recall|f1(?: score)?|latency|response time|error rate|uptime|"
                    r"satisfaction|throughput|users|participants|response rate)\b[^.0-9]{0,40}?(\d+(?:\.\d+)?)\s?(%|ms|s\b|seconds)?",
                    re.I)


@dataclass(frozen=True)
class Finding:
    kind: str           # UNSUPPORTED_CLAIM, QUANTIFIED_CLAIM, CONTRADICTION, LIMITATION, REQUIREMENT, METHOD, SECURITY
    chunk_id: str
    sentence: str
    detail: str = ""
    other_chunk_id: str = ""


def analyse(chunks) -> list[Finding]:
    """chunks: [(chunk_id, text)]"""
    findings, metrics = [], {}
    for chunk_id, text in chunks:
        for s in sentences(text):
            if STRONG.search(s):
                kind = "QUANTIFIED_CLAIM" if EVIDENCE.search(s) else "UNSUPPORTED_CLAIM"
                findings.append(Finding(kind, chunk_id, s, STRONG.search(s).group(0)))
            if LIMIT.search(s):
                findings.append(Finding("LIMITATION", chunk_id, s, LIMIT.search(s).group(0)))
            if REQUIREMENT.search(s):
                findings.append(Finding("REQUIREMENT", chunk_id, s))
            if METHOD.search(s):
                findings.append(Finding("METHOD", chunk_id, s, METHOD.search(s).group(0)))
            if SECURITY.search(s):
                findings.append(Finding("SECURITY", chunk_id, s, SECURITY.search(s).group(0)))
            for m in METRIC.finditer(s):
                key = m.group(1).lower().replace("response time", "latency")
                metrics.setdefault(key, []).append((float(m.group(2)), (m.group(3) or "").lower(), chunk_id, s))
    for key, values in metrics.items():
        first = values[0]
        for other in values[1:]:
            if other[1] == first[1] and other[0] != first[0] and other[2] != first[2]:
                findings.append(Finding("CONTRADICTION", other[2], other[3],
                                        f"{key}: {_num(first[0])}{first[1]} elsewhere, {_num(other[0])}{other[1]} here",
                                        first[2]))
                break
    return findings


def _num(x):
    return str(int(x)) if x == int(x) else str(x)
