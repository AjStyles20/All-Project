# P009 (legacy folder P006) — Personal Screen Memory System

A Windows program that keeps encrypted images of the window you are working in, only when something meaningful changes, so you can later find what you saw and pick up where you left off. Everything stays on the computer.

**Read first:** `docs/PRIVACY_SECURITY_MODEL.md`. It was written and committed before any capture code, as the project boundary requires.

## Status (2026-11-05)
- **First version, built under DR-021.** Capture policies B0–B4, default exclusions, DPAPI-encrypted store with retention, storage cap and deletion, recorder, local dashboard, offline policy comparison.
- **Not verified on a live desktop.** The Windows probes were run from the development session, where Windows reported the screen as locked and no foreground window, so the program correctly captured nothing. Recording must be tried at the keyboard by the user.
- **No text recognition yet:** search covers window titles and program names only.
- **No study with people.** The research question (task-resumption performance, Pass 003) needs participants and ethics approval. The offline comparison uses a *proxy* (see `docs/EVALUATION.md`).

## Run (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m pytest -q
python -m p009 record            # asks for confirmation, then opens the dashboard
python -m p009 view              # dashboard only
python -m p009 simulate final    # offline comparison of B0-B4
```
Options: `--retention-days 7`, `--max-gb 2`, `--exclude-program name.exe`, `--exclude-title word`, `--folder PATH`. Data lives in `%LOCALAPPDATA%\P009ScreenMemory`.

## Layout
| Path | Contents |
|---|---|
| `p009/policies.py` | B0 dense, B1 sparse, B2 visual change, B3 event-triggered, B4 selective |
| `p009/exclusions.py` | Programs and title words never captured |
| `p009/store.py`, `p009/protect.py` | SQLite metadata, DPAPI-encrypted images, retention, cap, deletion |
| `p009/platform_win.py`, `p009/recorder.py` | Foreground window, idle and lock detection, capture loop |
| `p009/api.py`, `p009/static/` | Local dashboard (127.0.0.1, per-run token, local Host only) |
| `p009/simulate.py` | Synthetic sessions and policy comparison |
| `results/` | Pilot and final simulation output |
