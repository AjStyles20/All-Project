# P007 technology selection (PROJECT_RULES §21)

| Item | Choice | Why |
|---|---|---|
| Platform | Web application | Dashboards and reporting for staff; nothing needs native OS access. |
| Language | Python 3.11+ | Project OS default. Pass 004 §19 suggests it for generation, audit and evaluation. |
| Backend | FastAPI | Same as P001, so the patterns and tests carry over. |
| Frontend | Plain HTML, CSS and JavaScript modules | One dashboard screen; no framework needed. Strict CSP, `textContent` only. |
| Storage | SQLite | Single-file ledger, no server to run. Writes use `BEGIN IMMEDIATE`, so a balance check and the spend that depends on it cannot interleave. Move to PostgreSQL or MySQL before multi-user deployment. |
| Statistics | Python standard library (`statistics`, `math`) | The tests needed (means, Welch t, two-proportion z, median/MAD) are small. pandas and scikit-learn are not needed yet. |
| Deployment | Local only | Synthetic-data demonstration build. No hosting chosen. |
| AI / external services | None | Nothing leaves the machine; no costs. |

A move to a different core language or to real student data is an A3 decision for AJ.
