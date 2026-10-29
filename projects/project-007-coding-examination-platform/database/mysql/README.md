# Local MySQL / MySQL Workbench Setup — P001

## Purpose
This guide connects the full P001 platform to a local MySQL Server administered with MySQL Workbench. MySQL Workbench is the client; MySQL Server is the DBMS. Never commit a real database password.

## Step 1 — Create the database and least-privilege application account
Open MySQL Workbench, connect using a MySQL administrative account, then open:
`database/mysql/bootstrap/000_create_database_and_user.sql`.

Before running it, replace only `CHANGE_ME_LOCAL_PASSWORD` with a strong local password. The script creates `p001_coding_exam`, creates `p001_app@127.0.0.1`, and grants only SELECT/INSERT/UPDATE/DELETE on that schema.

**Reason:** the web application should not normally have permission to CREATE, ALTER or DROP tables. Schema changes are an explicit migration/administrator responsibility.

## Step 2 — Apply migration 001
In Workbench select the `p001_coding_exam` schema and execute:
`database/mysql/migrations/001_identity_rbac.sql`.

It creates `users`, `user_roles` and `auth_sessions` with foreign keys and indexes.

## Step 3 — Apply migration 002
In Workbench, with `p001_coding_exam` selected, execute:
`database/mysql/migrations/002_examinations_questions.sql`.

It creates `examinations`, `questions` and `examination_questions`, including ownership foreign keys, lifecycle status, positive-score/order constraints and examination-question membership integrity.

## Step 3b — Apply migration 003
In Workbench, with `p001_coding_exam` selected, execute:
`database/mysql/migrations/003_candidate_sessions.sql`.

It creates `candidate_assignments`, `examination_sessions` and `submission_responses`. Each candidate can be assigned to an examination only once, each assignment gets one session, and each saved response carries a revision number.

## Step 3c — Apply migration 004
In Workbench, with `p001_coding_exam` selected, execute:
`database/mysql/migrations/004_response_marks.sql`.

It creates three tables:
- `response_marks`: the current mark per session and question, including which response revision was marked.
- `response_mark_history`: an append-only log of every mark saved.
- `examination_result_releases`: the release record. Candidates see marks only after it exists.

## Step 3d — Apply migration 005
In Workbench, with `p001_coding_exam` selected, execute:
`database/mysql/migrations/005_capability_contracts.sql`.

It creates `capability_contracts` (every version of each examination's Examination Capability Contract, stored as its canonical JSON document with a SHA-256 hash) and `contract_exceptions` (per-candidate authorized exceptions). From FD-05 onward, an examination cannot be scheduled without a contract.

## Step 4 — Configure the application locally
In PowerShell for the current terminal session:

```powershell
$env:P001_DB_HOST="127.0.0.1"
$env:P001_DB_PORT="3306"
$env:P001_DB_NAME="p001_coding_exam"
$env:P001_DB_USER="p001_app"
$env:P001_DB_PASSWORD="<your local password>"
```

Do not put the real password in Git.

## Step 5 — Install dependencies and verify the schema
From `projects/project-007-coding-examination-platform`:

```powershell
python -m pip install -r requirements.txt
python -m scripts.check_mysql_connection
```

Expected final line:
`P001 MySQL FD-05 schema check: PASS`.

## Step 6 — Run the live integration tests
The live test is deliberately opt-in:

```powershell
$env:P001_RUN_MYSQL_TESTS="1"
python -m pytest tests/integration/test_mysql_identity_live.py tests/integration/test_mysql_fd02_live.py tests/integration/test_mysql_fd03_live.py tests/integration/test_mysql_fd04_live.py tests/integration/test_mysql_fd05_live.py -q
```

This creates a uniquely named temporary-style candidate account, logs in, verifies the principal/role, revokes the session and verifies the token is no longer accepted.

## Verification meaning
Workbench successfully creating tables proves the physical schema. The connection-check script proves Python can reach the intended schema. The opt-in integration test proves the identity repository and authentication service operate against a real MySQL Server. These are separate claims and are recorded separately.
