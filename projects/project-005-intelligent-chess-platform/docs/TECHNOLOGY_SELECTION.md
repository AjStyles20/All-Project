# P010 technology selection (PROJECT_RULES §21)

| Item | Choice | Why |
|---|---|---|
| Platform | Web application | Two players and spectators on any device; no install. |
| Language | Python 3.11+ | Project OS default. |
| Rules engine | Written in-house (`p010/chess.py`) | python-chess is GPL-3.0, which would bind the repository; the in-house engine matches published perft counts. |
| Backend | FastAPI, games in memory | Same stack as other projects. Persistence (SQLite or MySQL) is the next step. |
| Updates | Polling every 1.5 s | Simple and reliable for a first version; WebSockets later if needed. |
| Frontend | Plain HTML/CSS/JS, Unicode pieces | No framework or image assets needed. Strict CSP; seat tokens stay in the URL fragment. |
| Arbiter | Rules and context in Python; baseline text classifiers in plain Python | No model downloads or paid APIs. |
| Voice | Not in this version | Text stands in for speech-to-text. Adding voice needs consent, retention and safeguarding rules first (Pass 003). |
