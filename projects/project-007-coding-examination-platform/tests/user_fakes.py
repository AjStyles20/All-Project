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
        self.audit = []

    def record_audit(self, event):
        self.audit.append(event)

    def list_audit(self, limit=200):
        return list(reversed(self.audit))[:limit]

    def get_roles(self, user_id):
        return set(self.roles[user_id])

    def create(self, user, roles, must_change_password=False, audit=None):
        if any(r.username == user.username for r in self.records.values()):
            raise UserConflictError("That username is already taken.")
        self.records[user.user_id] = user
        self.roles[user.user_id] = set(roles)
        self.must_change[user.user_id] = must_change_password
        if audit:
            self.audit.append(audit)

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

    def set_active(self, user_id, active, audit=None):
        if not active:
            self._guard_last_admin(user_id)
        self.records[user_id] = replace(self.records[user_id], is_active=active)
        if audit:
            self.audit.append(audit)

    def set_roles(self, user_id, roles, audit=None):
        if Role.ADMINISTRATOR not in roles:
            self._guard_last_admin(user_id)
        self.roles[user_id] = set(roles)
        if audit:
            self.audit.append(audit)

    def set_password(self, user_id, password_hash, *, must_change_password, audit=None):
        self.records[user_id] = replace(self.records[user_id], password_hash=password_hash)
        self.must_change[user_id] = must_change_password
        if audit:
            self.audit.append(audit)

    def revoke_user_sessions(self, user_id, revoked_at, keep_token_hash=None):
        self.sessions = {h: u for h, u in self.sessions.items() if u != user_id or h == keep_token_hash}


class InMemoryLoginThrottleRepository:
    """Mirrors the SQL upsert: window reset, lock when the limit is reached, position returned."""
    def __init__(self):
        self.rows = {}  # key -> dict(subject, count, started, locked)

    def locked_until(self, keys):
        locks = [self.rows[k]["locked"] for k in keys if k in self.rows and self.rows[k]["locked"]]
        return max(locks) if locks else None

    def reserve(self, key, subject_key, limit, now, window_cutoff, lock_until):
        row = self.rows.get(key)
        if row is None:
            self.rows[key] = row = {"subject": subject_key, "count": 1, "started": now, "locked": None}
        elif row["started"] >= window_cutoff:
            row["count"] += 1
            if row["count"] >= limit:
                row["locked"] = lock_until
        else:
            row.update(count=1, started=now)
        return row["count"]

    def refund(self, key):
        if key in self.rows:
            self.rows[key]["count"] = max(self.rows[key]["count"] - 1, 0)

    def clear(self, keys):
        for key in keys:
            self.rows.pop(key, None)

    def clear_subject(self, subject_key):
        keys = [k for k, r in self.rows.items() if r["subject"] == subject_key]
        self.clear(keys)
        return len(keys)

    def purge_older_than(self, cutoff):
        for key in [k for k, r in self.rows.items() if r["started"] < cutoff and (not r["locked"] or r["locked"] < cutoff)]:
            del self.rows[key]
