# AJ Project OS

A reusable AI-assisted project-development operating system for academic and software projects.

## Purpose

AJ Project OS coordinates research, engineering, verification, documentation, and defense preparation without allowing any agent to silently redefine the project.

## Core Principles

- Inspect before modifying.
- Never invent project state, metrics, integrations, results, or evidence.
- Preserve approved architecture unless a change is justified and authorized.
- Simulation must always be labelled as simulation.
- Implementation is not the same as verification.
- Documentation must match the actual implementation and evidence.
- Significant project-changing decisions require AJ approval.
- Every agent must leave a structured handoff.

## Main Directories

- `project-control/` — canonical project state, decisions, requirements, evidence, limitations, and handoffs.
- `agent-instructions/` — role instructions for orchestrator, research, engineering, verification, documentation, defense, and AJ Tutor.
- `research/` — research outputs and literature evidence.
- `docs/` — academic and technical documentation.
- `src/` — implementation source code for instantiated projects.
- `tests/` — automated and manual verification assets.
- `defense/` — defense preparation materials.

## Canonical Project Identity

Project IDs were renumbered on 10 September 2026 while historical GitHub and Google Drive folder names were preserved for provenance. Before interpreting any historical `P###` folder or document, read `project-control/CANONICAL_PROJECT_INDEX.md`. That index is the authoritative old-ID → current-ID migration map and records the latest verified documentation state and important evidence warnings.

Do not infer current project identity from a historical folder name alone.

## Authority Levels

- **A0 Observe** — inspect, research, review.
- **A1 Routine Execution** — safe implementation, fixes, tests, comments, internal refactors.
- **A2 Significant Change** — meaningful implementation decisions requiring Project Lead review.
- **A3 Project-Changing** — title, objectives, methodology, core stack, ML target, major subsystem removal, destructive restructuring. Requires AJ approval.

## Definition of Done

- **D0** Not started
- **D1** Designed
- **D2** Implemented
- **D3** Unit tested
- **D4** Integrated
- **D5** Live verified
- **D6** Documentation aligned
- **D7** Defense ready

The canonical operating rules are in `project-control/PROJECT_RULES.md`.
