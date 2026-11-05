"""P010 web API and page. Run: uvicorn p010.api:app --port 8012

First version: games in memory, no accounts. A seat is held by whoever has its secret link.
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from p010.arbiter import Contract
from p010.games import GameError, Games

STATIC = Path(__file__).parent / "static"


class NewGame(BaseModel):
    contract: Contract = Contract.SOCIAL


class MoveInput(BaseModel):
    token: str = Field(min_length=1, max_length=64)
    uci: str = Field(min_length=4, max_length=5)


class TokenInput(BaseModel):
    token: str = Field(min_length=1, max_length=64)


class ChatInput(BaseModel):
    token: str | None = Field(default=None, max_length=64)
    name: str = Field(default="spectator", min_length=1, max_length=30)
    text: str = Field(min_length=1, max_length=300)


def create_app() -> FastAPI:
    games = Games()
    app = FastAPI(title="P010 Chess")

    @app.middleware("http")
    async def headers(request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; object-src 'none'; frame-ancestors 'none'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    def fail(exc: GameError):
        raise HTTPException(exc.status, str(exc)) from exc

    @app.get("/", include_in_schema=False)
    def index():
        return FileResponse(STATIC / "index.html")

    @app.post("/api/games", status_code=201)
    def new_game(payload: NewGame):
        game, tokens = games.create(payload.contract)
        return {"game_id": game.game_id, "white_token": tokens["white"], "black_token": tokens["black"]}

    @app.get("/api/games/{game_id}")
    def view(game_id: str, since: int = Query(default=0, ge=0)):
        try:
            return games.get(game_id).view(since)
        except GameError as exc:
            fail(exc)

    @app.post("/api/games/{game_id}/move")
    def move(game_id: str, payload: MoveInput):
        try:
            return games.move(game_id, payload.token, payload.uci).view()
        except GameError as exc:
            fail(exc)

    @app.post("/api/games/{game_id}/resign")
    def resign(game_id: str, payload: TokenInput):
        try:
            return games.resign(game_id, payload.token).view()
        except GameError as exc:
            fail(exc)

    @app.post("/api/games/{game_id}/chat", status_code=201)
    def chat(game_id: str, payload: ChatInput):
        try:
            return games.chat(game_id, payload.token, payload.name, payload.text).__dict__
        except GameError as exc:
            fail(exc)

    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app


app = create_app()
