"""A student's past predictions and their latest one."""
from backend.db.connection import get_db
from backend.repositories import prediction_repository


def get_history(student_id):
    db = get_db()
    try:
        rows = prediction_repository.history_of(db, student_id)
        return [{"date": r["date"], "score": round(r["score"], 1),
                 "risk": r["risk"]} for r in rows]
    finally:
        db.close()


def get_latest(student_id):
    db = get_db()
    try:
        row = prediction_repository.latest_of(db, student_id)
        if row:
            return {"date": row["date"], "score": round(row["score"], 1),
                    "risk": row["risk"]}
        return None
    finally:
        db.close()
