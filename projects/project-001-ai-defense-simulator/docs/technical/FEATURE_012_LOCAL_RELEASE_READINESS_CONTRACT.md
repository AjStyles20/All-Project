# Feature 012 Contract — Local Run & Release Readiness

## Status
APPROVED FOR BOUNDED EXECUTION

## Purpose
Make Project 001 reproducibly and conservatively runnable as a local single-user prototype on AJ's Windows machine without silently widening the network boundary, exposing credentials, or overstating deployment readiness.

## Required behavior
1. Default runtime bind address is loopback only (`127.0.0.1`).
2. The supported local launcher rejects non-loopback bind addresses rather than accepting `0.0.0.0` or LAN/public interfaces.
3. Port is explicitly bounded to 1024–65535.
4. OpenAI integration remains disabled by default (`P001_OPENAI_ENABLED=0`).
5. No API key appears in `.env.example`, source code, browser forms, logs, health output, or self-check output.
6. Local runtime data lives outside tracked source artifacts and the SQLite path can be configured.
7. `.env`, SQLite runtime files, backups, caches and virtual environments are ignored by Git.
8. A local self-check verifies Python/runtime configuration, writable data location, database initialization and provider configuration state without making an external provider request.
9. A database backup command uses SQLite's backup mechanism rather than copying a possibly-active database file blindly.
10. Local startup does not automatically enable provider/network calls or open external services.
11. Startup/configuration failures are explicit and bounded; secrets are not echoed.
12. Documentation distinguishes CI verification, local startup verification, browser/device verification and live-provider verification.

## Out of scope
- public/LAN deployment
- reverse proxy/TLS deployment
- authentication/multi-user authorization
- Windows installer/executable packaging
- cloud hosting
- automatic API-key onboarding
- automatic provider billing/usage tests

## Completion gate
Feature 012 is D4/CI verified after launcher/config/self-check/backup behavior and regression tests pass on the checked-out PR merge ref. D5 remains AJ-controlled execution on the actual Windows/browser/device environment.
