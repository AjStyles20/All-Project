# P003 — B2 External Execution Boundary and Handoff

## Status
The first-wave B2 readiness gate is CI-verified. The repository is now ready to prepare the six predeclared prompts, but the currently connected execution tools do not expose a general-purpose text-generation endpoint with the metadata guarantees required by the frozen B2 protocol.

## Do not substitute
Do not use:
- manually invented assistant responses;
- the placeholder B2 adapter;
- a model response whose provider/model identity cannot be preserved;
- live-web browsing during a frozen-packet run;
- a different packet version without a new manifest.

## Required external execution capability
For each of the six predeclared run IDs, the execution environment must permit preservation of:
- provider;
- model;
- model/version/build when exposed;
- execution timestamp;
- exact system and user prompts;
- generation parameters exposed by provider;
- complete raw response.

The output must then be entered into `B2RunRecord` unchanged.

## Authorized run IDs
- B2-A-001
- B2-A-002
- B2-A-003
- B2-NC01-001
- B2-NC01-002
- B2-NC01-003

## Handoff sequence
1. use `prepare_run(...)` to verify manifest/packet hash and obtain exact prompts;
2. execute one predeclared run using the chosen fixed model/provider;
3. preserve metadata and raw response immediately;
4. create/hash immutable `B2RunRecord`;
5. repeat until all six predeclared runs are retained;
6. extract atomic claims without support labels;
7. prepare blinded reviewer materials.

## Scientific boundary
P003 is **externally execution-blocked for real B2 evidence**, not engineering-blocked. Deterministic implementation can continue only where it does not alter the frozen first-wave protocol.

No B2-vs-B3 empirical superiority claim is permitted while this boundary remains unresolved.
