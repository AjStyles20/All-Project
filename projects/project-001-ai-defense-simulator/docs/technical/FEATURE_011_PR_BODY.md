## Purpose
Integrate the existing Project 001 capabilities into one coherent bounded defense/viva rehearsal flow.

## Included
- session start lands directly on the first authoritative turn
- session-specific question route with server-side workspace/session/question verification
- visible turn/max-turn progress and current action
- answer/evaluation flow stays inside the owning rehearsal
- direct follow-up-to-next-turn navigation
- session summary with generated/answered/current-turn state
- automatic server-authoritative completion when the final configured turn is answered
- completed sessions reject further follow-up generation
- cross-workspace/session-question tampering tests
- completion idempotence tests

## Security boundaries
No authentication/public-deployment claim is added. Existing provenance, provider, CSP, same-origin, upload, speech, and workspace-isolation controls remain in force. Client-supplied session IDs do not authorize question access.

## Verification
Full GitHub Actions merge-ref compile/test/dependency-audit gate pending.

## Live boundary
AJ-controlled browser/device rehearsal and live provider verification remain separate D5 gates.
