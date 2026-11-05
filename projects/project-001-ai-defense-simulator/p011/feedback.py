"""Answer feedback by explicit criteria (architecture proposal: Feedback Model).

No overall score. Each item says which criterion it concerns, what it observed, and its basis:
"source" when it compares the answer with the user's own documents, "heuristic" when it is a
surface check of the answer text. Neither is a judgement of presentation quality (P001-C004).
"""
import re
from dataclasses import dataclass

HEDGES = re.compile(r"\b(might|may|likely|not sure|uncertain|limitation|only|depends|so far|in our tests|we did not)\b", re.I)
OVERCLAIM = re.compile(r"\b(always|never|guarantees?|proves?|perfect|100 ?%|completely|no risk)\b", re.I)
EVIDENCE = re.compile(r"(\b(table|figure|section|appendix|test|experiment|measured|data|results?|logs?)\b|\d)", re.I)
STOP = set("the a an and or of to in on for with is are was were be been it this that we our you your as by at from "
           "how what why which who can could should would does did do not no".split())


@dataclass(frozen=True)
class Item:
    criterion: str
    observation: str
    basis: str     # "source" or "heuristic"


def _words(text):
    return {w for w in re.findall(r"[a-z][a-z0-9-]+", text.lower()) if w not in STOP and len(w) > 2}


def _numbers(text):
    return {float(n) for n in re.findall(r"\b\d+(?:\.\d+)?\b", text)}


def evaluate(answer: str, question, source_texts: list[str]) -> list[Item]:
    items = []
    if len(answer.split()) < 8:
        items.append(Item("completeness", "The answer is very short; a reviewer will likely ask you to expand.", "heuristic"))
    if question.grounded and source_texts:
        source = " ".join(source_texts)
        overlap = _words(answer) & _words(question.quote)
        if overlap:
            items.append(Item("relevance", f"Uses the terms of the challenged sentence ({', '.join(sorted(overlap)[:5])}).", "source"))
        else:
            items.append(Item("relevance", "Does not use any of the key terms of the challenged sentence; check you answered it.", "source"))
        stray = _numbers(answer) - _numbers(source)
        if stray:
            items.append(Item("consistency", f"Mentions figures not found in your documents ({', '.join(str(int(n)) if n == int(n) else str(n) for n in sorted(stray))}). "
                              "Make sure they match what you wrote.", "source"))
    if EVIDENCE.search(answer):
        items.append(Item("evidence use", "Refers to data, tests or results.", "heuristic"))
    else:
        items.append(Item("evidence use", "Does not point to any data, test or result.", "heuristic"))
    if OVERCLAIM.search(answer):
        items.append(Item("unsupported statements", f"Uses absolute wording (\"{OVERCLAIM.search(answer).group(0)}\"); a reviewer may push back.", "heuristic"))
    if question.category in ("UNSUPPORTED_CLAIM", "LIMITATION", "CONTRADICTION") and not HEDGES.search(answer):
        items.append(Item("uncertainty", "This question invites you to state limits or uncertainty; the answer states none.", "heuristic"))
    return items
