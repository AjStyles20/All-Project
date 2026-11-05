# Project 002 — AI-Powered Virtual Classroom and Adaptive Learning Environment

## Concept
A virtual learning environment in which users provide learning materials and interact with configurable AI teachers, tutors, or classroom personas. Candidate capabilities include lessons, questioning, explanations, discussion, different teaching styles, speech, classroom roles, and later richer visual interaction.

## Current stage
**First implementation (2026-11-05, DR-021): Phases 1–2 of Pass 017.** Deterministic trust kernel (APLDG) and mastery kernel (PGAIC), the SQL JOIN benchmark course, an evaluation against the Pass 017 gates, and a single-user web app. No language model is connected. Canonical ID: P006 (see `project-control/CANONICAL_PROJECT_INDEX.md`). Results: `docs/RESULTS.md`.

```bash
pip install -r requirements.txt
python -m pytest -q
PYTHONPATH=src python -m p002                   # opens the Learning World locally
PYTHONPATH=src python -m p002.evaluation final
```

## Research mandate
Establish the genuine lineage from teaching/learning technology through intelligent tutoring and conversational systems to modern RAG/generative-AI learning environments; map academic, commercial, and open-source prior art; identify counterexamples and novelty threats; establish user problems, feasibility, privacy/security/ethics, accessibility, cost, and defensible differentiation before architecture approval.

## Claim discipline
No “first”, “unique”, or “no existing system” claim without sufficient evidence. Record facts, inferences, hypotheses, unknowns, and contrary evidence separately.
