from __future__ import annotations

from pathlib import Path
import os
from urllib.parse import urlencode, urlparse

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .db import Database
from .embeddings import EmbeddingProvider, provider_identity
from .evaluation import AnswerEvaluator, evaluate_and_store_answer
from .ingestion import (
    DocumentExtractionError,
    SUPPORTED_EXTENSIONS,
    extract_document_chunks,
    sha256_bytes,
)
from .questioning import QuestionGenerator, generate_and_store_question
from .retrieval import hybrid_search
from .ui_data import get_question, get_workspace, list_documents, list_evaluations, list_questions, list_workspaces

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = Path(os.getenv("P001_DATABASE_PATH", DATA_DIR / "project001.db"))
MAX_UPLOAD_BYTES = int(os.getenv("P001_MAX_UPLOAD_BYTES", str(2 * 1024 * 1024)))
ENABLE_API_DOCS = os.getenv("P001_ENABLE_API_DOCS", "0") == "1"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("P001_ALLOWED_HOSTS", "127.0.0.1,localhost,testserver").split(",")
    if host.strip()
]

db = Database(DATABASE_PATH)
db.initialize()

embedding_provider: EmbeddingProvider | None = None
question_generator: QuestionGenerator | None = None
answer_evaluator: AnswerEvaluator | None = None

templates = Jinja2Templates(directory=str(APP_DIR / "templates"))

app = FastAPI(
    title="Project 001 — Source-Grounded Review Simulator",
    version="0.6.0",
    docs_url="/docs" if ENABLE_API_DOCS else None,
    redoc_url="/redoc" if ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if ENABLE_API_DOCS else None,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")


@app.middleware("http")
async def security_headers_and_origin_guard(request: Request, call_next):
    if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
        fetch_site = request.headers.get("sec-fetch-site", "").lower()
        if fetch_site == "cross-site":
            return PlainTextResponse("Cross-origin request rejected", status_code=403)

        origin = request.headers.get("origin")
        if origin:
            parsed = urlparse(origin)
            request_host = request.headers.get("host", "")
            if parsed.scheme not in {"http", "https"} or parsed.netloc != request_host:
                return PlainTextResponse("Cross-origin request rejected", status_code=403)

    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; base-uri 'none'; frame-ancestors 'none'; "
        "form-action 'self'; object-src 'none'; img-src 'self' data:; "
        "style-src 'self'; script-src 'self'; connect-src 'self'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    return response


def _semantic_status() -> dict:
    status = {"status": "not configured", "provider": None, "model": None}
    if embedding_provider is not None:
        identity = provider_identity(embedding_provider)
        status = {"status": "configured", "provider": identity.provider, "model": identity.model}
    return status


def _question_status() -> dict:
    status = {"status": "not configured", "provider": None, "model": None}
    if question_generator is not None:
        status = {
            "status": "configured",
            "provider": str(question_generator.provider_name),
            "model": str(question_generator.model_name),
        }
    return status


def _evaluation_status() -> dict:
    status = {"status": "not configured", "provider": None, "model": None}
    if answer_evaluator is not None:
        status = {
            "status": "configured",
            "provider": str(answer_evaluator.provider_name),
            "model": str(answer_evaluator.model_name),
        }
    return status


def _redirect(path: str, *, message: str | None = None, error: str | None = None) -> RedirectResponse:
    params: dict[str, str] = {}
    if message:
        params["message"] = message
    if error:
        params["error"] = error
    target = f"{path}?{urlencode(params)}" if params else path
    return RedirectResponse(target, status_code=303)


def _render_error(request: Request, detail: str, *, status_code: int, return_path: str = "/"):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"detail": detail, "return_path": return_path, "message": None, "error": None},
        status_code=status_code,
    )


@app.get("/health")
def health() -> dict:
    try:
        db.initialize()
        database_status = "available"
    except Exception:
        database_status = "unavailable"
    return {
        "application": "available",
        "database": database_status,
        "ai_provider": _question_status(),
        "semantic_retrieval": _semantic_status(),
        "answer_evaluation": _evaluation_status(),
    }


@app.post("/api/workspaces")
def create_workspace(name: str = Form(...)) -> dict:
    cleaned = name.strip()
    if not cleaned:
        raise HTTPException(status_code=422, detail="Workspace name is required")
    if len(cleaned) > 120:
        raise HTTPException(status_code=422, detail="Workspace name is too long")
    return db.create_workspace(cleaned)


