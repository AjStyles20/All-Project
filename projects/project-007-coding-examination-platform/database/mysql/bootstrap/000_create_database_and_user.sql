-- P001 local-development bootstrap.
-- Run this as a MySQL administrative account in MySQL Workbench.
-- Replace CHANGE_ME_LOCAL_PASSWORD before execution. Do not commit a real password.
-- The application defaults to TCP host 127.0.0.1, so the least-privilege
-- application account is created for that host explicitly.

CREATE DATABASE IF NOT EXISTS p001_coding_exam
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'p001_app'@'127.0.0.1'
  IDENTIFIED BY 'CHANGE_ME_LOCAL_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE
  ON p001_coding_exam.*
  TO 'p001_app'@'127.0.0.1';

FLUSH PRIVILEGES;

-- Schema migrations are intentionally run separately using an administrative
-- or migration account. The normal application account is not granted
-- CREATE/ALTER/DROP privileges.
