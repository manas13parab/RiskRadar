"""Login check for teachers and students."""
from backend.db.connection import get_db
from backend.repositories import student_repository, teacher_repository
from backend.security import verify_password


def check_login(user_id, password, role):
    db = get_db()
    try:
        if role == "teacher":
            row = teacher_repository.get_by_id(db, user_id)
        else:
            row = student_repository.get_by_id(db, user_id)
        if row and verify_password(row["password_hash"], password):
            return {"id": row["id"], "name": row["name"], "role": role}
        return None
    finally:
        db.close()
