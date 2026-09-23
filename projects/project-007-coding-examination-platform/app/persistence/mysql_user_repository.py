"""MySQL implementation of the operational identity repository."""
from datetime import datetime

from app.domain.identity import AuthenticatedPrincipal, Role
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.user_repository import UserRecord


class MySQLUserRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def create(self, user: UserRecord, roles: set[Role]) -> None:
        if not roles:
            raise ValueError("At least one role is required.")
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "INSERT INTO users (user_id, username, password_hash, display_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s)",
                (user.user_id, user.username, user.password_hash, user.display_name, user.is_active),
            )
            cursor.executemany(
                "INSERT INTO user_roles (user_id, role) VALUES (%s, %s)",
                [(user.user_id, role.value) for role in roles],
            )
            cursor.close()

    def get_by_username(self, username: str) -> UserRecord | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else UserRecord(
            row["user_id"], row["username"], row["password_hash"],
            row["display_name"], bool(row["is_active"])
        )

    def principal_for_user(self, user_id: str) -> AuthenticatedPrincipal | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id, username FROM users WHERE user_id = %s AND is_active = TRUE",
                (user_id,),
            )
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                return None
            cursor.execute("SELECT role FROM user_roles WHERE user_id = %s", (user_id,))
            role_rows = cursor.fetchall()
            cursor.close()
        return AuthenticatedPrincipal(
            row["user_id"], row["username"],
            frozenset(Role(item["role"]) for item in role_rows),
        )

    def store_session(self, session_id: str, user_id: str, token_hash: str,
                      created_at: datetime, expires_at: datetime) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO auth_sessions "
                "(session_id, user_id, token_hash, created_at, expires_at, revoked_at) "
                "VALUES (%s, %s, %s, %s, %s, NULL)",
                (session_id, user_id, token_hash,
                 created_at.replace(tzinfo=None), expires_at.replace(tzinfo=None)),
            )
            cursor.close()

    def principal_for_token_hash(self, token_hash: str, now: datetime) -> AuthenticatedPrincipal | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_id FROM auth_sessions "
                "WHERE token_hash = %s AND revoked_at IS NULL AND expires_at > %s",
                (token_hash, now.replace(tzinfo=None)),
            )
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else self.principal_for_user(row["user_id"])

    def revoke_session(self, token_hash: str, revoked_at: datetime) -> bool:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE auth_sessions SET revoked_at = %s "
                "WHERE token_hash = %s AND revoked_at IS NULL",
                (revoked_at.replace(tzinfo=None), token_hash),
            )
            changed = cursor.rowcount
            cursor.close()
        return changed == 1
