-- P001 FD-05: Examination Capability Contracts (ECC v1.0, DR-013).

-- Every version of an examination's contract. A version is editable only while
-- DRAFT; BOUND and SUPERSEDED rows are never rewritten (non-retroactive, spec §5).
CREATE TABLE IF NOT EXISTS capability_contracts (
    examination_id VARCHAR(64) NOT NULL,
    version INT NOT NULL,
    status ENUM('DRAFT','BOUND','SUPERSEDED') NOT NULL,
    document JSON NOT NULL,
    content_hash CHAR(71) NOT NULL,
    bound_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    PRIMARY KEY (examination_id, version),
    INDEX idx_contracts_status (examination_id, status),
    CONSTRAINT chk_contracts_version CHECK (version > 0),
    CONSTRAINT fk_contracts_exam FOREIGN KEY (examination_id)
        REFERENCES examinations(examination_id)
) ENGINE=InnoDB;

-- Per-candidate authorized exceptions (spec §4.5). Reason is a category only (NFR-10).
CREATE TABLE IF NOT EXISTS contract_exceptions (
    exception_id VARCHAR(64) PRIMARY KEY,
    examination_id VARCHAR(64) NOT NULL,
    contract_version INT NOT NULL,
    candidate_user_id VARCHAR(64) NOT NULL,
    capability_overrides JSON NOT NULL,
    extra_time_minutes INT NOT NULL DEFAULT 0,
    reason_category ENUM('ACCESSIBILITY','TECHNICAL','OTHER_APPROVED') NOT NULL,
    approved_by_user_id VARCHAR(64) NOT NULL,
    approved_at DATETIME(6) NOT NULL,
    INDEX idx_exceptions_candidate (examination_id, candidate_user_id),
    CONSTRAINT chk_exceptions_time CHECK (extra_time_minutes BETWEEN 0 AND 1440),
    CONSTRAINT fk_exceptions_contract FOREIGN KEY (examination_id, contract_version)
        REFERENCES capability_contracts(examination_id, version),
    CONSTRAINT fk_exceptions_candidate FOREIGN KEY (candidate_user_id)
        REFERENCES users(user_id),
    CONSTRAINT fk_exceptions_approver FOREIGN KEY (approved_by_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;
