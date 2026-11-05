"""P007 web API and dashboard.

Demonstration build for synthetic data: there is no sign-in, and the issuer is whoever the
caller says it is. The ledger's own rules (scope, balance, stock, single reversal) still hold.
Run: uvicorn p007.api:default_app --factory  (P007_DB_PATH sets the SQLite file, default ./p007.sqlite3)
"""
import os
import time
from dataclasses import asdict
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from p007.audit import ENGINES
from p007.benchmark import SCENARIO_NAMES, SCENARIOS, generate
from p007.store import Ledger, LedgerError

STATIC = Path(__file__).parent / "static"
ID = Field(min_length=1, max_length=64)


class EarnInput(BaseModel):
    issuer_id: str = ID
    student_id: str = ID
    policy_id: str = ID
    measure: float | None = Field(default=None, ge=0, le=100000)


class RedeemInput(BaseModel):
    student_id: str = ID
    reward_id: str = ID


class ReverseInput(BaseModel):
    transaction_id: str = ID
    issuer_id: str = ID


class DemoInput(BaseModel):
    scenario: str = Field(pattern="^S[0-8]$")
    seed: int = Field(default=1, ge=0, le=1_000_000)


def create_app(db_path) -> FastAPI:
    ledger = Ledger(db_path)
    app = FastAPI(title="P007 School Points")

    def refuse(exc: LedgerError):
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    @app.middleware("http")
    async def security_headers(request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; frame-ancestors 'none'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/students")
    def students():
        return ledger.balances()

    @app.get("/api/rewards")
    def rewards():
        return ledger.rewards()

    @app.get("/api/policies")
    def policies():
        return [asdict(p) for p in ledger.load_dataset().policies.values()]

    @app.get("/api/scenarios")
    def scenarios():
        return [{"id": s, "name": SCENARIO_NAMES[s]} for s in SCENARIOS]

    @app.post("/api/earn", status_code=201)
    def earn(payload: EarnInput):
        try:
            return {"transaction_id": ledger.earn(payload.issuer_id, payload.student_id, payload.policy_id,
                                                  int(time.time()), payload.measure)}
        except LedgerError as exc:
            refuse(exc)

    @app.post("/api/redeem", status_code=201)
    def redeem(payload: RedeemInput):
        try:
            return {"transaction_id": ledger.redeem(payload.student_id, payload.reward_id, int(time.time()))}
        except LedgerError as exc:
            refuse(exc)

    @app.post("/api/reverse", status_code=201)
    def reverse(payload: ReverseInput):
        try:
            return {"transaction_id": ledger.reverse(payload.transaction_id, payload.issuer_id, int(time.time()))}
        except LedgerError as exc:
            refuse(exc)

    @app.get("/api/audit")
    def audit(engine: str = Query(default="B4", pattern="^B[0-4]$")):
        report = ENGINES[engine](ledger.load_dataset())
        return {"engine": report.engine, "state": report.state.value,
                "findings": [{**asdict(f), "state": f.state.value} for f in report.findings]}

    @app.post("/api/demo", status_code=201)
    def demo(payload: DemoInput):
        # Loads synthetic data only; the scenario's ground truth is never stored or returned.
        dataset, _ = generate(payload.scenario, payload.seed)
        try:
            ledger.import_dataset(dataset)
        except LedgerError as exc:
            refuse(exc)
        return {"students": len(dataset.students), "transactions": len(dataset.transactions)}

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app


def default_app() -> FastAPI:
    # A factory, so importing this module never creates a database file.
    return create_app(os.environ.get("P007_DB_PATH", "p007.sqlite3"))
