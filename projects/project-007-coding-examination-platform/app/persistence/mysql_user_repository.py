"""MySQL implementation of the operational identity repository."""
import json
from datetime import datetime

from mysql.connector import errors as mysql_errors

from app.domain.identity import (
    AuditAction, AuditEvent, AuthenticatedPrincipal, Role, UserConflictError, UserSummary,
)
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.user_repository import UserRecord


def _write_audit(cursor, event: AuditEvent | None) -> None:
    # Called on the change's own cursor: the change and its record commit or roll back together.
    if event is None:
        return
    cursor.execute(
        "INSERT INTO account_audit_events "
        "(occurred_at, action, actor_user_id, target_user_id, target_username, detail) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (event.occurred_at.replace(tzinfo=None), event.action.value, event.actor_user_id,
         event.target_user_id, event.target_username, json.dumps(event.detail, sort_keys=True)),
    )


class MySQLUserRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def record_audit(self, event: AuditEvent) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            _write_audit(cursor, event)
            cursor.close()

    def list_audit(self, limit: int = 200) -> list[AuditEvent]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT e.*, u.username AS actor_username FROM account_audit_events e "
                           "LEFT JOIN users u ON u.user_id = e.actor_user_id "
                           "ORDER BY e.event_id DESC LIMIT %s", (limit,))
            rows = cursor.fetchall()
            cursor.close()
        return [AuditEvent(r["occurred_at"], AuditAction(r["action"]), r["actor_user_id"], r["target_user_id"],
                           r["target_username"], json.loads(r["detail"]) if isinstance(r["detail"], (str, bytes, bytearray)) else r["detail"],
                           r["actor_username"])
                for r in rows]

    def get_roles(self, user_id: str) -> set[Role]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT role FROM user_roles WHERE user_id = %s", (user_id,))
            rows = cursor.fetchall()
            cursor.close()
        return {Role(r["role"]) for r in rows}

    def create(self, user: UserRecord, roles: set[Role], must_change_password: bool = False,
               audit: AuditEvent | None = None) -> None:
        if not roles:
            raise ValueError("At least one role is required.")
        try:
            with self.database.connect() as connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(
                    "INSERT INTO users (user_id, username, password_hash, display_name, is_active, "
                    "must_change_password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (user.user_id, user.username, user.password_hash, user.display_name, user.is_active,
                     must_change_password),
                )
                cursor.executemany(
                    "INSERT INTO user_roles (user_id, role) VALUES (%s, %s)",
                    [(user.user_id, role.value) for role in roles],
                )
                _write_audit(cursor, audit)
                cursor.close()
        except mysql_errors.IntegrityError as exc:
            raise UserConflictError("That username is already taken.") from exc

    def get_by_id(self, user_id: str) -> UserRecord | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else UserRecord(
            row["user_id"], row["username"], row["password_hash"],
            row["display_name"], bool(row["is_active"])
        )

    def list_users(self) -> list[UserSummary]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, username, display_name, is_active, must_change_password "
                           "FROM users ORDER BY username")
            users = cursor.fetchall()
            cursor.execute("SELECT user_id, role FROM user_roles")
            role_rows = cursor.fetchall()
            cursor.close()
        roles: dict[str, set[Role]] = {}
        for item in role_rows:
            roles.setdefault(item["user_id"], set()).add(Role(item["role"]))
        return [UserSummary(u["user_id"], u["username"], u["display_name"], bool(u["is_active"]),
                            bool(u["must_change_password"]), frozenset(roles.get(u["user_id"], set())))
                for u in users]

    @staticmethod
    def _other_active_admins(cursor, user_id: str) -> int:
        # FOR UPDATE: two administrators demoting each other at the same moment must
        # queue here, or each could see the other as the remaining administrator.
        cursor.execute(
            "SELECT u.user_id FROM users u JOIN user_roles r ON r.user_id = u.user_id "
            "WHERE r.role = 'ADMINISTRATOR' AND u.is_active = TRUE FOR UPDATE", ())
        return sum(1 for row in cursor.fetchall() if row[0] != user_id)

    @staticmethod
    def _is_active_admin(cursor, user_id: str) -> bool:
        cursor.execute(
            "SELECT 1 FROM users u JOIN user_roles r ON r.user_id = u.user_id "
            "WHERE u.user_id = %s AND r.role = 'ADMINISTRATOR' AND u.is_active = TRUE", (user_id,))
        return cursor.fetchone() is not None

    def set_active(self, user_id: str, active: bool, audit: AuditEvent | None = None) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            if not active:
                others = self._other_active_admins(cursor, user_id)
                if self._is_active_admin(cursor, user_id) and others == 0:
                    raise UserConflictError("This is the last active administrator.")
            cursor.execute("UPDATE users SET is_active = %s WHERE user_id = %s", (active, user_id))
            _write_audit(cursor, audit)
            cursor.close()

    def set_roles(self, user_id: str, roles: set[Role], audit: AuditEvent | None = None) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            if Role.ADMINISTRATOR not in roles:
                others = self._other_active_admins(cursor, user_id)
                if self._is_active_admin(cursor, user_id) and others == 0:
                    raise UserConflictError("This is the last active administrator.")
            cursor.execute("DELETE FROM user_roles WHERE user_id = %s", (user_id,))
            cursor.executemany("INSERT INTO user_roles (user_id, role) VALUES (%s, %s)",
                               [(user_id, role.value) for role in roles])
            _write_audit(cursor, audit)
            cursor.close()

    def set_password(self, user_id: str, password_hash: str, *, must_change_password: bool,
                     audit: AuditEvent | None = None) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE users SET password_hash = %s, must_change_password = %s WHERE user_id = %s",
                           (password_hash, must_change_password, user_id))
            _write_audit(cursor, audit)
            cursor.close()

    def revoke_user_sessions(self, user_id: str, revoked_at: datetime, keep_token_hash: str | None = None) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE auth_sessions SET revoked_at = %s WHERE user_id = %s AND revoked_at IS NULL "
                "AND token_hash <> %s",
                (revoked_at.replace(tzinfo=None), user_id, keep_token_hash or ""))
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
                "SELECT user_id, username, must_change_password FROM users "
                "WHERE user_id = %s AND is_active = TRUE",
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
            bool(row["must_change_password"]),
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
