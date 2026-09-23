# P001 Diagram Register

This register is the canonical index for system-analysis/design diagrams. Diagram source and rendered figures must describe implemented or explicitly labelled target-state behavior.

## Current diagram set
1. High-Level System Architecture — target full-product architecture.
2. Use Case Diagram — Candidate, Examiner, Administrator, Independent Assessor.
3. Activity Diagram — candidate examination workflow.
4. Sequence Diagram — login and protected-resource access.
5. Data Flow Diagram (DFD) Level 0 — external actors, platform, MySQL, file/evidence storage and execution boundary.
6. Entity-Relationship Diagram (ERD) — operational main-table logical model; physical MySQL schema will be refined through migrations.
7. Component Diagram — frontend, FastAPI modules, EGPCV engine, persistence and external execution boundary.
8. Deployment Diagram — browser/client, application server, MySQL server and supporting storage/tool boundary.
9. Class Diagram — key full-product domain classes.

## Figure placement
The figures belong in the System Analysis and Design / Methodology documentation immediately after the prose section they explain. They must not be presented as evidence that every target-state module is already implemented. The work log and RTM determine implementation status.

## Database notation warning
The ERD is currently a design baseline. FD-01 physically implements users, user_roles and auth_sessions in the existing development schema. The remaining operational entities become physical MySQL tables incrementally beginning with the MySQL migration and FD-02.
