# P003 M6/M7 — Reproducibility and Baseline-Runner Checkpoint

## M6 verification

GitHub Actions P003 ETEC Tests run #36 verified deterministic replay persistence and integrity checks: **26 passed, 0 failed in 0.08s**.

M6 is closed for the transparent JSON replay slice.

## M7 first bounded slice

The first M7 implementation creates explicit B0-B3 baseline adapters and a neutral comparison record:

- **B0 — News/GPR signal:** event/news-intensity signal only.
- **B1 — Event + Exposure:** verified event and direct Nigeria exposure, no downstream transmission contract.
- **B2 — Narrative placeholder:** records an ungated downstream narrative claim. It is not yet a real LLM/RAG invocation.
- **B3 — ETEC:** deterministic typed-edge progression with weakest-link stopping.

The comparison runner records output class, ordinal claim strength, and whether structural gating was applied. It does **not** calculate a winner or claim empirical superiority.

## Critical experiment boundary

Constructed fixtures cannot establish the frozen M7 research criterion that B3 reduces unsupported downstream claims relative to B2. That requires:
1. equivalent frozen information for each baseline;
2. a real, frozen B2 LLM/RAG procedure or another defensible implementation of that baseline;
3. reference judgments/outcomes independent of B3;
4. historical/negative-control cases selected without outcome cherry-picking;
5. predeclared scoring rules.

Until then, M7 results are infrastructure checks only.
