"""FD-08: login throttling, timing-safe login, and the account audit trail."""
from datetime import datetime, timedelta

import pytest

from app.domain.identity import AuditAction, Role, UserConflictError
from app.persistence.mysql_login_throttle_repository import MySQLLoginThrottleRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.persistence.user_repository import UserRecord
from app.security.passwords import hash_password
from app.services import auth_service as auth_module
from app.services.auth_service import AuthenticationError, AuthService
from app.services.login_guard import IP_FAILURE_LIMIT, USER_FAILURE_LIMIT, LoginGuard, LoginThrottled
from app.services.user_admin_service import UserAdminService
from tests.unit.test_mysql_examination_repository import FakeDatabase
from tests.user_fakes import InMemoryLoginThrottleRepository, InMemoryUserRepository

T0 = datetime(2026, 11, 2, 9, 0)


class Clock:
    def __init__(self): self.now = T0
    def __call__(self): return self.now


def guard_and_clock():
    clock = Clock()
    return LoginGuard(InMemoryLoginThrottleRepository(), clock), clock


def fail(guard, user="ada", ip="10.0.0.1", times=1):
    """Full attempts that end in a wrong password, in the order the API runs them."""
    result = False
    for _ in range(times):
        result = guard.attempt_failed(guard.begin(user, ip))
    return result


def test_lock_after_limit_then_expires():
    guard, clock = guard_and_clock()
    assert fail(guard, times=USER_FAILURE_LIMIT - 1) is False
    assert fail(guard) is True  # this failure caused the lock
    with pytest.raises(LoginThrottled) as locked:
        guard.begin("ada", "10.0.0.1")
    assert 0 < locked.value.retry_after_seconds <= 900
    clock.now = T0 + timedelta(minutes=16)
    guard.begin("ada", "10.0.0.1")


def test_parallel_attempts_cannot_exceed_the_limit():
    # The bug found in browser testing: requests all pass the lock check while earlier ones
    # are still hashing. Here none has finished, and the locked_until check is blinded, so
    # only the atomic count can stop them.
    guard, _ = guard_and_clock()
    guard.repository.locked_until = lambda keys: None
    allowed = throttled = 0
    for _ in range(USER_FAILURE_LIMIT + 10):
        try:
            guard.begin("ada", "10.0.0.1")
            allowed += 1
        except LoginThrottled:
            throttled += 1
    assert (allowed, throttled) == (USER_FAILURE_LIMIT, 10)


def test_correct_password_on_the_last_allowed_attempt_still_works():
    guard, _ = guard_and_clock()
    fail(guard, times=USER_FAILURE_LIMIT - 1)
    guard.begin("ada", "10.0.0.1")
    guard.attempt_succeeded("ada", "10.0.0.1")
    fail(guard, times=USER_FAILURE_LIMIT - 1)  # the count started again
    guard.begin("ada", "10.0.0.1")


def test_attacker_elsewhere_cannot_lock_the_real_user_out():
    guard, _ = guard_and_clock()
    fail(guard, ip="203.0.113.9", times=USER_FAILURE_LIMIT)
    with pytest.raises(LoginThrottled):
        guard.begin("ada", "203.0.113.9")
    guard.begin("ada", "10.0.0.1")  # same account, different address: unaffected


def test_unknown_usernames_lock_exactly_like_real_ones():
    guard, _ = guard_and_clock()
    fail(guard, user="no-such-person", times=USER_FAILURE_LIMIT)
    with pytest.raises(LoginThrottled):
        guard.begin("no-such-person", "10.0.0.1")


def test_ip_wide_limit_stops_spraying_many_usernames():
    guard, _ = guard_and_clock()
    for n in range(IP_FAILURE_LIMIT):
        fail(guard, user=f"user{n}", ip="198.51.100.7")
    with pytest.raises(LoginThrottled):
        guard.begin("brand-new-name", "198.51.100.7")
    guard.begin("brand-new-name", "10.0.0.1")


def test_a_lab_signing_in_correctly_from_one_ip_is_never_throttled():
    guard, _ = guard_and_clock()
    for n in range(IP_FAILURE_LIMIT * 3):
        guard.begin(f"student{n}", "192.0.2.1")
        guard.attempt_succeeded(f"student{n}", "192.0.2.1")
    guard.begin("one-more", "192.0.2.1")


def test_old_failures_fall_out_of_the_window():
    guard, clock = guard_and_clock()
    fail(guard, times=USER_FAILURE_LIMIT - 1)
    clock.now = T0 + timedelta(minutes=16)
    assert fail(guard) is False
    guard.begin("ada", "10.0.0.1")


def test_success_clears_the_pair_but_keeps_earlier_ip_failures():
    guard, _ = guard_and_clock()
    fail(guard, times=3)
    guard.begin("ada", "10.0.0.1")
    guard.attempt_succeeded("ada", "10.0.0.1")
    from app.services.login_guard import ip_key
    assert guard.repository.rows[ip_key("10.0.0.1")]["count"] == 3


