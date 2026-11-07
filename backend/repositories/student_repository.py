"""SQL for the students table."""


def get_by_id(db, student_id):
    return db.execute("SELECT id, name, password_hash FROM students WHERE id = ?",
                      (student_id,)).fetchone()


def count(db):
    return db.execute("SELECT COUNT(*) FROM students").fetchone()[0]


def insert(db, student_id, name, email, department, gender, age, password_hash):
    db.execute(
        "INSERT INTO students (id, name, email, department, gender, age, password_hash) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (student_id, name, email, department, gender, age, password_hash))


def list_with_latest_prediction(db):
    """Every student with the score and risk of their latest prediction."""
    return db.execute("""
            SELECT s.id, s.name, s.department, p.score, p.risk
            FROM students s
            LEFT JOIN predictions p ON p.student_id = s.id
                AND p.id = (SELECT MAX(p2.id) FROM predictions p2
                            WHERE p2.student_id = s.id)
            ORDER BY s.id
        """).fetchall()
