"""FD-07 user management: accounts, roles, one-time passwords, own password change."""
import secrets
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.identity import Role, UserConflictError, UserSummary
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
    def __init__(self, repository):
        self.users = repository

    # Administrator

    def list_users(self) -> list[UserSummary]:
        return self.users.list_users()

    def list_candidates(self) -> list[UserSummary]:
        return [u for u in self.users.list_users() if u.is_active and Role.CANDIDATE in u.roles]

    def create_user(self, username: str, display_name: str, roles: set[Role]) -> tuple[UserSummary, str]:
        """Returns the account and its one-time password; only the hash is stored."""
        normalized = username.strip().lower()
        if not normalized or not display_name.strip():
            raise ValueError("Username and display name are required.")
        if not roles:
            raise ValueError("At least one role is required.")
        password = one_time_password()
        record = UserRecord(str(uuid4()), normalized, hash_password(password), display_name.strip(), True)
        self.users.create(record, set(roles), must_change_password=True)
        return UserSummary(record.user_id, normalized, record.display_name, True, True, frozenset(roles)), password

    def set_active(self, actor_user_id: str, user_id: str, active: bool) -> None:
        if not active and actor_user_id == user_id:
            raise UserConflictError("You cannot deactivate your own account.")
        self._require(user_id)
        self.users.set_active(user_id, active)
        if not active:
            # Otherwise old sessions would come back to life on reactivation.
            self.users.revoke_user_sessions(user_id, self._now())

    def set_roles(self, actor_user_id: str, user_id: str, roles: set[Role]) -> None:
        if not roles:
            raise ValueError("At least one role is required.")
        if actor_user_id == user_id and Role.ADMINISTRATOR not in roles:
            raise UserConflictError("You cannot remove your own administrator role.")
        self._require(user_id)
        self.users.set_roles(user_id, set(roles))

    def reset_password(self, user_id: str) -> str:
        self._require(user_id)
        password = one_time_password()
        self.users.set_password(user_id, hash_password(password), must_change_password=True)
        self.users.revoke_user_sessions(user_id, self._now())
        return password

    # Any signed-in user

    def change_own_password(self, user_id: str, current_password: str, new_password: str, raw_token: str) -> None:
        record = self.users.get_by_id(user_id)
        if record is None or not verify_password(current_password, record.password_hash):
            raise WrongPasswordError("Current password is incorrect.")
        check_new_password(new_password, record.username)
        if new_password == current_password:
            raise ValueError("New password must be different from the current one.")
        self.users.set_password(user_id, hash_password(new_password), must_change_password=False)
        # Other devices signed in with the old password are signed out; this one stays.
        self.users.revoke_user_sessions(user_id, self._now(), keep_token_hash=token_digest(raw_token))

    def _require(self, user_id: str) -> None:
        if self.users.get_by_id(user_id) is None:
            raise UserNotFoundError("User not found.")

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
