# Project 001 — AI Virtual Audience / Presentation & Defense Simulator

## Purpose
Build and evaluate an AI-assisted presentation, viva, interview, and project-defense practice system that can use uploaded source materials to generate context-aware questions, simulate panel/audience roles, capture user responses, and provide transparent feedback.

## Status
**First version (2026-11-05, DR-021).** Canonical ID P011 (this folder is legacy P001). The research verdict is unchanged: parked as an independent FYP, mechanism family merged with P001. Built as a product following `docs/technical/ARCHITECTURE_PROPOSAL.md`: upload your own documents, see what a reviewer would challenge, practise role-based questions grounded in quoted sentences, and get criterion-by-criterion feedback. No AI provider is connected; question generation is rule-based. Results: `docs/RESULTS.md` (the rules do not generalise to new wording).

```bash
pip install -r requirements.txt
python -m pytest -q
python -m p011                    # opens the app locally
python -m p011.evaluation final
```

## Governance
This project inherits the repository-level `project-control/PROJECT_RULES.md` and agent instructions. Project-specific truth lives in this folder's `project-control/` files.

## Initial Product Boundary
The first defensible MVP should focus on:
- source-grounded question generation from user-provided documents/slides;
- configurable audience/panel personas;
- text and microphone-based practice sessions where feasible;
- response capture and session history;
- transparent feedback with clearly defined metrics or rubric criteria;
- clear distinction between implemented, simulated, planned, and unsupported capabilities.

Features such as advanced avatars, real-time computer vision, emotion recognition, complex voice cloning, and high-fidelity animated classrooms are not assumed to be MVP requirements. They must pass scope review before implementation.

## Project Owner
AJ
