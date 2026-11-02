# FD-07 — User Management Design

## Purpose
Before FD-07, accounts could only be created by code, so the platform could not be used by real people. FD-07 adds the first administrator, account administration, and password handling. Baseline requirement: FR-02 (user/account administration).

## First administrator
`python -m scripts.create_admin --username <name> --display-name "<full name>"` creates the first administrator. There is deliberately **no web page or API for this**: an unauthenticated "first admin" endpoint could be claimed by whoever reached the server first. Anyone able to run the script already holds the database credentials. The password is read without echo and stored only as a hash.

## One-time passwords
An administrator never chooses or knows a user's lasting password.
- Creating a user or resetting a password generates a random one-time password (`secrets.token_urlsafe(15)`), returned **once** with `Cache-Control: no-store`. Only its hash is stored.
- `users.must_change_password` is then set. **The server enforces it:** until the password is changed, every endpoint except `/auth/me`, `/auth/password` and `/auth/logout` answers `403 PASSWORD_CHANGE_REQUIRED`. The UI's forced screen is only a convenience on top.
- New passwords need 12 to 128 characters and must not contain the username. They must also differ from the current one when changing it.

## Sessions

| Event | Effect on sessions |
|---|---|
| User changes own password | Other devices signed out; this one stays |
| Administrator resets password | All signed out |
| Administrator deactivates account | All signed out; access stops on the next request |
| Administrator reactivates account | Old sessions stay dead |
| Administrator changes roles | Take effect on the next request |

## Avoiding lockout
- Administrators cannot deactivate themselves or remove their own administrator role.
- **The last active administrator** cannot be deactivated or demoted. The check runs inside the update's transaction with `SELECT … FOR UPDATE`, so two administrators demoting each other at the same moment queue instead of both succeeding.

## Least exposure
- `GET /examiner/candidates` returns only id, username and display name, for active candidates.
- `GET /admin/users` never includes password material.
- `GET /admin/examinations` returns id, title and status only.

## API

| Method | Path | Role |
|---|---|---|
| POST | `/auth/password` | any signed-in user |
| GET, POST | `/admin/users` | Administrator |
| PATCH | `/admin/users/{id}/active` | Administrator |
| PUT | `/admin/users/{id}/roles` | Administrator |
| POST | `/admin/users/{id}/password-reset` | Administrator |
| GET | `/admin/examinations` | Administrator |
| GET | `/examiner/candidates` | Examiner, Administrator |

## Known limitations
These matter under PROJECT_RULES §22 and should be resolved **before any public or real-student deployment**:
1. **No login rate limit or lockout.** Passwords can be guessed repeatedly, limited only by the slow hash.
2. **Username enumeration by timing.** A login for an unknown username returns faster, because it skips password hashing.
3. **One-time passwords are handed over by the administrator**; the platform sends no email.
4. **No bulk import.** Long cohorts must be created one at a time, and the candidate list is a plain dropdown.
5. **No audit trail** of who changed which account.

## Verification
- Service, API and SQL-contract tests; a test of the first-admin script.
- Live: `tests/integration/test_mysql_fd07_live.py` and the full suite passed on a disposable MySQL 8.4.9 (TE-017).
- Browser: first sign-in, forced change, reset, deactivation, candidate list and exam list (TE-017).

This is the implementing agent's own testing, not independent verification or a security review.
