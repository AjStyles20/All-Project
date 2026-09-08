# AJ Project OS — Technology and Platform Selection Standard

## Purpose
This standard defines how programming languages, frameworks, databases, frontend technologies, and delivery platforms are chosen for projects managed under AJ Project OS.

The goal is not to force every project into one stack. The goal is to prefer technologies AJ can understand, maintain, explain, test, and extend, while allowing a different stack when the project genuinely requires it.

## 1. Default Language Policy
Python is the default primary programming language for new Project OS projects when it is technically appropriate.

Reasons:
- AJ prefers Python and has existing practical experience with it.
- Python is well suited to AI/ML, data processing, automation, backend APIs, research prototypes, document processing, and rapid product development.
- Python generally produces a smaller conceptual and tooling burden for current Project OS work than introducing a new primary language without need.

Python-first does not mean Python-only.

Other languages may be selected when they provide a clear project-level advantage:
- JavaScript/TypeScript for substantial browser-side applications and frontend ecosystems.
- C# for .NET-centric desktop, web, enterprise, or Windows-integrated applications.
- Java for JVM/Android/enterprise requirements where it is a better fit.
- C/C++ for embedded, systems, performance-critical, hardware-near, game-engine, or low-level work.
- HTML/CSS/JavaScript remain normal web-layer technologies even when Python is the backend language.

A language change that materially changes an approved project's core implementation stack is an A3 decision.

## 2. Platform Is Chosen Before Framework
Every project must explicitly identify its intended delivery platform before implementation expands substantially.

Permitted primary platform classifications:
- Web application
- Desktop application
- Mobile application
- Embedded/IoT system
- Game/application using a game engine
- CLI/automation/service
- Hybrid/multi-platform application

A web application is not considered a lesser or incomplete form of application. A browser-delivered product may be a full-fledged production application if its requirements are satisfied through the web platform.

## 3. Default Platform Policy
For products centered on accounts, dashboards, document upload, AI interaction, forms, collaboration, administration, reporting, or access across different devices, prefer a web application unless a native capability requirement argues against it.

Reasons:
- no installation requirement for users;
- easier demonstration and deployment;
- cross-device accessibility;
- simpler update distribution;
- natural fit for client/server AI products;
- easier staged evolution from prototype to hosted application.

Choose desktop/mobile/native when the requirement depends materially on capabilities such as:
- persistent deep OS integration;
- continuous background processing not reliably available in browsers;
- system-wide screen capture or accessibility hooks;
- local hardware/peripheral control;
- offline-first workloads requiring native storage/runtime behavior;
- app-store/mobile-device capabilities;
- high-performance rendering or game-engine needs.

## 4. Default Python Web Stack
For an ordinary Python-first web product, the default candidate stack is:
- Backend/API: FastAPI
- Persistence: SQLite for local/single-user/prototype scope; PostgreSQL when concurrency, hosted multi-user use, or production scale justifies it
- Templates/UI for simple-to-medium interfaces: server-rendered HTML + CSS + lightweight JavaScript
- Testing: pytest + framework integration tests

This is a default candidate, not a universal mandate.

Flask may be preferred for very small applications where FastAPI's validation/API structure offers no meaningful advantage.
Django may be preferred when a project strongly benefits from its integrated ORM, admin, authentication, forms, and conventional full-stack structure.

## 5. React Policy
React must not be selected merely because it is popular or considered more modern.

Use React, preferably with TypeScript for substantial projects, when the interface needs one or more of the following:
- complex client-side state;
- highly interactive dashboards;
- reusable interactive component systems;
- real-time multi-panel interfaces;
- rich drag/drop or workspace behavior;
- extensive client-side navigation;
- an established frontend/backend API separation that materially improves the product.

Do not introduce React for a mostly form-driven, document-driven, administrative, or simple workflow interface if server-rendered HTML and lightweight JavaScript can deliver the required UX more clearly and with less complexity.

AJ may still use React deliberately as a learning objective, but this must be recorded separately from a technical necessity.

## 6. Progressive Frontend Rule
Prefer the smallest frontend architecture that can satisfy the verified requirements.

