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

    def has_any_role(self, allowed: set[Role]) -> bool:
        return bool(self.roles.intersection(allowed))
