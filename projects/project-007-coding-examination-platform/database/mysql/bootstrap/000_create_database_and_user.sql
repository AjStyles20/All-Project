-- P001 local-development bootstrap.
-- Run this as a MySQL administrative account in MySQL Workbench.
-- Replace CHANGE_ME_LOCAL_PASSWORD before execution. Do not commit a real password.

CREATE DATABASE IF NOT EXISTS p001_coding_exam
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'p001_app'@'localhost'
  IDENTIFIED BY 'CHANGE_ME_LOCAL_PASSWORD';

GRANT SELECT, INSERT, UPDATE, DELETE
  ON p001_coding_exam.*
  TO 'p001_app'@'localhost';

FLUSH PRIVILEGES;

-- Schema migrations are intentionally run separately.
-- The application account is not granted CREATE/ALTER/DROP in normal operation.
