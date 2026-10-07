CREATE DATABASE IF NOT EXISTS pathfinder CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pathfinder;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    class_level VARCHAR(20) DEFAULT '10',
    role ENUM('student','admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS streams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS careers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stream_id INT NULL,
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(140) NOT NULL UNIQUE,
    short_description VARCHAR(500),
    subjects TEXT,
    skills TEXT,
    icon VARCHAR(10) DEFAULT '◎',
    featured TINYINT(1) DEFAULT 0,
    FOREIGN KEY(stream_id) REFERENCES streams(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS exams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    full_name VARCHAR(255),
    exam_date DATE NULL,
    description TEXT,
    website VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS career_exams (
    career_id INT NOT NULL,
    exam_id INT NOT NULL,
    PRIMARY KEY(career_id, exam_id),
    FOREIGN KEY(career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY(exam_id) REFERENCES exams(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS colleges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NOT NULL,
    name VARCHAR(180) NOT NULL,
    location VARCHAR(120),
    FOREIGN KEY(career_id) REFERENCES careers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quiz_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    active TINYINT(1) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS quiz_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text VARCHAR(500) NOT NULL,
    FOREIGN KEY(question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS option_career_weights (
    option_id INT NOT NULL,
    career_id INT NOT NULL,
    weight DECIMAL(6,2) NOT NULL DEFAULT 1,
    PRIMARY KEY(option_id, career_id),
    FOREIGN KEY(option_id) REFERENCES quiz_options(id) ON DELETE CASCADE,
    FOREIGN KEY(career_id) REFERENCES careers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quiz_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attempt_id INT NOT NULL,
    question_id INT NOT NULL,
    option_id INT NOT NULL,
    FOREIGN KEY(attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    FOREIGN KEY(question_id) REFERENCES quiz_questions(id) ON DELETE CASCADE,
    FOREIGN KEY(option_id) REFERENCES quiz_options(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attempt_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attempt_id INT NOT NULL,
    career_id INT NOT NULL,
    score DECIMAL(8,2) NOT NULL,
    match_percent DECIMAL(5,2) NOT NULL,
    FOREIGN KEY(attempt_id) REFERENCES quiz_attempts(id) ON DELETE CASCADE,
    FOREIGN KEY(career_id) REFERENCES careers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS competitions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(180) NOT NULL,
    type VARCHAR(80) DEFAULT 'Olympiad',
    class_level VARCHAR(40) DEFAULT 'All',
    interest VARCHAR(80) DEFAULT 'All',
    deadline DATE NULL,
    description TEXT,
    website VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS bookmarks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_id INT NULL,
    competition_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_career_bookmark(user_id,career_id),
    UNIQUE KEY unique_comp_bookmark(user_id,competition_id),
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(career_id) REFERENCES careers(id) ON DELETE CASCADE,
    FOREIGN KEY(competition_id) REFERENCES competitions(id) ON DELETE CASCADE
);
