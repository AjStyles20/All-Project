# Local MySQL / MySQL Workbench Setup — P001

## Purpose
This guide connects the full P001 platform to a local MySQL Server administered with MySQL Workbench. Do not commit passwords.

## Development database
Recommended schema name: `p001_coding_exam`.

In MySQL Workbench, connect to the local MySQL Server and execute:

```sql
CREATE DATABASE IF NOT EXISTS p001_coding_exam
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Then select that schema and run the versioned migration scripts under `database/mysql/migrations/` in numeric order.

## Application configuration
The application will read its MySQL connection details from environment variables/configuration rather than source-code credentials. A later persistence increment will add the MySQL driver/adapter and executable application bootstrap.

## Why this order
We first freeze the schema decision and versioned migration, then implement the adapter against that contract. This prevents the database design, ERD and Python repository from drifting independently.

## Verification
A successful Workbench execution of a migration proves schema creation only. Application integration is verified separately by MySQL-backed integration tests.
