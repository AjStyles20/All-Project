"""StartupMatch web API and page.

Security (first version, local use):
- scrypt passwords; session cookie is HttpOnly, SameSite=Strict, holds a random token whose hash is stored;
- every state-changing request must carry "X-Requested-With: fetch" (a cross-site form cannot set it);
- 5 failed sign-ins per e-mail per 15 minutes, then a pause;
- every route checks the signed-in user and their role; a founder can only act for their own startup, an investor
  for their own fund; contact details are shown only after an intro is accepted.
Run: python -m p008   (binds 127.0.0.1)
"""
import time
from datetime import date
from pathlib import Path

from fastapi import Cookie, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from p008.matching import DISCLAIMER, STAGES, match, rank, says_vs_does
from p008.store import Store, StoreError, as_investor, as_startup

STATIC = Path(__file__).parent / "static"
COOKIE = "sm_session"
STATUSES = {"accepted", "declined", "in-talks", "passed"}
SECTORS = ["fintech", "health", "education", "climate", "devtools", "consumer", "logistics", "ai"]

Text = lambda n: Field(default="", max_length=n)


class Register(BaseModel):
    email: str = Field(min_length=3, max_length=200, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=10, max_length=200)
    role: str = Field(pattern="^(founder|investor)$")
    name: str = Field(min_length=1, max_length=120)


class Login(BaseModel):
    email: str = Field(max_length=200)
    password: str = Field(max_length=200)


class StartupIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    one_liner: str = Text(280)
    sector: str | None = None
    stage: str | None = None
    country: str | None = Field(default=None, max_length=60)
    raising: int | None = Field(default=None, ge=0, le=10 ** 10)
    contact: str = Text(200)
    listed: bool = True


class InvestorIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    sectors: list[str] = Field(default_factory=list, max_length=12)
    stages: list[str] = Field(default_factory=list, max_length=5)
    countries: list[str] = Field(default_factory=list, max_length=20)
    check_min: int | None = Field(default=None, ge=0, le=10 ** 10)
    check_max: int | None = Field(default=None, ge=0, le=10 ** 10)
    contact: str = Text(200)


class DealIn(BaseModel):
    company: str = Field(min_length=1, max_length=120)
    sector: str
    stage: str
    on_date: date
    source: str = Field(min_length=1, max_length=300)
    verified: date | None = None


class IntroIn(BaseModel):
    investor_id: int
    message: str = Field(min_length=10, max_length=1500)


class StatusIn(BaseModel):
    status: str


class MessageIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


