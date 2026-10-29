-- P001 FD-04: examiner marks on submitted responses.

-- One current mark per (session, question). A question can be marked even when the
-- candidate left it unanswered, so the mark does not reference submission_responses.
CREATE TABLE IF NOT EXISTS response_marks (
    session_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    score INT NOT NULL,
    comment TEXT NOT NULL,
    -- Which saved revision the examiner read when marking (NULL = no response saved).
    response_revision INT NULL,
    marked_by_user_id VARCHAR(64) NOT NULL,
    marked_at DATETIME(6) NOT NULL,
    PRIMARY KEY (session_id, question_id),
    CONSTRAINT chk_marks_score CHECK (score >= 0),
    CONSTRAINT fk_marks_session FOREIGN KEY (session_id)
        REFERENCES examination_sessions(session_id),
    CONSTRAINT fk_marks_question FOREIGN KEY (question_id)
        REFERENCES questions(question_id),
    CONSTRAINT fk_marks_marker FOREIGN KEY (marked_by_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;

-- Append-only log of every mark ever saved, current or superseded (DR-012 (2)).
-- The application account only ever INSERTs here; nothing updates or deletes rows.
CREATE TABLE IF NOT EXISTS response_mark_history (
    history_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    score INT NOT NULL,
    comment TEXT NOT NULL,
    response_revision INT NULL,
    marked_by_user_id VARCHAR(64) NOT NULL,
    marked_at DATETIME(6) NOT NULL,
    INDEX idx_mark_history_item (session_id, question_id),
    CONSTRAINT fk_mark_history_session FOREIGN KEY (session_id)
        REFERENCES examination_sessions(session_id),
    CONSTRAINT fk_mark_history_question FOREIGN KEY (question_id)
        REFERENCES questions(question_id),
    CONSTRAINT fk_mark_history_marker FOREIGN KEY (marked_by_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;

-- Results release (DR-012 (3)): candidates see marks only after this row exists,
-- and its existence locks further marking for the examination.
CREATE TABLE IF NOT EXISTS examination_result_releases (
    examination_id VARCHAR(64) PRIMARY KEY,
    released_by_user_id VARCHAR(64) NOT NULL,
    released_at DATETIME(6) NOT NULL,
    CONSTRAINT fk_release_exam FOREIGN KEY (examination_id)
        REFERENCES examinations(examination_id),
    CONSTRAINT fk_release_user FOREIGN KEY (released_by_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;
