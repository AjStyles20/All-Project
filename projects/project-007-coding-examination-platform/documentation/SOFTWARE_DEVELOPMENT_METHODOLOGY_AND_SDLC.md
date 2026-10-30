# P001 Software Development Methodology and SDLC

## Status
Canonical full-development methodology. This document governs product development around the frozen P001 research experiment. It does not change the external-human-evidence protocol or manufacture research results.

## 1. Development methodology
P001 uses an **Agile iterative and incremental Software Development Life Cycle (SDLC)** with explicit research/change-control gates.

This is not claimed to be formal Scrum: the project has not consistently used Scrum roles, ceremonies, or time-boxed team sprints. Instead, development proceeds in small, testable increments with requirements traceability, Git version control, automated tests, review gates, and documentation updates.

### Iteration loop
1. Select a bounded requirement from the product backlog.
2. Confirm research-boundary compatibility.
3. Refine analysis and design.
4. Implement the smallest coherent increment.
5. Add or update unit, integration, and end-to-end tests.
6. Run continuous integration (CI).
7. Review behavior, security, usability, and traceability.
8. Update technical and academic documentation.
9. Accept, revise, or reject the increment before the next iteration.

## 2. Why not pure Waterfall?
A pure sequential Waterfall process does not accurately describe this project. Requirements and mechanisms were refined after literature review, prior-art attack, falsification planning, prototype implementation, and testing. The project therefore needs controlled iteration. Waterfall-style phase artifacts are still retained where useful: requirements, system design, implementation, testing, deployment, and maintenance documentation.

## 3. SDLC phases
### 3.1 Planning and feasibility
Define problem, stakeholders, scope, constraints, research contribution, hardware/software feasibility, completion risks, and ethical/security boundaries.

### 3.2 Requirements analysis
Maintain functional requirements, non-functional requirements, actor definitions, use cases, business rules, research invariants, acceptance criteria, and a Requirements Traceability Matrix (RTM).

### 3.3 System design
Maintain system architecture, module/component design, data model and Entity-Relationship Diagram (ERD), use-case model, activity diagrams, sequence diagrams, Data Flow Diagrams (DFD), deployment design, and user-interface wireframes.

### 3.4 Implementation
Build the product as separable layers: presentation/interface, application/API, domain/evidence engine, persistence, research/evaluation adapters, and infrastructure. Research-critical rules remain isolated from convenience/UI code.

### 3.5 Verification and validation
Use unit tests, integration tests, end-to-end tests, security tests, usability/acceptance tests, and the separately governed research evaluation. Software correctness must not be reported as scientific validation.

### 3.6 Deployment
Provide reproducible environment setup, configuration management, database initialization/migration, local demonstration deployment, logging, backup/recovery guidance, and documented external-service requirements.

### 3.7 Maintenance and evolution
Use Git history, issues/requirements, CI, semantic change control, documentation synchronization, defect repair, dependency maintenance, and versioned extensions.

## 4. Definition of Done for a development increment
An increment is complete only when its requirement and acceptance criteria are explicit; design impact is recorded; implementation is committed; appropriate tests exist and pass in CI; security/data implications are reviewed; documentation and RTM are updated; and frozen research definitions have not been silently altered.

## 5. Research/product boundary
The EGPCV research mechanism remains a controlled subsystem. Full-product development may add authentication, examination management, user interfaces, administration, reporting, deployment, and other product capabilities, but those additions do not constitute evidence that EGPCV is scientifically superior. Human assessor evidence remains external and must be collected under the frozen protocol.

## 6. Documentation synchronization rule
Every material implementation increment must update the affected requirements, diagrams/design description, RTM, test evidence, and work/change log in the same development cycle.
