-- P001 FD-07: user management. Run once (MySQL has no ADD COLUMN IF NOT EXISTS).

-- Set when an administrator issues a one-time password; the API then allows nothing
-- except changing it until the user has chosen their own.
ALTER TABLE users ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT FALSE;
