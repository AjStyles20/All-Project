"""FD-07 user management: accounts, roles, one-time passwords, own password change."""
import secrets
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.identity import AuditAction, AuditEvent, Role, UserConflictError, UserSummary
from app.persistence.user_repository import UserRecord
from app.security.passwords import hash_password, verify_password
from app.security.tokens import token_digest

MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_LENGTH = 128


class UserNotFoundError(LookupError):
    pass


class WrongPasswordError(ValueError):
    pass


def check_new_password(password: str, username: str) -> None:
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise ValueError(f"Password must be {MIN_PASSWORD_LENGTH} to {MAX_PASSWORD_LENGTH} characters.")
    if username.lower() in password.lower():
        raise ValueError("Password must not contain the username.")


def one_time_password() -> str:
    return secrets.token_urlsafe(15)


class UserAdminService:
    def __init__(self, repository, login_guard=None):
        self.users = repository
        self.login_guard = login_guard

    def _event(self, action: AuditAction, actor: str | None, user_id: str, username: str, **detail) -> AuditEvent:
        return AuditEvent(self._now(), action, actor, user_id, username, detail)

    def list_audit(self, limit: int = 200) -> list[AuditEvent]:
        return self.users.list_audit(limit)

    # Administrator

    def list_users(self) -> list[UserSummary]:
        return self.users.list_users()

    def list_candidates(self) -> list[UserSummary]:
        return [u for u in self.users.list_users() if u.is_active and Role.CANDIDATE in u.roles]

    def create_user(self, actor_user_id: str | None, username: str, display_name: str,
                    roles: set[Role]) -> tuple[UserSummary, str]:
        """Returns the account and its one-time password; only the hash is stored."""
        normalized = username.strip().lower()
        if not normalized or not display_name.strip():
            raise ValueError("Username and display name are required.")
        if not roles:
            raise ValueError("At least one role is required.")
        password = one_time_password()
        record = UserRecord(str(uuid4()), normalized, hash_password(password), display_name.strip(), True)
        self.users.create(record, set(roles), must_change_password=True, audit=self._event(
            AuditAction.USER_CREATED, actor_user_id, record.user_id, normalized, roles=sorted(r.value for r in roles)))
        return UserSummary(record.user_id, normalized, record.display_name, True, True, frozenset(roles)), password

    def set_active(self, actor_user_id: str, user_id: str, active: bool) -> None:
        if not active and actor_user_id == user_id:
            raise UserConflictError("You cannot deactivate your own account.")
        record = self._require(user_id)
        action = AuditAction.REACTIVATED if active else AuditAction.DEACTIVATED
        self.users.set_active(user_id, active, audit=self._event(action, actor_user_id, user_id, record.username))
        if not active:
            # Otherwise old sessions would come back to life on reactivation.
            self.users.revoke_user_sessions(user_id, self._now())

    def set_roles(self, actor_user_id: str, user_id: str, roles: set[Role]) -> None:
        if not roles:
            raise ValueError("At least one role is required.")
        if actor_user_id == user_id and Role.ADMINISTRATOR not in roles:
            raise UserConflictError("You cannot remove your own administrator role.")
        record = self._require(user_id)
        before = sorted(r.value for r in self.users.get_roles(user_id))
        self.users.set_roles(user_id, set(roles), audit=self._event(
            AuditAction.ROLES_CHANGED, actor_user_id, user_id, record.username,
            roles_before=before, roles_after=sorted(r.value for r in roles)))

    def reset_password(self, actor_user_id: str, user_id: str) -> str:
        record = self._require(user_id)
        password = one_time_password()
        self.users.set_password(user_id, hash_password(password), must_change_password=True, audit=self._event(
            AuditAction.PASSWORD_RESET, actor_user_id, user_id, record.username))
        self.users.revoke_user_sessions(user_id, self._now())
        if self.login_guard is not None:
            self.login_guard.clear_user(record.username)
        return password

    def clear_login_lock(self, actor_user_id: str, user_id: str) -> int:
        record = self._require(user_id)
        removed = self.login_guard.clear_user(record.username)
        self.users.record_audit(self._event(AuditAction.LOGIN_LOCK_CLEARED, actor_user_id, user_id, record.username))
        return removed

    def record_login_lock(self, username: str, client_ip: str) -> None:
        """Audited only for real accounts: typed text that matches no user is never stored."""
        record = self.users.get_by_username(username.strip().lower())
        if record is not None:
            self.users.record_audit(self._event(AuditAction.LOGIN_LOCKED, None, record.user_id, record.username,
                                                client_ip=client_ip))

    # Any signed-in user

    def change_own_password(self, user_id: str, current_password: str, new_password: str, raw_token: str) -> None:
        record = self.users.get_by_id(user_id)
        if record is None or not verify_password(current_password, record.password_hash):
            raise WrongPasswordError("Current password is incorrect.")
        check_new_password(new_password, record.username)
        if new_password == current_password:
            raise ValueError("New password must be different from the current one.")
        self.users.set_password(user_id, hash_password(new_password), must_change_password=False, audit=self._event(
            AuditAction.PASSWORD_CHANGED, user_id, user_id, record.username))
        # Other devices signed in with the old password are signed out; this one stays.
        self.users.revoke_user_sessions(user_id, self._now(), keep_token_hash=token_digest(raw_token))

    def _require(self, user_id: str) -> UserRecord:
        record = self.users.get_by_id(user_id)
        if record is None:
            raise UserNotFoundError("User not found.")
        return record

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
