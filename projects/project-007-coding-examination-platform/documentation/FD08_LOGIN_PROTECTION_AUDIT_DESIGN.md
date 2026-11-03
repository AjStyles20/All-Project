# FD-08 — Login protection and account audit trail

Closes three of the gaps listed in `FD07_USER_MANAGEMENT_DESIGN.md`: no login rate limit, username enumeration by timing, and no account audit trail. Policy choices are recorded in DR-020 for AJ's review.

## Login throttling

| Limit | Value | Keyed on |
|---|---|---|
| Per account and address | 5 failed attempts in 15 minutes, then locked for 15 minutes | username + client IP |
| Per address | 100 failed attempts in 15 minutes | client IP |

Why keyed on the pair: on an exam platform a lockout can be used as a weapon. If the lock followed the username alone, anyone could lock a classmate out just as an exam opens. Keyed on the pair, an attacker elsewhere locks only their own address. The per-address cap is high because a whole lab can share one IP and people mistype at the start of an exam; it exists to stop one address trying many usernames.

- **A lock never ends an existing session.** A student already in an exam keeps working.
- **Administrators can clear a lock** (`POST /admin/users/{id}/clear-login-lock`, "Clear sign-in lock" on the Users screen). It clears the account's locks from every address. A password reset also clears them.
- **Unknown usernames are counted exactly like real ones**, so a lock reveals nothing about who exists.
- **The stored keys are SHA-256 digests**, because the username box sometimes receives a mistyped password.
- **The client IP is `request.client`.** `X-Forwarded-For` is ignored, because the client sets it and could dodge the limit. Behind a reverse proxy, configure uvicorn's `--proxy-headers` and `--forwarded-allow-ips` explicitly (`database/mysql/README.md`).
- A locked attempt returns **429** with `Retry-After`. The message does not say whether the password was right.

### Counting before hashing
Each attempt is counted **before** the password is checked: one atomic `INSERT … ON DUPLICATE KEY UPDATE` returns the attempt's position in the window, and attempts past the limit are refused. A correct password clears the pair's count and refunds the address count, so a lab signing in correctly never reaches the address limit.

The first version counted only after a wrong password. Browser testing showed that parallel requests all passed the lock check while earlier ones were still hashing, so a burst could make more than five guesses, and a correct password still worked after five failures (TE-018). Counting first closes that. Tests now use real threads, through the API and against MySQL.

The failure that reaches the limit, and only that one, writes a `LOGIN_LOCKED` audit record. An earlier check ("is it locked now?") made every attempt of a parallel burst report the same lock (TE-018).

## Timing
A login for an unknown or deactivated username now verifies the password against a fixed decoy hash, so it takes as long as a wrong password for a real account.

## Account audit trail
Table `account_audit_events` (migration 008). Each account change is written **in the same transaction** as the change, so a refused or failed change leaves no record.

| Action | Written by |
|---|---|
| `USER_CREATED` | Administrator, or the `create_admin` script (no actor) |
| `ROLES_CHANGED` | Administrator (roles before and after) |
| `DEACTIVATED`, `REACTIVATED` | Administrator |
| `PASSWORD_RESET` | Administrator |
| `PASSWORD_CHANGED` | The user |
| `LOGIN_LOCKED` | The system (existing accounts only) |
| `LOGIN_LOCK_CLEARED` | Administrator |

Passwords and hashes are never recorded. `GET /admin/audit` (Administrator) returns the newest events first and names the acting administrator. The UI shows it at "Audit trail".

## Known limitations
1. Limits are fixed in code (`app/services/login_guard.py`), not configurable.
2. Throttle state is in MySQL; there is no separate cache, so each attempt costs a few small writes.
3. The audit trail has no retention policy, export or search.
4. Not addressed: one-time passwords are still handed over by the administrator, and there is no bulk import (see FD-07).

## Verification
- Unit, API and SQL-contract tests, including parallel attempts with real threads.
- Live: `tests/integration/test_mysql_fd08_live.py` and the full suite on a disposable MySQL 8.4.9 (TE-018).
- Browser and API against the running app: lockout message, parallel burst, clearing a lock, audit screen (TE-018).

This is the implementing agent's own testing, not independent verification or a security review.
