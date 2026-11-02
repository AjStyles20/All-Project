-- P001 FD-08: login throttling and account audit trail.

-- Failed-login counters. Keys are SHA-256 digests of (username, IP) or (IP), never the raw
-- text: people sometimes type their password into the username box.
CREATE TABLE IF NOT EXISTS login_throttle (
    scope_key CHAR(64) PRIMARY KEY,
    -- Digest of the username alone, so an administrator can clear a lock from any IP.
    subject_key CHAR(64) NULL,
    failed_count INT NOT NULL,
    window_started_at DATETIME(6) NOT NULL,
    locked_until DATETIME(6) NULL,
    INDEX idx_login_throttle_window (window_started_at),
    INDEX idx_login_throttle_subject (subject_key)
) ENGINE=InnoDB;

-- Append-only record of account changes, written in the same transaction as the change.
-- Never holds passwords or hashes. actor_user_id is NULL for the first-admin script and
-- for automatic events. No foreign keys: the record must outlive whatever it describes.
CREATE TABLE IF NOT EXISTS account_audit_events (
    event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    occurred_at DATETIME(6) NOT NULL,
    action VARCHAR(40) NOT NULL,
    actor_user_id VARCHAR(64) NULL,
    target_user_id VARCHAR(64) NOT NULL,
    target_username VARCHAR(100) NOT NULL,
    detail JSON NOT NULL,
    INDEX idx_audit_target (target_user_id, event_id)
) ENGINE=InnoDB;
