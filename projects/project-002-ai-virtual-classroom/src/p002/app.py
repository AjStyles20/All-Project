"""Single-user Personal Learning World (ADR-007): the course with its trust states, and practice
with an explicit help ladder and mastery that has to be shown without help.

Learner events are stored in SQLite and replayed into the deterministic kernels at start-up.
Local only: bound to 127.0.0.1 by `python -m p002`, every /api request needs the per-run token,
and the Host must be local.
"""
import secrets
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from p002.course import CONCEPTS, QUESTIONS, TABLES, build
from p002.domain import Assistance, IssueState, Mastery, PolicyError
from p002.mastery import MasteryKernel

STATIC = Path(__file__).parent / "static"
LEARNER = "me"
BY_ID = {q.id: q for q in QUESTIONS}


class HintInput(BaseModel):
    question_id: str = Field(max_length=40)


class AnswerInput(BaseModel):
    question_id: str = Field(max_length=40)
    choice: int = Field(ge=0, le=9)
    accommodation: str | None = Field(default=None, max_length=60)


class IssueInput(BaseModel):
    concept: str = Field(max_length=40)
    description: str = Field(min_length=1, max_length=300)


class MoveInput(BaseModel):
    to: IssueState


class Store:
    def __init__(self, path):
        self.path = str(path)
        with self._db() as db:
            db.execute("CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT, at REAL, kind TEXT, "
                       "a TEXT, b TEXT, c INTEGER, d INTEGER, e INTEGER, f TEXT)")

    def _db(self):
        db = sqlite3.connect(self.path)
        return db

    def append(self, kind, a="", b="", c=0, d=0, e=0, f=None):
        with self._db() as db:
            db.execute("INSERT INTO events (at, kind, a, b, c, d, e, f) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (time.time(), kind, a, b, c, d, e, f))

    def events(self):
        with self._db() as db:
            return db.execute("SELECT kind, a, b, c, d, e, f FROM events ORDER BY seq").fetchall()


def replay(store) -> MasteryKernel:
    k = MasteryKernel()
    issue_ids = []
    for kind, a, b, c, d, e, f in store.events():
        if kind == "attempt":
            q = BY_ID[a]
            steps = [(Assistance(level), "learner asked for more help") for level in range(1, d + 1)]
            k.record(LEARNER, q.concept, q.id, bool(c), steps, accommodation=f, verification=bool(e))
        elif kind == "issue_open":
            issue_ids.append(k.open_issue(LEARNER, a, b).id)
        elif kind == "issue_move":
            try:
                k.move_issue(a, IssueState(b))
            except PolicyError:
                pass
    return k


def create_app(db_path, token: str) -> FastAPI:
    store = Store(db_path)
    trust, ids = build()
    open_help = {}   # question_id -> current help level for the attempt in progress
    app = FastAPI(title="P006 Learning World", docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        host = (request.headers.get("host") or "").rsplit(":", 1)[0]
        if host not in ("127.0.0.1", "localhost"):
            return JSONResponse({"detail": "Local access only."}, status_code=403)
        if request.url.path.startswith("/api/") and not secrets.compare_digest(
                request.headers.get("x-token", "").encode(), token.encode()):
            return JSONResponse({"detail": "Missing or wrong token."}, status_code=401)
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; frame-ancestors 'none'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/course")
    def course():
        claims = []
        for cid, c in trust.claims.items():
            e = trust.explain(cid)
            claims.append({"id": cid, "text": c.text, "authority": e.authority.name, "status": e.status.value,
                           "reasons": list(e.reasons), "path": list(e.path), "created_by": c.created_by,
                           "evidence": [[s, r.value] for s, r in c.evidence],
                           "parents": [[p, edge.value, actor] for p, edge, actor in c.parents]})
        sources = [{"id": s.id, "title": s.title, "version": s.version, "authority": s.authority.name,
                    "superseded_by": s.superseded_by, "sha256": s.sha256[:12], "text": s.text} for s in trust.sources.values()]
        artifacts = []
        for aid, a in trust.artifacts.items():
            status, reasons = trust.artifact_status(aid)
            artifacts.append({"id": aid, "kind": a.kind, "content": a.content, "status": status.value,
                              "reasons": reasons, "depends_on": a.depends_on})
        return {"sources": sources, "claims": claims, "artifacts": artifacts, "audit": trust.audit}

    def next_question(k):
        for concept in CONCEPTS:
            if k.needs_verification(LEARNER, concept):
                return next(q for q in QUESTIONS if q.concept == concept and q.check)
        for concept in CONCEPTS:
            if k.state(LEARNER, concept).mastery is not Mastery.INDEPENDENT:
                return next(q for q in QUESTIONS if q.concept == concept and not q.check)
        return None

    def public(q, level=0):
        return {"id": q.id, "concept": CONCEPTS[q.concept], "prompt": q.prompt, "options": list(q.options),
                "check": q.check, "tables": "" if q.check else TABLES, "help_level": level,
                "hints": list(q.hints[:level]), "max_help": len(q.hints)}

    @app.get("/api/practice")
    def practice():
        q = next_question(replay(store))
        return {"question": public(q, open_help.get(q.id, 0)) if q else None}

    @app.post("/api/hint")
    def hint(payload: HintInput):
        q = BY_ID.get(payload.question_id)
        if q is None:
            raise HTTPException(404, "No such question.")
        if q.check:
            raise HTTPException(409, "This is a check without help: no hints.")
        level = open_help.get(q.id, 0) + 1
        if level > len(q.hints):
            raise HTTPException(409, "No more help for this question.")
        open_help[q.id] = level
        return {"question": public(q, level)}

    @app.post("/api/answer")
    def answer(payload: AnswerInput):
        q = BY_ID.get(payload.question_id)
        if q is None or payload.choice >= len(q.options):
            raise HTTPException(404, "No such question or option.")
        level = open_help.pop(q.id, 0)
        correct = payload.choice == q.answer
        store.append("attempt", q.id, "", int(correct), level, int(q.check), payload.accommodation)
        k = replay(store)
        s = k.state(LEARNER, q.concept)
        return {"correct": correct, "answer": q.options[q.answer], "help_level": level,
                "mastery": s.mastery.value, "reasons": s.reasons}

    @app.get("/api/mastery")
    def mastery():
        k = replay(store)
        out = []
        for concept, label in CONCEPTS.items():
            s = k.state(LEARNER, concept)
            trail = [{"id": a.id, "task": a.task, "correct": a.correct, "help": f"L{int(a.assistance)}",
                      "check": a.verification, "accommodation": a.accommodation}
                     for a in (k.attempts[i] for i in s.evidence)]
            out.append({"concept": concept, "label": label, "mastery": s.mastery.value, "reasons": s.reasons, "trail": trail})
        issues = [{**asdict(i), "state": i.state.value} for i in k.issues.values()]
        return {"concepts": out, "issues": issues}

    @app.post("/api/issues", status_code=201)
    def open_issue(payload: IssueInput):
        if payload.concept not in CONCEPTS:
            raise HTTPException(404, "No such concept.")
        store.append("issue_open", payload.concept, payload.description)
        return {"ok": True}

    @app.post("/api/issues/{issue_id}/move")
    def move_issue(issue_id: str, payload: MoveInput):
        k = replay(store)
        if issue_id not in k.issues:
            raise HTTPException(404, "No such issue.")
        try:
            k.move_issue(issue_id, payload.to)
        except PolicyError as exc:
            raise HTTPException(409, str(exc)) from exc
        store.append("issue_move", issue_id, payload.to.value)
        return {"state": payload.to.value}

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
