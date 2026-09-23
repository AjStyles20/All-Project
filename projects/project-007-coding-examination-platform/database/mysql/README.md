# Local MySQL / MySQL Workbench Setup — P001

## Purpose
This guide connects the full P001 platform to a local MySQL Server administered with MySQL Workbench. MySQL Workbench is the client; MySQL Server is the DBMS. Never commit a real database password.

## Step 1 — Create the database and least-privilege application account
Open MySQL Workbench, connect using a MySQL administrative account, then open:
`database/mysql/bootstrap/000_create_database_and_user.sql`.

Before running it, replace only `CHANGE_ME_LOCAL_PASSWORD` with a strong local password. The script creates `p001_coding_exam`, creates `p001_app@localhost`, and grants only SELECT/INSERT/UPDATE/DELETE on that schema.

**Reason:** the web application should not normally have permission to CREATE, ALTER or DROP tables. Schema changes are an explicit migration/administrator responsibility.

## Step 2 — Apply migration 001
In Workbench select the `p001_coding_exam` schema and execute:
`database/mysql/migrations/001_identity_rbac.sql`.

It creates `users`, `user_roles` and `auth_sessions` with foreign keys and indexes.

## Step 3 — Configure the application locally
In PowerShell for the current terminal session:

```powershell
$env:P001_DB_HOST="127.0.0.1"
$env:P001_DB_PORT="3306"
$env:P001_DB_NAME="p001_coding_exam"
$env:P001_DB_USER="p001_app"
$env:P001_DB_PASSWORD="<your local password>"
```

Do not put the real password in Git.

## Step 4 — Install dependencies and verify the schema
From `projects/project-007-coding-examination-platform`:

```powershell
python -m pip install -r requirements.txt
python scripts/check_mysql_connection.py
```

Expected final line:
`P001 MySQL FD-01 schema check: PASS`.

## Step 5 — Run the live integration test
The live test is deliberately opt-in:

```powershell
$env:P001_RUN_MYSQL_TESTS="1"
python -m pytest tests/integration/test_mysql_identity_live.py -q
```

This creates a uniquely named temporary-style candidate account, logs in, verifies the principal/role, revokes the session and verifies the token is no longer accepted.

## Verification meaning
Workbench successfully creating tables proves the physical schema. The connection-check script proves Python can reach the intended schema. The opt-in integration test proves the identity repository and authentication service operate against a real MySQL Server. These are separate claims and are recorded separately.
