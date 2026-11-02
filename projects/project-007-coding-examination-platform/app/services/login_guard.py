"""FD-08 login throttling.

Lockouts on an exam platform can be weaponised: anyone could lock a classmate out just as
an exam opens. So the per-user limit is keyed on (username, client IP), locks are short,
existing sessions are never affected, and administrators can clear a lock. Unknown
usernames are counted exactly like real ones, so a lock reveals nothing about who exists.
"""
import hashlib
from datetime import datetime, timedelta, timezone

USER_FAILURE_LIMIT = 5
# High, because a whole lab can share one IP and people mistype at the start of an exam.
IP_FAILURE_LIMIT = 100
WINDOW = timedelta(minutes=15)
LOCK = timedelta(minutes=15)


class LoginThrottled(Exception):
    def __init__(self, retry_after_seconds: int):
        super().__init__("Too many failed sign-in attempts. Please try again later.")
        self.retry_after_seconds = retry_after_seconds


def _digest(*parts: str) -> str:
    # Hashed because the "username" box sometimes receives a mistyped password.
    return hashlib.sha256("\x00".join(parts).encode()).hexdigest()


def user_key(username: str, client_ip: str) -> str:
    return _digest("user", username.strip().lower(), client_ip)


def subject_key(username: str) -> str:
    return _digest("subject", username.strip().lower())


def ip_key(client_ip: str) -> str:
    return _digest("ip", client_ip)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class LoginGuard:
    def __init__(self, repository, clock=_utc_now):
        self.repository = repository
        self.clock = clock

    def check(self, username: str, client_ip: str) -> None:
        now = self.clock()
        latest = self.repository.locked_until([user_key(username, client_ip), ip_key(client_ip)])
        if latest is not None and latest > now:
            raise LoginThrottled(max(1, int((latest - now).total_seconds())))

    def record_failure(self, username: str, client_ip: str) -> bool:
        """Returns True if this failure just locked the (username, IP) pair."""
        now = self.clock()
        self.repository.record_failure(ip_key(client_ip), None, IP_FAILURE_LIMIT, now, now - WINDOW, now + LOCK)
        return self.repository.record_failure(user_key(username, client_ip), subject_key(username),
                                              USER_FAILURE_LIMIT, now, now - WINDOW, now + LOCK)

    def record_success(self, username: str, client_ip: str) -> None:
        # Only this pair: one successful login must not reset an IP-wide attack counter.
        self.repository.clear([user_key(username, client_ip)])
        self.repository.purge_older_than(self.clock() - WINDOW - LOCK)

    def clear_user(self, username: str) -> int:
        """Administrator action: lift a user's lock from every IP."""
        return self.repository.clear_subject(subject_key(username))