Typical progression:
1. semantic HTML + CSS;
2. lightweight JavaScript;
3. targeted interactive components;
4. React/TypeScript or another SPA framework when complexity justifies migration.

Do not migrate solely for aesthetics or fashion.

## 7. Database Selection
SQLite is acceptable for prototypes, local applications, single-user systems, demonstrations, and low-concurrency hosted use when its limits do not conflict with requirements.

PostgreSQL is the preferred relational upgrade path for multi-user hosted systems requiring stronger concurrency, operational tooling, or scale.

MySQL/MariaDB, SQL Server, document databases, vector databases, and other persistence technologies may be used when a requirement materially favors them.

Do not add a dedicated vector database merely because a project uses AI or embeddings. Project-sized corpora may be better served initially by relational storage plus inspectable retrieval.

## 8. AI/ML Stack
Python is the preferred AI/data language unless there is a concrete constraint requiring another runtime.

Model/provider code should be isolated behind adapters or service interfaces where practical so that the domain layer is not unnecessarily tied to one external vendor.

Local-model use must be evaluated against hardware, memory, latency, deployment, licensing, and model-quality requirements rather than assumed to be preferable.

## 9. Desktop and Mobile Guidance
Desktop applications should generally be considered when browser delivery cannot meet OS-integration or offline/runtime requirements.

Candidate approaches may include:
- Python + PySide/PyQt for Python-centric desktop applications;
- C#/.NET for Windows-heavy desktop requirements;
- Electron/Tauri or similar web-technology shells when a mature web UI must become desktop-integrated;
- native or cross-platform mobile technologies where phone/tablet capabilities are primary.

Platform/framework selection must be justified by requirements before commitment.

## 10. Embedded, Hardware, and Systems Guidance
For microcontrollers and hardware projects:
- MicroPython is preferred where hardware capability, timing, memory, and library requirements permit it and fast iteration is valuable.
- C/C++ is preferred when timing, memory, peripheral control, library support, firmware size, or hardware constraints require lower-level implementation.

Do not force Python into a hardware environment where it makes the system materially less reliable or feasible.

## 11. Game Development Guidance
A game should normally use an appropriate game engine rather than a generic web/backend stack.

Engine and language selection depends on project type, target platform, graphics requirements, team familiarity, licensing, hardware, and deployment goals. Possible ecosystems include Godot, Unity, Unreal, or browser-based engines.

This choice is project-specific and normally A3 because it determines the core application architecture.

## 12. Required Technology Decision Record for Every Project
Before substantial engineering, each project must record:
- primary platform;
- primary language(s);
- backend framework if applicable;
- frontend approach;
- database/storage approach;
- AI/ML stack if applicable;
- deployment target;
- major external services/providers;
- reason for each material choice;
- rejected alternatives where useful;
- migration path for known scale or platform limits.

## 13. Decision Criteria
Technology choices should be evaluated against:
- project requirements;
- AJ's ability to understand and defend the implementation;
- development speed;
- maintainability;
- testability;
- hardware constraints;
- deployment complexity;
- cost;
- security/privacy;
- ecosystem/library support;
- performance requirements;
- offline requirements;
- expected scale;
- learning value, when deliberately chosen as a project objective.

## 14. Anti-Patterns
Do not:
- use a framework only because it is trendy;
- convert a simple project into microservices without a requirement;
- add React solely to make a project look professional;
- treat a web application as incomplete merely because it is browser-based;
- select a native application when the browser already satisfies the requirements;
- use Python everywhere regardless of hardware/runtime constraints;
- change an approved core stack silently;
- describe planned platform migration as already implemented.

## 15. AJ Preference Profile
Current default preference order for suitable projects:
1. Python as primary application/backend language.
2. HTML/CSS/JavaScript for web presentation and interaction.
3. React may be introduced where UI complexity justifies it or where AJ deliberately chooses it as a learning objective.
4. Existing familiarity with C, C++, C#, and Java may be used when a project's domain favors those ecosystems.

This preference profile guides decisions but does not override technical feasibility or explicit project requirements.
