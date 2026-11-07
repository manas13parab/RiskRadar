"""Creates the tables (teachers, students, predictions) if they do not exist yet."""
from backend.db.connection import get_db


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS teachers (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            email       TEXT,
            department  TEXT,
            gender      TEXT,
            age         INTEGER,
            password_hash TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  TEXT NOT NULL,
            score       REAL NOT NULL,
            risk        TEXT NOT NULL,
            factors     TEXT DEFAULT '[]',
            tips        TEXT DEFAULT '[]',
            date        TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        CREATE INDEX IF NOT EXISTS idx_pred_student ON predictions(student_id);
    """)
    conn.commit()
    conn.close()
