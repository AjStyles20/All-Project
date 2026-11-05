"""Reviewer roles and question generation (architecture proposal: Reviewer/Persona Model).

A role is a policy, not a fictional person: which findings it cares about, in what order,
and how it phrases the challenge. Each question carries the sentence and chunk that
motivated it. When nothing in the documents fits, the role asks a general question and
marks it as not grounded.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    key: str
    name: str
    purpose: str
    priorities: tuple       # finding kinds, most important first
    general: tuple          # questions used when the documents give nothing to challenge


ROLES = {r.key: r for r in [
    Role("technical", "Technical reviewer", "Probes how the system works and whether requirements are met",
         ("REQUIREMENT", "UNSUPPORTED_CLAIM", "METHOD", "CONTRADICTION"),
         ("Walk me through the main components and how data moves between them.",)),
    Role("methodology", "Methodology reviewer", "Probes how results were obtained and whether they support the claims",
         ("METHOD", "QUANTIFIED_CLAIM", "CONTRADICTION", "LIMITATION"),
         ("How did you decide what to measure, and what would have counted as failure?",)),
    Role("skeptic", "Evidence reviewer", "Challenges claims that go beyond the evidence",
         ("UNSUPPORTED_CLAIM", "CONTRADICTION", "QUANTIFIED_CLAIM", "LIMITATION"),
         ("Which of your claims are you least sure of, and why?",)),
    Role("security", "Security and privacy reviewer", "Probes data handling, access and failure modes",
         ("SECURITY", "REQUIREMENT", "LIMITATION"),
         ("What personal or sensitive data does your system handle, and who can see it?",)),
]}

TEMPLATES = {
    "UNSUPPORTED_CLAIM": "You write \"{s}\" The word \"{d}\" is a strong claim. What evidence supports it, and against what was it compared?",
    "QUANTIFIED_CLAIM": "You report \"{s}\" How was this measured, on what data, and how confident are you in the number?",
    "CONTRADICTION": "Your documents disagree: {d}. Here you write \"{s}\" Which figure is correct, and why do they differ?",
    "LIMITATION": "You acknowledge \"{s}\" How much does this limit your conclusions, and what would it take to address it?",
    "REQUIREMENT": "You state \"{s}\" How did you verify that this requirement is met? What test shows it?",
    "METHOD": "About your method: \"{s}\" Why this choice, and what would change your results?",
    "SECURITY": "On \"{s}\" How is this protected, who can access it, and what happens if it leaks?",
}


@dataclass(frozen=True)
class Question:
    role: str
    category: str
    text: str
    chunk_ids: tuple
    quote: str
    grounded: bool


def plan(roles, findings, per_role=3) -> list[Question]:
    """Questions for each chosen role, highest-priority findings first, no sentence asked twice."""
    asked, out = set(), []
    for key in roles:
        role = ROLES[key]
        mine = []
        for kind in role.priorities:
            for f in findings:
                if f.kind == kind and (f.sentence, f.kind) not in asked and len(mine) < per_role:
                    asked.add((f.sentence, f.kind))
                    chunks = (f.chunk_id,) + ((f.other_chunk_id,) if f.other_chunk_id else ())
                    mine.append(Question(key, kind, TEMPLATES[kind].format(s=f.sentence, d=f.detail), chunks, f.sentence, True))
        for text in role.general:
            if len(mine) < per_role:
                mine.append(Question(key, "GENERAL", text, (), "", False))
        out += mine
    return out
