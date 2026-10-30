from dataclasses import dataclass
from datetime import datetime
from app.domain.identity import AuthenticatedPrincipal, Role
from app.persistence.database import Database

@dataclass(frozen=True)
class UserRecord:
    user_id: str
    username: str
    password_hash: str
    display_name: str
    is_active: bool

class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    def create(self, user: UserRecord, roles: set[Role]) -> None:
        if not roles:
            raise ValueError("At least one role is required.")
        with self.database.connect() as c:
            c.execute("INSERT INTO users (user_id, username, password_hash, display_name, is_active) VALUES (?, ?, ?, ?, ?)",
                      (user.user_id, user.username, user.password_hash, user.display_name, int(user.is_active)))
            c.executemany("INSERT INTO user_roles (user_id, role) VALUES (?, ?)",
                          [(user.user_id, role.value) for role in roles])

    def get_by_username(self, username: str) -> UserRecord | None:
        with self.database.connect() as c:
            row = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return None if row is None else UserRecord(row["user_id"], row["username"], row["password_hash"], row["display_name"], bool(row["is_active"]))

    def principal_for_user(self, user_id: str) -> AuthenticatedPrincipal | None:
        with self.database.connect() as c:
            row = c.execute("SELECT user_id, username FROM users WHERE user_id = ? AND is_active = 1", (user_id,)).fetchone()
            if row is None:
                return None
            role_rows = c.execute("SELECT role FROM user_roles WHERE user_id = ?", (user_id,)).fetchall()
        return AuthenticatedPrincipal(row["user_id"], row["username"], frozenset(Role(r["role"]) for r in role_rows))

    def store_session(self, session_id: str, user_id: str, token_hash: str, created_at: datetime, expires_at: datetime) -> None:
        with self.database.connect() as c:
            c.execute("INSERT INTO auth_sessions (session_id, user_id, token_hash, created_at, expires_at, revoked_at) VALUES (?, ?, ?, ?, ?, NULL)",
                      (session_id, user_id, token_hash, created_at.isoformat(), expires_at.isoformat()))

    def principal_for_token_hash(self, token_hash: str, now: datetime) -> AuthenticatedPrincipal | None:
        with self.database.connect() as c:
            row = c.execute("SELECT user_id FROM auth_sessions WHERE token_hash = ? AND revoked_at IS NULL AND expires_at > ?",
                            (token_hash, now.isoformat())).fetchone()
        return None if row is None else self.principal_for_user(row["user_id"])

    def revoke_session(self, token_hash: str, revoked_at: datetime) -> bool:
        with self.database.connect() as c:
            cursor = c.execute("UPDATE auth_sessions SET revoked_at = ? WHERE token_hash = ? AND revoked_at IS NULL",
                               (revoked_at.isoformat(), token_hash))
        return cursor.rowcount == 1
