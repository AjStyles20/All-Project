# P010 (legacy folder P005) — Intelligent Online Chess Platform

Online chess for two players and spectators, with an automated arbiter that reads chat in context: the board, who is speaking, the game phase and the agreed match rules. It flags suspected outside help or abuse **for a person to review**; it never changes or ends a game.

Research framing: `research/PASS_003_CONTEXTUAL_VOICE_ARBITRATION_FINAL_GATE.md` (H5, contextual voice arbitration).

## Status (2026-11-05)
- **First version, built under DR-021.** Rules engine, two-player games with spectators and chat, arbiter methods B0–B4, labelled benchmark and evaluation.
- **Text chat, not voice.** Text stands in for speech-to-text output; the arbiter tolerates common recognition errors ("night to f six"). No audio is captured or stored.
- **No accounts:** a seat belongs to whoever holds its secret link. Games live in memory and are lost on restart.
- **Benchmark:** B4 met the predeclared rule, but it misses insults and threats phrased in ways its word lists do not cover (see `docs/EVALUATION.md`).

## Run
```bash
python -m venv venv
venv\Scripts\activate            # Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn p010.api:app --port 8012  # open http://127.0.0.1:8012, create a game, share the links
python -m p010.evaluation final
```

## Layout
| Path | Contents |
|---|---|
| `p010/chess.py` | Rules: legal moves, check, mate, stalemate, draws, SAN, FEN. Written in-house (python-chess is GPL-3.0); matches published perft counts. |
| `p010/arbiter.py` | Move-mention parsing and methods B0 keywords, B1 text classifier, B2 classifier + previous message, B3 keywords + board, B4 contextual |
| `p010/benchmark.py` | Labelled utterances for classes C0–C9 (C7 collusion not modelled) under four match contracts |
| `p010/evaluation.py` | Metrics and the predeclared rule |
| `p010/games.py`, `p010/api.py`, `p010/static/` | Games, chat with arbiter notices, web page |
| `docs/` | Technology selection, evaluation |
