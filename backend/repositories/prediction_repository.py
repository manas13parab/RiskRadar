"""SQL for the predictions table."""


def insert(db, student_id, score, risk, date, factors="[]", tips="[]"):
    db.execute(
        "INSERT INTO predictions (student_id, score, risk, factors, tips, date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (student_id, score, risk, factors, tips, date))


def latest_per_student(db):
    """The newest prediction of every student (used for the dashboard numbers)."""
    return db.execute("""
            SELECT p.student_id, p.score, p.risk
            FROM predictions p
            WHERE p.id = (SELECT MAX(p2.id) FROM predictions p2
                          WHERE p2.student_id = p.student_id)
        """).fetchall()


def recent(db, limit):
    return db.execute("""
            SELECT p.student_id AS id, s.name, p.score, p.risk, p.date
            FROM predictions p
            JOIN students s ON s.id = p.student_id
            ORDER BY p.id DESC
            LIMIT ?
        """, (limit,)).fetchall()


def history_of(db, student_id):
    return db.execute(
        "SELECT score, risk, date FROM predictions WHERE student_id = ? ORDER BY id",
        (student_id,)).fetchall()


def latest_of(db, student_id):
    return db.execute(
        "SELECT score, risk, date FROM predictions WHERE student_id = ? ORDER BY id DESC LIMIT 1",
        (student_id,)).fetchone()
