-- Progress database schema for the business-degree project.
-- Apply with: uv run scripts/init_db.py   (which runs this file)

PRAGMA foreign_keys = ON;

-- One row per lesson that has been generated.
CREATE TABLE IF NOT EXISTS lessons (
    address     TEXT PRIMARY KEY,          -- e.g. "203.4"
    title       TEXT NOT NULL,
    file        TEXT NOT NULL,             -- path to the HTML artifact
    year        INTEGER,                   -- parsed from address
    course_slot TEXT,                      -- parsed from address (e.g. "03")
    topic       INTEGER,                   -- parsed from address
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One row per quiz submission.
CREATE TABLE IF NOT EXISTS attempts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    address     TEXT NOT NULL REFERENCES lessons(address) ON DELETE CASCADE,
    ts          TEXT NOT NULL DEFAULT (datetime('now')),
    correct     INTEGER NOT NULL,
    total       INTEGER NOT NULL,
    score_pct   REAL NOT NULL
);

-- One row per question within an attempt — enables per-topic mastery.
CREATE TABLE IF NOT EXISTS question_results (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id  INTEGER NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
    address     TEXT NOT NULL,
    qid         TEXT NOT NULL,
    topic       TEXT,                      -- topic tag from answer key
    given       TEXT,
    is_correct  INTEGER NOT NULL           -- 0/1
);

-- Convenience view: latest score per lesson.
CREATE VIEW IF NOT EXISTS latest_scores AS
SELECT a.address, l.title, a.score_pct, a.correct, a.total, a.ts
FROM attempts a
JOIN lessons l ON l.address = a.address
WHERE a.id IN (
    SELECT MAX(id) FROM attempts GROUP BY address
);

-- Convenience view: mastery per topic tag across all attempts.
CREATE VIEW IF NOT EXISTS topic_mastery AS
SELECT topic,
       COUNT(*)                       AS questions_seen,
       SUM(is_correct)                AS questions_correct,
       ROUND(100.0 * SUM(is_correct) / COUNT(*), 1) AS pct
FROM question_results
WHERE topic IS NOT NULL
GROUP BY topic;