def test_stored_keys_never_contain_what_was_typed():
    guard, _ = guard_and_clock()
    fail(guard, user="MySecretPasswordTypedInTheWrongBox")
    for key, row in guard.repository.rows.items():
        assert "secret" not in key.lower() and len(key) == 64
        assert row["subject"] is None or "secret" not in row["subject"].lower()


def test_administrator_clear_works_from_any_ip():
    guard, _ = guard_and_clock()
    fail(guard, ip="10.0.0.1", times=USER_FAILURE_LIMIT)
    fail(guard, ip="10.0.0.2", times=USER_FAILURE_LIMIT)
    assert guard.clear_user("ADA ") == 2
    guard.begin("ada", "10.0.0.1")
    guard.begin("ada", "10.0.0.2")


# ---- timing ----

def test_unknown_and_deactivated_users_still_do_the_slow_hash(monkeypatch):
    calls = []
    real = auth_module.verify_password
    monkeypatch.setattr(auth_module, "verify_password", lambda p, h: (calls.append(h), real(p, h))[1])
    repo = InMemoryUserRepository()
    repo.create(UserRecord("u1", "gone", hash_password("a-long-enough-one"), "Gone", False), {Role.CANDIDATE})
    auth = AuthService(repo)
    with pytest.raises(AuthenticationError):
        auth.login("nobody", "whatever")
    with pytest.raises(AuthenticationError):
        auth.login("gone", "a-long-enough-one")  # right password, deactivated: still refused
    assert len(calls) == 2


# ---- audit ----

def accounts_with_admin():
    repo = InMemoryUserRepository()
    repo.create(UserRecord("admin-1", "root", hash_password("AdminPassword123"), "Root", True), {Role.ADMINISTRATOR})
    guard = LoginGuard(InMemoryLoginThrottleRepository())
    return UserAdminService(repo, guard), repo, guard


def test_every_account_change_is_audited_without_secrets():
    service, repo, _ = accounts_with_admin()
    user, temp = service.create_user("admin-1", "ada", "Ada", {Role.CANDIDATE})
    service.set_roles("admin-1", user.user_id, {Role.CANDIDATE, Role.EXAMINER})
    service.set_active("admin-1", user.user_id, False)
    service.set_active("admin-1", user.user_id, True)
    new = service.reset_password("admin-1", user.user_id)
    service.change_own_password(user.user_id, new, "a-long-enough-one", "token")
    actions = [e.action for e in repo.audit]
    assert actions == [AuditAction.USER_CREATED, AuditAction.ROLES_CHANGED, AuditAction.DEACTIVATED,
                       AuditAction.REACTIVATED, AuditAction.PASSWORD_RESET, AuditAction.PASSWORD_CHANGED]
    assert repo.audit[1].detail == {"roles_before": ["CANDIDATE"], "roles_after": ["CANDIDATE", "EXAMINER"]}
    assert repo.audit[0].actor_user_id == "admin-1" and repo.audit[5].actor_user_id == user.user_id
    text = repr(repo.audit)
    for secret in (temp, new, "a-long-enough-one", "pbkdf2"):
        assert secret not in text


def test_refused_change_writes_no_audit_record():
    service, repo, _ = accounts_with_admin()
    with pytest.raises(UserConflictError):
        service.set_active("admin-1", "admin-1", False)
    assert repo.audit == []


def test_lock_is_audited_only_for_real_accounts():
    service, repo, _ = accounts_with_admin()
    service.record_login_lock("not-a-user-maybe-a-password", "10.0.0.1")
    assert repo.audit == []
    service.record_login_lock("root", "10.0.0.1")
    assert repo.audit[0].action is AuditAction.LOGIN_LOCKED and repo.audit[0].actor_user_id is None


def test_reset_lifts_the_lock_and_clearing_is_audited():
    service, repo, guard = accounts_with_admin()
    fail(guard, user="root", times=USER_FAILURE_LIMIT)
    assert service.clear_login_lock("admin-1", "admin-1") == 1
    assert repo.audit[-1].action is AuditAction.LOGIN_LOCK_CLEARED
    fail(guard, user="root", times=USER_FAILURE_LIMIT)
    service.reset_password("admin-1", "admin-1")
    guard.begin("root", "10.0.0.1")


# ---- SQL contract ----

def test_attempt_count_is_one_atomic_upsert_reading_old_values_first():
    database = FakeDatabase(fetch_results=[(3,)])
    position = MySQLLoginThrottleRepository(database).reserve("k", "s", 5, T0, T0 - timedelta(minutes=15), T0 + timedelta(minutes=15))
    assert position == 3
    sql = database.statements[0][0]
    assert sql.index("locked_until = IF") < sql.index("failed_count = IF") < sql.index("window_started_at = IF")


def test_audit_row_is_written_on_the_changes_own_connection():
    database = FakeDatabase()
    service = UserAdminService(MySQLUserRepository(database))
    event = service._event(AuditAction.PASSWORD_RESET, "a", "u", "name")
    MySQLUserRepository(database).set_password("u", "hash", must_change_password=True, audit=event)
    sqls = [sql for sql, _ in database.statements]
    assert sqls[0].startswith("UPDATE users SET password_hash") and sqls[1].startswith("INSERT INTO account_audit_events")
