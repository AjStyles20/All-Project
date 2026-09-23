-- P001 FD-02: examination and programming-question management.

CREATE TABLE IF NOT EXISTS examinations (
    examination_id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    owner_user_id VARCHAR(64) NOT NULL,
    status ENUM('DRAFT','SCHEDULED','ACTIVE','CLOSED','ARCHIVED') NOT NULL DEFAULT 'DRAFT',
    starts_at DATETIME(6) NULL,
    ends_at DATETIME(6) NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_examinations_owner (owner_user_id),
    INDEX idx_examinations_status (status),
    CONSTRAINT fk_examinations_owner FOREIGN KEY (owner_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS questions (
    question_id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    prompt TEXT NOT NULL,
    language VARCHAR(50) NOT NULL,
    max_score INT NOT NULL,
    version INT NOT NULL DEFAULT 1,
    created_by_user_id VARCHAR(64) NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    CONSTRAINT chk_questions_max_score CHECK (max_score > 0),
    CONSTRAINT chk_questions_version CHECK (version > 0),
    INDEX idx_questions_creator (created_by_user_id),
    CONSTRAINT fk_questions_creator FOREIGN KEY (created_by_user_id)
        REFERENCES users(user_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS examination_questions (
    examination_id VARCHAR(64) NOT NULL,
    question_id VARCHAR(64) NOT NULL,
    display_order INT NOT NULL,
    score_weight INT NOT NULL,
    PRIMARY KEY (examination_id, question_id),
    UNIQUE KEY uq_exam_display_order (examination_id, display_order),
    CONSTRAINT chk_exam_question_order CHECK (display_order > 0),
    CONSTRAINT chk_exam_question_weight CHECK (score_weight > 0),
    CONSTRAINT fk_exam_questions_exam FOREIGN KEY (examination_id)
        REFERENCES examinations(examination_id) ON DELETE CASCADE,
    CONSTRAINT fk_exam_questions_question FOREIGN KEY (question_id)
        REFERENCES questions(question_id)
) ENGINE=InnoDB;
