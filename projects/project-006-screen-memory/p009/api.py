"""Local dashboard: browse, search, pause and delete (privacy model §1 and §3).

Bound to 127.0.0.1 by the launcher. Every /api request needs the per-run token, and the Host
header must name this machine, so web pages and DNS-rebinding tricks cannot reach the data.
The token travels in the URL fragment (never sent to a server) and then in a request header.
"""
import secrets
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

STATIC = Path(__file__).parent / "static"
LOCAL_HOSTS = {"127.0.0.1", "localhost"}


class RecentInput(BaseModel):
    minutes: int = Field(ge=1, le=24 * 60)


class DeleteAllInput(BaseModel):
    confirm: str


def create_app(store, token: str, recorder=None) -> FastAPI:
    app = FastAPI(title="P009 Screen Memory", docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        host = (request.headers.get("host") or "").rsplit(":", 1)[0].strip("[]")
        if host not in LOCAL_HOSTS:
            return JSONResponse({"detail": "Local access only."}, status_code=403)
        if request.url.path.startswith("/api/"):
            supplied = request.headers.get("x-token", "")
            if not secrets.compare_digest(supplied.encode(), token.encode()):
                return JSONResponse({"detail": "Missing or wrong token."}, status_code=401)
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' blob:; object-src 'none'; frame-ancestors 'none'")
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/status")
    def status():
        return {**store.stats(), "recorder": recorder.status if recorder else "not recording"}

    @app.post("/api/pause")
    def pause():
        if recorder is None:
            raise HTTPException(409, "This dashboard is not recording.")
        recorder.pause()
        return {"recorder": recorder.status}

    @app.post("/api/resume")
    def resume():
        if recorder is None:
            raise HTTPException(409, "This dashboard is not recording.")
        recorder.resume()
        return {"recorder": recorder.status}

    @app.get("/api/frames")
    def frames(q: str = Query(default="", max_length=200)):
        return store.search(q)

    @app.get("/api/frames/{frame_id}/image")
    def image(frame_id: str):
        data = store.image(frame_id)
        if data is None:
            raise HTTPException(404, "Not found.")
        return Response(data, media_type="image/webp")

    @app.delete("/api/frames/{frame_id}")
    def delete(frame_id: str):
        return {"deleted": store.delete(frame_id)}

    @app.post("/api/delete-recent")
    def delete_recent(payload: RecentInput):
        return {"deleted": store.delete_since(payload.minutes * 60)}

    @app.post("/api/delete-all")
    def delete_all(payload: DeleteAllInput):
        if payload.confirm != "DELETE":
            raise HTTPException(400, 'Type DELETE to confirm.')
        return {"deleted": store.delete_all()}

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
