from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    CANDIDATE = "CANDIDATE"
    EXAMINER = "EXAMINER"
    ADMINISTRATOR = "ADMINISTRATOR"
    INDEPENDENT_ASSESSOR = "INDEPENDENT_ASSESSOR"

@dataclass(frozen=True)
class AuthenticatedPrincipal:
    user_id: str
    username: str
    roles: frozenset[Role]
    # FD-07: signed in with a one-time password; the API allows only changing it.
    must_change_password: bool = False

    def has_any_role(self, allowed: set[Role]) -> bool:
        return bool(self.roles.intersection(allowed))


@dataclass(frozen=True)
class UserSummary:
    user_id: str
    username: str
    display_name: str
    is_active: bool
    must_change_password: bool
    roles: frozenset[Role]


class UserConflictError(ValueError):
    """The change collides with existing accounts or would lock administrators out."""


class AuditAction(str, Enum):
    USER_CREATED = "USER_CREATED"
    ROLES_CHANGED = "ROLES_CHANGED"
    DEACTIVATED = "DEACTIVATED"
    REACTIVATED = "REACTIVATED"
    PASSWORD_RESET = "PASSWORD_RESET"
    PASSWORD_CHANGED = "PASSWORD_CHANGED"
    LOGIN_LOCKED = "LOGIN_LOCKED"
    LOGIN_LOCK_CLEARED = "LOGIN_LOCK_CLEARED"


@dataclass(frozen=True)
class AuditEvent:
    """Never holds passwords or hashes. actor_user_id is None for script or automatic events."""
    occurred_at: datetime
    action: AuditAction
    actor_user_id: str | None
    target_user_id: str
    target_username: str
    detail: dict = field(default_factory=dict)
