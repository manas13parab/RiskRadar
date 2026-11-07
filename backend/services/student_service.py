"""The student list shown to teachers."""
from backend.db.connection import get_db
from backend.repositories import student_repository


def get_students():
    db = get_db()
    try:
        rows = student_repository.list_with_latest_prediction(db)
        return [{"id": r["id"], "name": r["name"], "department": r["department"],
                 "score": round(r["score"], 1) if r["score"] else 0,
                 "risk": r["risk"] or "N/A"} for r in rows]
    finally:
        db.close()
