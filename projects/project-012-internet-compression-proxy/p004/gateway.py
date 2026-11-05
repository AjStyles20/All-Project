"""Origin-controlled optimising gateway (specification §1–§3).

One fixed upstream origin. Only GET and HEAD of plain origin paths. No cache. Every policy
runs behind the same safety rules S1–S10; B4 also verifies its output before serving it.

Run (laboratory): uvicorn p004.gateway:lab_app --factory --port 8013
"""
import asyncio
import logging
import os
from urllib.parse import urlsplit

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response

from p004.policies import VOC, CostModel, Hints, facts_for, make
from p004.transforms import NotTransformable, fidelity, to_gzip, to_webp

MAX_BODY = 20 * 1024 * 1024
TRANSFORM_TIMEOUT = 5.0
HOP_BY_HOP = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "proxy-connection", "te",
              "trailer", "transfer-encoding", "upgrade", "host", "content-length"}
log = logging.getLogger("p004.gateway")


def _hints(request: Request) -> Hints:
    def number(name, default):
        try:
            return max(0.01, float(request.headers.get(name, default)))
        except ValueError:
            return default
    return Hints(accept_webp="image/webp" in request.headers.get("accept", ""),
                 accept_gzip="gzip" in request.headers.get("accept-encoding", ""),
                 downlink_mbps=number("downlink", 10.0), rtt_ms=number("rtt", 50.0),
                 save_data=request.headers.get("save-data", "").lower() == "on")


def create_app(origin: str, policy: str = "B4", model: CostModel | None = None,
               transport: httpx.BaseTransport | None = None) -> FastAPI:
    parts = urlsplit(origin)
    if parts.scheme not in ("http", "https") or not parts.netloc or parts.path not in ("", "/"):
        raise ValueError("origin must be a bare http(s)://host[:port]")
    base = f"{parts.scheme}://{parts.netloc}"
    decide = make(policy, model)
    limiter = asyncio.Semaphore(4)
    client = httpx.Client(transport=transport, follow_redirects=False, timeout=10.0)
    app = FastAPI(title="P004 gateway", docs_url=None, redoc_url=None, openapi_url=None)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        raw = request.scope.get("raw_path") or request.url.path.encode()
        target = raw.split(b"?", 1)[0]
        if request.method not in ("GET", "HEAD"):
            return Response("Only GET and HEAD are supported.\n", status_code=405, headers={"Allow": "GET, HEAD"})
        if not target.startswith(b"/") or target.startswith(b"//") or b"/../" in target + b"/" \
                or b"\\" in target or b"%2e%2e" in target.lower():
            return Response("This gateway only serves its own origin.\n", status_code=400)
        return await call_next(request)

    @app.api_route("/{path:path}", methods=["GET", "HEAD"])
    async def proxy(request: Request, path: str):
        upstream_headers = {k: v for k, v in request.headers.items() if k.lower() not in HOP_BY_HOP}
        upstream_headers["accept-encoding"] = "identity"
        url = base + "/" + path + (("?" + request.url.query) if request.url.query else "")
        try:
            with client.stream(request.method, url, headers=upstream_headers) as upstream:
                body = b""
                for chunk in upstream.iter_bytes():
                    body += chunk
                    if len(body) > MAX_BODY:
                        _log(request, 502, "too large")
                        return Response("Upstream response too large.\n", status_code=502)
                status, headers = upstream.status_code, dict(upstream.headers)
        except httpx.HTTPError:
            _log(request, 502, "upstream error")
            return Response("Upstream unavailable.\n", status_code=502)

        out_headers = {k: v for k, v in headers.items() if k.lower() not in HOP_BY_HOP}
        if status != 200 or request.method == "HEAD":
            _log(request, status, "untouched")
            return Response(body, status_code=status, headers=out_headers)

        content_type = headers.get("content-type", "application/octet-stream").split(";")[0].strip().lower()
        facts = facts_for(content_type, body, headers)
        hints = _hints(request)
        plan = decide(facts, hints)
        served, outcome = body, plan.action.upper()
        if plan.action in ("webp", "gzip"):
            try:
                async with limiter:
                    result = await asyncio.wait_for(asyncio.to_thread(_apply, body, plan, policy == "B4"),
                                                    TRANSFORM_TIMEOUT)
                transformed, scores = result
                ok, why = VOC.verify(len(body), len(transformed), scores) if policy == "B4" else (True, "")
                if ok:
                    served, outcome = transformed, plan.action.upper()
                    if plan.action == "webp":
                        out_headers["content-type"] = "image/webp"
                    else:
                        out_headers["content-encoding"] = "gzip"
                else:
                    outcome = f"FALLBACK ({why})"
            except (NotTransformable, asyncio.TimeoutError):
                outcome = "FALLBACK (could not transform)"
        out_headers["vary"] = ", ".join(filter(None, [headers.get("vary"), "Accept, Accept-Encoding, Downlink, Save-Data"]))
        out_headers["x-optimization"] = f"{policy}; {outcome}; {plan.reason}"[:300]
        _log(request, status, outcome)
        return Response(served, status_code=status, headers=out_headers)

    return app


def _apply(body, plan, measure_fidelity):
    if plan.action == "webp":
        out, _ = to_webp(body, plan.quality, plan.max_width)
        return out, (fidelity(body, out) if measure_fidelity else None)
    out, _ = to_gzip(body, plan.level)
    return out, None


def _log(request, status, outcome):
    # Path only: no query string, cookies or authorisation (S9).
    log.info("%s %s %s %s", request.method, request.url.path, status, outcome)


MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "cost_model.json")


def lab_app():
    # B4 without its fitted model would predict no savings and never transform.
    model = CostModel.load(os.environ.get("P004_COST_MODEL", MODEL_PATH))
    return create_app(os.environ.get("P004_ORIGIN", "http://127.0.0.1:8014"), os.environ.get("P004_POLICY", "B4"), model)
