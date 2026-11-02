"""In-memory stand-in for the FD-07 side of MySQLUserRepository, mirroring its guards:
unique usernames, last-active-administrator protection, keep-one-session revocation."""
from dataclasses import replace

from app.domain.identity import AuthenticatedPrincipal, Role, UserConflictError, UserSummary


class InMemoryUserRepository:
    def __init__(self):
        self.records = {}
        self.roles = {}
        self.must_change = {}
        self.sessions = {}  # token_hash -> user_id

    def create(self, user, roles, must_change_password=False):
        if any(r.username == user.username for r in self.records.values()):
            raise UserConflictError("That username is already taken.")
        self.records[user.user_id] = user
        self.roles[user.user_id] = set(roles)
        self.must_change[user.user_id] = must_change_password

    def get_by_id(self, user_id):
        return self.records.get(user_id)

    def get_by_username(self, username):
        return next((r for r in self.records.values() if r.username == username), None)

    def list_users(self):
        return [UserSummary(r.user_id, r.username, r.display_name, r.is_active, self.must_change[r.user_id],
                            frozenset(self.roles[r.user_id]))
                for r in sorted(self.records.values(), key=lambda r: r.username)]

    def principal_for_user(self, user_id):
        record = self.records.get(user_id)
        if record is None or not record.is_active:
            return None
        return AuthenticatedPrincipal(user_id, record.username, frozenset(self.roles[user_id]), self.must_change[user_id])

    def _guard_last_admin(self, user_id):
        others = [u for u, r in self.records.items()
                  if u != user_id and r.is_active and Role.ADMINISTRATOR in self.roles[u]]
        if self.records[user_id].is_active and Role.ADMINISTRATOR in self.roles[user_id] and not others:
            raise UserConflictError("This is the last active administrator.")

    def set_active(self, user_id, active):
        if not active:
            self._guard_last_admin(user_id)
        self.records[user_id] = replace(self.records[user_id], is_active=active)

    def set_roles(self, user_id, roles):
        if Role.ADMINISTRATOR not in roles:
            self._guard_last_admin(user_id)
        self.roles[user_id] = set(roles)

    def set_password(self, user_id, password_hash, *, must_change_password):
        self.records[user_id] = replace(self.records[user_id], password_hash=password_hash)
        self.must_change[user_id] = must_change_password

    def revoke_user_sessions(self, user_id, revoked_at, keep_token_hash=None):
        self.sessions = {h: u for h, u in self.sessions.items() if u != user_id or h == keep_token_hash}
