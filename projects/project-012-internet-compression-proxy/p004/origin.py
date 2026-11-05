"""Controlled test origin: serves the generated corpus plus fixtures for the security tests.

Used in-process by the tests (as an httpx transport) and as a small server in the lab:
uvicorn p004.origin:app --port 8014
"""
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

from p004.corpus import build

OBJECTS = {o.name: o for o in build(1)}


def respond(path: str, headers: dict) -> tuple[int, dict, bytes]:
    if path.startswith("/c/") and path[3:] in OBJECTS:
        o = OBJECTS[path[3:]]
        return 200, {"content-type": o.content_type, **o.headers}, o.body
    if path == "/redirect":
        return 302, {"location": "http://169.254.169.254/latest/meta-data/"}, b""
    if path == "/big":
        return 200, {"content-type": "application/octet-stream"}, b"\0" * (21 * 1024 * 1024)
    if path == "/account":
        if not headers.get("authorization"):
            return 401, {"content-type": "text/plain"}, b"sign in"
        return 200, {"content-type": "application/json", "cache-control": "private"}, b'{"balance": 12, "pad": "' + b"x" * 5000 + b'"}'
    if path == "/echo-headers":
        return 200, {"content-type": "text/plain"}, "\n".join(f"{k}: {v}" for k, v in sorted(headers.items())).encode()
    return 404, {"content-type": "text/plain"}, b"not found"


def transport() -> httpx.MockTransport:
    def handler(request: httpx.Request):
        status, headers, body = respond(request.url.path, {k.lower(): v for k, v in request.headers.items()})
        return httpx.Response(status, headers=headers, content=body)
    return httpx.MockTransport(handler)


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/{path:path}")
def serve(path: str, request: Request):
    status, headers, body = respond("/" + path, {k.lower(): v for k, v in request.headers.items()})
    return Response(body, status_code=status, headers=headers)
