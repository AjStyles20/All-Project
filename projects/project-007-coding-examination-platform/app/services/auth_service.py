from datetime import datetime, timedelta, timezone
from functools import lru_cache
from uuid import uuid4
from app.persistence.user_repository import UserRecord, UserRepository
from app.security.passwords import hash_password, verify_password
from app.security.tokens import issue_token, token_digest

@lru_cache(maxsize=1)
def _decoy_hash() -> str:
    return hash_password("decoy-password-for-unknown-usernames")


class AuthenticationError(ValueError):
    pass

class AuthService:
    def __init__(self, users: UserRepository, session_hours: int = 8):
        self.users = users
        self.session_hours = session_hours

    def create_user(self, user_id: str, username: str, password: str, display_name: str, roles) -> UserRecord:
        normalized = username.strip().lower()
        if not normalized:
            raise ValueError("Username is required.")
        record = UserRecord(user_id, normalized, hash_password(password), display_name.strip(), True)
        self.users.create(record, set(roles))
        return record

    def login(self, username: str, password: str) -> tuple[str, datetime]:
        user = self.users.get_by_username(username.strip().lower())
        # Always do the slow hash, so response time does not reveal whether a username
        # exists or is deactivated.
        matches = verify_password(password, user.password_hash if user else _decoy_hash())
        if user is None or not user.is_active or not matches:
            raise AuthenticationError("Invalid username or password.")
        now = datetime.now(timezone.utc)
        expires = now + timedelta(hours=self.session_hours)
        raw_token, digest = issue_token()
        self.users.store_session(str(uuid4()), user.user_id, digest, now, expires)
        return raw_token, expires

    def authenticate(self, raw_token: str):
        return self.users.principal_for_token_hash(token_digest(raw_token), datetime.now(timezone.utc))

    def logout(self, raw_token: str) -> bool:
        return self.users.revoke_session(token_digest(raw_token), datetime.now(timezone.utc))