@app.post("/api/workspaces/{workspace_id}/documents")
async def upload_document(workspace_id: str, file: UploadFile = File(...)) -> dict:
    if not db.workspace_exists(workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found")

    filename = (file.filename or "").strip()
    if not filename:
        raise HTTPException(status_code=422, detail="Filename is required")
    if len(filename) > 255:
        raise HTTPException(status_code=422, detail="Filename is too long")

    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}",
        )

    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds configured upload limit")
    if not data:
        raise HTTPException(status_code=422, detail="File is empty")

    try:
        chunks = extract_document_chunks(filename, data)
    except DocumentExtractionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if not chunks:
        raise HTTPException(status_code=422, detail="File contains no extractable text")

    document = db.store_document(
        workspace_id=workspace_id,
        original_filename=filename,
        extension=extension,
        content_hash=sha256_bytes(data),
        chunks=chunks,
    )
    document["warnings"] = []
    return document


@app.get("/api/workspaces/{workspace_id}/search")
def search_workspace(
    workspace_id: str,
    q: str = Query(..., min_length=1, max_length=500),
    limit: int = Query(10, ge=1, le=50),
    mode: str = Query("lexical", pattern="^(lexical|hybrid)$"),
) -> dict:
    if not db.workspace_exists(workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found")

    try:
        if mode == "lexical":
            results = db.search(workspace_id=workspace_id, query=q, limit=limit)
            retrieval = {
                "requested_mode": "lexical",
                "effective_mode": "lexical",
                "semantic_status": "not requested",
                "provider": None,
                "model": None,
            }
        else:
            results, status = hybrid_search(
                db,
                workspace_id=workspace_id,
                query=q,
                provider=embedding_provider,
                limit=limit,
            )
            retrieval = {
                "requested_mode": status.requested_mode,
                "effective_mode": status.effective_mode,
                "semantic_status": status.semantic_status,
                "provider": status.provider,
                "model": status.model,
            }
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Retrieval data could not be processed safely") from exc
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Search query could not be processed") from exc

    return {"workspace_id": workspace_id, "query": q, "retrieval": retrieval, "results": results}


@app.post("/api/workspaces/{workspace_id}/questions")
def create_grounded_question(
    workspace_id: str,
    topic: str = Form(...),
    reviewer_role: str = Form(...),
    retrieval_mode: str = Form("hybrid"),
) -> dict:
    if not db.workspace_exists(workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found")
    if question_generator is None:
        raise HTTPException(status_code=503, detail="Question generation is not configured")
    if retrieval_mode not in {"lexical", "hybrid"}:
        raise HTTPException(status_code=422, detail="Unsupported retrieval mode")

    try:
        if retrieval_mode == "lexical":
            evidence = db.search(workspace_id=workspace_id, query=topic, limit=8)
            effective_mode = "lexical"
            semantic_status = "not requested"
        else:
            evidence, status = hybrid_search(
                db,
                workspace_id=workspace_id,
                query=topic,
                provider=embedding_provider,
                limit=8,
            )
            effective_mode = status.effective_mode
            semantic_status = status.semantic_status

        return generate_and_store_question(
            db,
            workspace_id=workspace_id,
            reviewer_role=reviewer_role,
            topic=topic,
            evidence_rows=evidence,
            retrieval_mode=effective_mode,
            semantic_status=semantic_status,
            provider=question_generator,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Question could not be generated safely") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Question provider failed") from exc


@app.post("/api/workspaces/{workspace_id}/questions/{question_id}/answers")
def evaluate_answer(
    workspace_id: str,
    question_id: str,
    answer: str = Form(...),
) -> dict:
    if not db.workspace_exists(workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found")
    if answer_evaluator is None:
        raise HTTPException(status_code=503, detail="Answer evaluation is not configured")

    try:
        return evaluate_and_store_answer(
            db,
            workspace_id=workspace_id,
            question_id=question_id,
            answer=answer,
            provider=answer_evaluator,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="Answer could not be evaluated safely") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Answer evaluator failed") from exc


@app.get("/")
def web_home(
    request: Request,
    message: str | None = Query(None, max_length=300),
    error: str | None = Query(None, max_length=300),
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "workspaces": list_workspaces(db),
            "semantic_status": _semantic_status(),
            "question_status": _question_status(),
            "evaluation_status": _evaluation_status(),
            "message": message,
            "error": error,
        },
    )


@app.post("/ui/workspaces")
def web_create_workspace(name: str = Form(...)):
    try:
        workspace = create_workspace(name)
    except HTTPException as exc:
        return _redirect("/", error=str(exc.detail))
    return _redirect(f"/workspaces/{workspace['id']}", message="Workspace created.")


@app.get("/workspaces/{workspace_id}")
def web_workspace(
    request: Request,
    workspace_id: str,
    q: str | None = Query(None, max_length=500),
    mode: str = Query("lexical", pattern="^(lexical|hybrid)$"),
    message: str | None = Query(None, max_length=300),
    error: str | None = Query(None, max_length=300),
):
    workspace = get_workspace(db, workspace_id)
    if workspace is None:
        return _render_error(request, "Workspace not found.", status_code=404)

    search_results = None
    retrieval_status = None
    local_error = error
    if q is not None and q.strip():
        try:
            result = search_workspace(workspace_id, q=q, limit=20, mode=mode)
            search_results = result["results"]
            retrieval_status = result["retrieval"]
        except HTTPException as exc:
            local_error = str(exc.detail)
            search_results = []

    return templates.TemplateResponse(
        request=request,
        name="workspace.html",
        context={
            "workspace": workspace,
            "documents": list_documents(db, workspace_id=workspace_id),
            "questions": list_questions(db, workspace_id=workspace_id),
            "query": q,
            "mode": mode,
            "search_results": search_results,
            "retrieval_status": retrieval_status,
            "question_configured": question_generator is not None,
            "message": message,
            "error": local_error,
        },
    )


@app.post("/ui/workspaces/{workspace_id}/documents")
async def web_upload_document(workspace_id: str, file: UploadFile = File(...)):
    try:
        document = await upload_document(workspace_id, file)
    except HTTPException as exc:
        return _redirect(f"/workspaces/{workspace_id}", error=str(exc.detail))
    return _redirect(
        f"/workspaces/{workspace_id}",
        message=f"Uploaded {document['original_filename']} with {document['chunk_count']} extracted chunk(s).",
    )


@app.post("/ui/workspaces/{workspace_id}/questions")
def web_create_question(
    workspace_id: str,
    topic: str = Form(...),
    reviewer_role: str = Form(...),
    retrieval_mode: str = Form("hybrid"),
):
    try:
        question = create_grounded_question(workspace_id, topic, reviewer_role, retrieval_mode)
    except HTTPException as exc:
        return _redirect(f"/workspaces/{workspace_id}", error=str(exc.detail))
    return _redirect(
        f"/workspaces/{workspace_id}/questions/{question['id']}",
        message="Grounded reviewer question generated.",
    )


@app.get("/workspaces/{workspace_id}/questions/{question_id}")
def web_question(
    request: Request,
    workspace_id: str,
    question_id: str,
    message: str | None = Query(None, max_length=300),
    error: str | None = Query(None, max_length=300),
):
    workspace = get_workspace(db, workspace_id)
    if workspace is None:
        return _render_error(request, "Workspace not found.", status_code=404)
    try:
        question = get_question(db, workspace_id=workspace_id, question_id=question_id)
        if question is None:
            return _render_error(
                request,
                "Question not found in this workspace.",
                status_code=404,
                return_path=f"/workspaces/{workspace_id}",
            )
        evaluations = list_evaluations(db, workspace_id=workspace_id, question_id=question_id)
    except ValueError:
        return _render_error(
            request,
            "Stored question or evaluation provenance could not be verified safely.",
            status_code=422,
            return_path=f"/workspaces/{workspace_id}",
        )

    return templates.TemplateResponse(
        request=request,
        name="question.html",
        context={
            "workspace": workspace,
            "question": question,
            "evaluations": evaluations,
            "evaluation_configured": answer_evaluator is not None,
            "message": message,
            "error": error,
        },
    )


@app.post("/ui/workspaces/{workspace_id}/questions/{question_id}/answers")
def web_evaluate_answer(
    workspace_id: str,
    question_id: str,
    answer: str = Form(...),
):
    try:
        evaluate_answer(workspace_id, question_id, answer)
    except HTTPException as exc:
        return _redirect(
            f"/workspaces/{workspace_id}/questions/{question_id}",
            error=str(exc.detail),
        )
    return _redirect(
        f"/workspaces/{workspace_id}/questions/{question_id}",
        message="Answer evaluated and feedback recorded.",
    )