def create_app(db_path, today=None, secure_cookie=False) -> FastAPI:
    store = Store(db_path)
    failures = {}
    app = FastAPI(title="StartupMatch", docs_url=None, redoc_url=None, openapi_url=None)
    day = (lambda: today) if today else date.today

    @app.middleware("http")
    async def guard(request: Request, call_next):
        if request.method not in ("GET", "HEAD") and request.headers.get("x-requested-with") != "fetch":
            return JSONResponse({"detail": "Missing request header."}, status_code=403)
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; frame-ancestors 'none'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    def me(token):
        user = store.user_for(token)
        if user is None:
            raise HTTPException(401, "Please sign in.")
        return user

    def role(token, wanted):
        user = me(token)
        if user["role"] != wanted:
            raise HTTPException(403, f"This is for {wanted}s.")
        return user

    def check_vocab(sector=None, stage=None, sectors=(), stages=()):
        for s in ([sector] if sector else []) + list(sectors):
            if s not in SECTORS:
                raise HTTPException(422, f"Unknown sector: {s}")
        for s in ([stage] if stage else []) + list(stages):
            if s not in STAGES:
                raise HTTPException(422, f"Unknown stage: {s}")

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC / "index.html")

    @app.get("/api/vocab")
    def vocab():
        return {"sectors": SECTORS, "stages": STAGES, "disclaimer": DISCLAIMER}

    # ---------- accounts ----------

    @app.post("/api/register", status_code=201)
    def register(p: Register, response: Response):
        try:
            uid = store.register(p.email, p.password, p.role)
        except StoreError as exc:
            raise HTTPException(409, str(exc)) from exc
        if p.role == "founder":
            store.save_startup(uid, {"name": p.name}, day())
        else:
            store.save_investor(uid, {"name": p.name}, day())
        response.set_cookie(COOKIE, store.new_session(uid), httponly=True, samesite="strict", secure=secure_cookie, max_age=7 * 86400)
        return {"role": p.role}

    @app.post("/api/login")
    def login(p: Login, response: Response):
        key = p.email.strip().lower()
        recent = [t for t in failures.get(key, []) if time.time() - t < 900]
        if len(recent) >= 5:
            raise HTTPException(429, "Too many attempts. Try again in a few minutes.")
        user = store.check_password(p.email, p.password)
        if user is None:
            failures[key] = recent + [time.time()]
            raise HTTPException(401, "E-mail or password is wrong.")
        failures.pop(key, None)
        response.set_cookie(COOKIE, store.new_session(user["id"]), httponly=True, samesite="strict", secure=secure_cookie, max_age=7 * 86400)
        return {"role": user["role"]}

    @app.post("/api/logout")
    def logout(response: Response, sm_session: str | None = Cookie(default=None)):
        if sm_session:
            store.end_session(sm_session)
        response.delete_cookie(COOKIE)
        return {"ok": True}

    @app.get("/api/me")
    def whoami(sm_session: str | None = Cookie(default=None)):
        # Signed-out is a normal state for this page, not an error.
        user = store.user_for(sm_session)
        if user is None:
            return {"role": None}
        profile = store.startup_row(owner_id=user["id"]) if user["role"] == "founder" else store.investor_row(owner_id=user["id"])
        return {"email": user["email"], "role": user["role"], "profile": profile}

    # ---------- founders ----------

    @app.put("/api/startup")
    def save_startup(p: StartupIn, sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "founder")
        check_vocab(sector=p.sector, stage=p.stage)
        store.save_startup(user["id"], p.model_dump(), day())
        return store.startup_row(owner_id=user["id"])

    @app.get("/api/matches")
    def matches(sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "founder")
        startup = as_startup(store.startup_row(owner_id=user["id"]))
        rows = {r["id"]: r for r in store.all_investors()}
        ranked = rank(startup, [as_investor(r) for r in rows.values()], day())
        return {"disclaimer": DISCLAIMER, "matches": [{
            "investor_id": m.investor_id, "name": rows[m.investor_id]["name"], "score": m.score, "confidence": m.confidence,
            "components": [vars(c) for c in m.components], "warnings": m.warnings,
            "declared": {k: rows[m.investor_id][k] for k in ("sectors", "stages", "countries", "check_min", "check_max")},
            "deals": [{k: d[k] for k in ("company", "sector", "stage", "on_date", "source", "verified")} for d in rows[m.investor_id]["deals"][:8]],
        } for m in ranked]}

    @app.post("/api/intros", status_code=201)
    def request_intro(p: IntroIn, sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "founder")
        startup = store.startup_row(owner_id=user["id"])
        if store.investor_row(investor_id=p.investor_id) is None:
            raise HTTPException(404, "No such investor.")
        try:
            return {"id": store.create_intro(startup["id"], p.investor_id, p.message)}
        except StoreError as exc:
            raise HTTPException(409, str(exc)) from exc

    # ---------- investors ----------

    @app.put("/api/investor")
    def save_investor(p: InvestorIn, sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "investor")
        check_vocab(sectors=p.sectors, stages=p.stages)
        if p.check_min and p.check_max and p.check_min > p.check_max:
            raise HTTPException(422, "The minimum cheque is above the maximum.")
        store.save_investor(user["id"], p.model_dump(), day())
        return store.investor_row(owner_id=user["id"])

    @app.post("/api/deals", status_code=201)
    def add_deal(p: DealIn, sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "investor")
        check_vocab(sector=p.sector, stage=p.stage)
        inv = store.investor_row(owner_id=user["id"])
        return {"id": store.add_deal(inv["id"], {**p.model_dump(), "on_date": p.on_date.isoformat(),
                                                 "verified": p.verified.isoformat() if p.verified else None})}

    @app.delete("/api/deals/{deal_id}")
    def delete_deal(deal_id: int, sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "investor")
        if not store.delete_deal(store.investor_row(owner_id=user["id"])["id"], deal_id):
            raise HTTPException(404, "No such deal.")
        return {"ok": True}

    @app.get("/api/startups")
    def startups(sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "investor")
        inv = as_investor(store.investor_row(owner_id=user["id"]))
        results = []
        for row in store.listed_startups():
            m = match(as_startup(row), inv, day())
            results.append({"startup_id": row["id"], "name": row["name"], "one_liner": row["one_liner"], "sector": row["sector"],
                            "stage": row["stage"], "country": row["country"], "raising": row["raising"], "score": m.score,
                            "components": [vars(c) for c in m.components if c.name != "recent deals"]})
        results.sort(key=lambda r: (r["score"] is None, -(r["score"] or 0), r["name"]))
        return {"disclaimer": DISCLAIMER, "says_vs_does": says_vs_does(inv, day()), "startups": results}

    # ---------- intros (both sides) ----------

    def view_intro(i, user_id):
        accepted = i["status"] in ("accepted", "in-talks")
        founder = user_id == i["founder_id"]
        return {"id": i["id"], "status": i["status"], "message": i["message"], "created": i["created"], "updated": i["updated"],
                "startup": i["startup_name"], "investor": i["investor_name"], "you": "founder" if founder else "investor",
                # Contact details only after the investor accepts.
                "their_contact": (i["investor_contact"] if founder else i["startup_contact"]) if accepted else None}

    def participant(intro_id, user):
        i = store.intro(intro_id)
        if i is None or user["id"] not in (i["founder_id"], i["investor_owner_id"]):
            raise HTTPException(404, "No such intro.")
        return i

    @app.get("/api/intros")
    def intros(sm_session: str | None = Cookie(default=None)):
        user = me(sm_session)
        return [view_intro(i, user["id"]) for i in store.intros_for(user["id"])]

    @app.post("/api/intros/{intro_id}/status")
    def set_status(intro_id: int, p: StatusIn, sm_session: str | None = Cookie(default=None)):
        user = role(sm_session, "investor")
        i = participant(intro_id, user)
        if p.status not in STATUSES:
            raise HTTPException(422, "Unknown status.")
        if i["status"] in ("declined", "passed"):
            raise HTTPException(409, "This intro is closed.")
        store.set_intro_status(intro_id, p.status)
        return view_intro(store.intro(intro_id), user["id"])

    @app.get("/api/intros/{intro_id}/messages")
    def get_messages(intro_id: int, sm_session: str | None = Cookie(default=None)):
        user = me(sm_session)
        participant(intro_id, user)
        return [{"text": m["text"], "at": m["at"], "from": m["author_role"], "mine": m["author_id"] == user["id"]}
                for m in store.messages(intro_id)]

    @app.post("/api/intros/{intro_id}/messages", status_code=201)
    def post_message(intro_id: int, p: MessageIn, sm_session: str | None = Cookie(default=None)):
        user = me(sm_session)
        i = participant(intro_id, user)
        if i["status"] not in ("accepted", "in-talks"):
            raise HTTPException(409, "Messages open once the investor accepts the intro.")
        store.add_message(intro_id, user["id"], p.text)
        return {"ok": True}

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
