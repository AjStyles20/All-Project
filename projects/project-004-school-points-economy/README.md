# P007 (legacy folder P004) — School Point & Digital Economy System

A school points ledger with a governance audit. The audit reports on how reward policies are playing out, in one of three states: **no material signal**, **governance signal** (a person should look) or **insufficient context**. It never gives a fair/unfair verdict.

Research framing, frozen in `research/PASS_004_FORMAL_RESEARCH_AND_EXPERIMENT_SPECIFICATION.md` (hypothesis H5): a contextual audit (B4) against four simpler baselines (B0–B3) on synthetic scenarios S0–S8.

## Status (2026-11-05)
- **First working version, built under DR-021.** Ledger, scenario generator, audit engines B0–B4, evaluation harness, web API and dashboard.
- **Synthetic data only.** There is no sign-in, and the issuer is whoever the caller says it is. Not for real student data.
- **Benchmark result:** B4 met the predeclared rule on the final seeds and at three class sizes. Because the same agent wrote both the scenarios and B4, this is **not evidence that the audit works on real schools** (see `docs/RESULTS.md`).

## Run
```bash
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn p007.api:default_app --factory --port 8011   # dashboard at http://127.0.0.1:8011
python -m p007.evaluation pilot   # harness check, seeds 0-4
python -m p007.evaluation final   # final seeds 1000-1019 and three class sizes
```
`P007_DB_PATH` sets the SQLite file (default `./p007.sqlite3`). On the dashboard, load a synthetic scenario into the empty ledger, then run any audit method.

## Layout
| Path | Contents |
|---|---|
| `p007/domain.py` | Data model (Pass 004 §10) |
| `p007/store.py` | SQLite ledger: awards, redemptions, reversals; balances derived from the log |
| `p007/benchmark.py` | Scenario generator S0–S8. Ground truth is returned separately from the data the audits see. |
| `p007/audit.py` | B0 totals, B1 static thresholds, B2 anomaly detection, B3 disparity only, B4 contextual audit; frozen thresholds |
| `p007/evaluation.py` | Metrics M1–M5 and M8, the composite success rule, pilot and final runs |
| `p007/api.py`, `p007/static/` | Web API and dashboard |
| `results/` | Raw pilot and final results (JSON) |
| `docs/` | Technology selection, evaluation protocol, results |
