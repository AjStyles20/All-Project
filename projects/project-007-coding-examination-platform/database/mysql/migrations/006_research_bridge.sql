-- P001 FD-06: operational -> EGPCV evidence bridge (ECC v1.0 §6, DR-013 Q3/Q4, DR-015).

-- Administrator-created link from an examination question to a research case template
-- and claims. Nothing is bridged without one (DR-013 Q4). The ethics reference is the
-- first consent gate (DR-015 (1)).
CREATE TABLE IF NOT EXISTS research_links (
    link_id VARCHAR(64) PRIMARY KEY,
    examination_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    template_case_id VARCHAR(128) NOT NULL,
    claim_ids JSON NOT NULL,
    ethics_reference VARCHAR(200) NOT NULL,
    created_by_user_id VARCHAR(64) NOT NULL,
    created_at DATETIME(6) NOT NULL,
    UNIQUE KEY uq_link_exam_question (examination_id, question_id),
    CONSTRAINT fk_links_exam FOREIGN KEY (examination_id) REFERENCES examinations(examination_id),
    CONSTRAINT fk_links_question FOREIGN KEY (question_id) REFERENCES questions(question_id),
    CONSTRAINT fk_links_creator FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;

-- Append-only consent log; the latest event per (examination, candidate) is current.
-- Second consent gate: explicit candidate opt-in (DR-015 (1)).
CREATE TABLE IF NOT EXISTS research_consent_events (
    event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    examination_id VARCHAR(64) NOT NULL,
    candidate_user_id VARCHAR(64) NOT NULL,
    status ENUM('OPTED_IN','WITHDRAWN') NOT NULL,
    recorded_at DATETIME(6) NOT NULL,
    INDEX idx_consent_latest (examination_id, candidate_user_id, event_id),
    CONSTRAINT fk_consent_exam FOREIGN KEY (examination_id) REFERENCES examinations(examination_id),
    CONSTRAINT fk_consent_candidate FOREIGN KEY (candidate_user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;

-- The only place a research code can be traced back to a person (DR-015 (2)).
-- Exposed through administrator-only endpoints; the research store never sees user ids.
CREATE TABLE IF NOT EXISTS research_identities (
    examination_id VARCHAR(64) NOT NULL,
    candidate_user_id VARCHAR(64) NOT NULL,
    research_code VARCHAR(32) NOT NULL,
    created_at DATETIME(6) NOT NULL,
    PRIMARY KEY (examination_id, candidate_user_id),
    UNIQUE KEY uq_research_code (research_code),
    CONSTRAINT fk_identity_exam FOREIGN KEY (examination_id) REFERENCES examinations(examination_id),
    CONSTRAINT fk_identity_candidate FOREIGN KEY (candidate_user_id) REFERENCES users(user_id)
) ENGINE=InnoDB;

-- One record per (session, linked question): provenance and idempotency of the bridge.
CREATE TABLE IF NOT EXISTS research_bridge_records (
    session_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    link_id VARCHAR(64) NOT NULL,
    outcome ENUM('BRIDGED','NO_RESPONSE','NO_CONTRACT') NOT NULL,
    research_case_id VARCHAR(200) NULL,
    response_revision INT NULL,
    policy_version VARCHAR(200) NULL,
    bridged_at DATETIME(6) NOT NULL,
    PRIMARY KEY (session_id, question_id),
    CONSTRAINT fk_bridge_session FOREIGN KEY (session_id) REFERENCES examination_sessions(session_id),
    CONSTRAINT fk_bridge_link FOREIGN KEY (link_id) REFERENCES research_links(link_id)
) ENGINE=InnoDB;

-- Withdrawal deletions (DR-016 (1)). Holds only the pseudonymous code and counts:
-- the code -> person link is deleted at the same time, so this log cannot re-identify.
CREATE TABLE IF NOT EXISTS research_withdrawal_log (
    event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    examination_id VARCHAR(64) NOT NULL,
    research_code VARCHAR(32) NULL,
    cases_deleted INT NOT NULL,
    cases_retained_as_shell INT NOT NULL,
    completed_at DATETIME(6) NOT NULL,
    INDEX idx_withdrawal_exam (examination_id),
    CONSTRAINT fk_withdrawal_exam FOREIGN KEY (examination_id) REFERENCES examinations(examination_id)
) ENGINE=InnoDB;
