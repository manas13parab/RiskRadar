"""SQL for the teachers table."""


def get_by_id(db, teacher_id):
    return db.execute("SELECT id, name, password_hash FROM teachers WHERE id = ?",
                      (teacher_id,)).fetchone()


def insert(db, teacher_id, name, password_hash):
    db.execute("INSERT INTO teachers (id, name, password_hash) VALUES (?, ?, ?)",
               (teacher_id, name, password_hash))
