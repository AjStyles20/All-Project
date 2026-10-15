from __future__ import annotations

from pathlib import Path
import os

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile

from .db import Database
from .ingestion import (
    DocumentExtractionError,
    SUPPORTED_EXTENSIONS,
    extract_document_chunks,
    sha256_bytes,
)

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = Path(os.getenv("P001_DATABASE_PATH", DATA_DIR / "project001.db"))
MAX_UPLOAD_BYTES = int(os.getenv("P001_MAX_UPLOAD_BYTES", str(2 * 1024 * 1024)))

db = Database(DATABASE_PATH)
db.initialize()

app = FastAPI(
    title="Project 001 — Source-Grounded Review Simulator",
    version="0.2.0",
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
        "ai_provider": "not configured",
    }


@app.post("/api/workspaces")
def create_workspace(name: str = Form(...)) -> dict:
    cleaned = name.strip()
    if not cleaned:
        raise HTTPException(status_code=422, detail="Workspace name is required")
    return db.create_workspace(cleaned)


@app.post("/api/workspaces/{workspace_id}/documents")
async def upload_document(workspace_id: str, file: UploadFile = File(...)) -> dict:
    if not db.workspace_exists(workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found")

    filename = (file.filename or "").strip()
    if not filename:
        raise HTTPException(status_code=422, detail="Filename is required")

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
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
) -> dict:
    if not db.workspace_exists(workspace_id):
        raise HTTPException(status_code=404, detail="Workspace not found")

    try:
        results = db.search(workspace_id=workspace_id, query=q, limit=limit)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Search query could not be processed") from exc

    return {
        "workspace_id": workspace_id,
        "query": q,
        "results": results,
    }
