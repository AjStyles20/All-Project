-- P001 FD-03: candidate assignment, examination sessions and saved responses.

CREATE TABLE IF NOT EXISTS candidate_assignments (
    assignment_id VARCHAR(64) PRIMARY KEY,
    examination_id VARCHAR(64) NOT NULL,
    candidate_user_id VARCHAR(64) NOT NULL,
    assigned_by_user_id VARCHAR(64) NOT NULL,
    assigned_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    UNIQUE KEY uq_assignment_exam_candidate (examination_id, candidate_user_id),
    INDEX idx_assignments_candidate (candidate_user_id),
    CONSTRAINT fk_assignments_exam FOREIGN KEY (examination_id)
        REFERENCES examinations(examination_id),
    CONSTRAINT fk_assignments_candidate FOREIGN KEY (candidate_user_id)
        REFERENCES users(user_id),
    CONSTRAINT fk_assignments_assigner FOREIGN KEY (assigned_by_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;

-- One session per assignment in FD-03: a repeated start resumes it instead of
-- creating a duplicate attempt (NFR-06). Multiple attempts would relax this key.
CREATE TABLE IF NOT EXISTS examination_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    assignment_id VARCHAR(64) NOT NULL,
    status ENUM('IN_PROGRESS','SUBMITTED') NOT NULL DEFAULT 'IN_PROGRESS',
    started_at DATETIME(6) NOT NULL,
    submitted_at DATETIME(6) NULL,
    UNIQUE KEY uq_session_assignment (assignment_id),
    CONSTRAINT fk_sessions_assignment FOREIGN KEY (assignment_id)
        REFERENCES candidate_assignments(assignment_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS submission_responses (
    session_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    content MEDIUMTEXT NOT NULL,
    revision INT NOT NULL,
    saved_at DATETIME(6) NOT NULL,
    PRIMARY KEY (session_id, question_id),
    CONSTRAINT chk_responses_revision CHECK (revision > 0),
    CONSTRAINT fk_responses_session FOREIGN KEY (session_id)
        REFERENCES examination_sessions(session_id),
    CONSTRAINT fk_responses_question FOREIGN KEY (question_id)
        REFERENCES questions(question_id)
) ENGINE=InnoDB;
