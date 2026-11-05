"""Local web app: upload your project documents, see what a reviewer would challenge, practise
answering role-based questions, and get criterion-by-criterion feedback with the evidence shown.

Local only: `python -m p011` binds 127.0.0.1, every /api request needs the per-run token,
and the Host must be local. Nothing is sent to any external service.
"""
import secrets
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from p011.analysis import analyse
from p011.feedback import evaluate
from p011.ingest import MAX_UPLOAD, IngestError, extract
from p011.reviewers import ROLES, Question, plan
from p011.store import Store

STATIC = Path(__file__).parent / "static"


class SessionInput(BaseModel):
    roles: list[str] = Field(min_length=1, max_length=4)
    per_role: int = Field(default=3, ge=1, le=6)


class AnswerInput(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


def create_app(db_path, token: str) -> FastAPI:
    store = Store(db_path)
    app = FastAPI(title="P011 Defence Practice", docs_url=None, redoc_url=None, openapi_url=None)

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

    @app.get("/api/roles")
    def roles():
        return [{"key": r.key, "name": r.name, "purpose": r.purpose} for r in ROLES.values()]

    @app.post("/api/documents", status_code=201)
    async def upload(request: Request, name: str = Query(min_length=1, max_length=200)):
        if int(request.headers.get("content-length") or 0) > MAX_UPLOAD:
            raise HTTPException(413, "File is larger than 10 MB.")
        data = b""
        async for chunk in request.stream():
            data += chunk
            if len(data) > MAX_UPLOAD:
                raise HTTPException(413, "File is larger than 10 MB.")
        try:
            pieces = extract(name, data)
        except IngestError as exc:
            raise HTTPException(400, str(exc)) from exc
        if not pieces:
            raise HTTPException(400, "No readable text was found in this file.")
        return {"id": store.add_document(name, data, pieces), "chunks": len(pieces)}

    @app.get("/api/documents")
    def documents():
        return store.documents()

    @app.delete("/api/documents/{doc_id}")
    def delete_document(doc_id: str):
        if not store.delete_document(doc_id):
            raise HTTPException(404, "No such document.")
        return {"deleted": doc_id}

    @app.get("/api/findings")
    def findings():
        chunks = store.chunks()
        located = {c["id"]: c for c in chunks}
        return [asdict(f) | {"where": f"{located[f.chunk_id]['document']}, {located[f.chunk_id]['locator']}"}
                for f in analyse([(c["id"], c["text"]) for c in chunks])]

    @app.get("/api/search")
    def search(q: str = Query(min_length=1, max_length=200)):
        return store.search(q)

    @app.get("/api/chunks/{chunk_id}")
    def chunk(chunk_id: str):
        c = store.chunk(chunk_id)
        if c is None:
            raise HTTPException(404, "No such passage.")
        return c

    @app.post("/api/sessions", status_code=201)
    def new_session(payload: SessionInput):
        unknown = [r for r in payload.roles if r not in ROLES]
        if unknown:
            raise HTTPException(400, f"Unknown role: {unknown[0]}")
        chunks = store.chunks()
        questions = plan(payload.roles, analyse([(c["id"], c["text"]) for c in chunks]), payload.per_role)
        return {"id": store.create_session(payload.roles, questions)}

    @app.get("/api/sessions")
    def sessions():
        return store.sessions()

    @app.get("/api/sessions/{sid}")
    def session(sid: str):
        s = store.session(sid)
        if s is None:
            raise HTTPException(404, "No such session.")
        for q in s["questions"]:
            q["evidence"] = [c for c in (store.chunk(cid) for cid in q["chunk_ids"]) if c]
        return s

    @app.post("/api/questions/{qid}/answer")
    def answer(qid: str, payload: AnswerInput):
        q = store.question(qid)
        if q is None:
            raise HTTPException(404, "No such question.")
        question = Question(q["role"], q["category"], q["text"], tuple(q["chunk_ids"]), q["quote"], bool(q["grounded"]))
        sources = [c["text"] for c in (store.chunk(cid) for cid in q["chunk_ids"]) if c]
        items = [asdict(i) for i in evaluate(payload.text, question, sources)]
        store.answer(qid, payload.text, items)
        return {"feedback": items}

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
