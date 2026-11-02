from dataclasses import dataclass
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
