"""Numbers for the teacher dashboard: risk counts and recent predictions."""
from backend import config
from backend.db.connection import get_db
from backend.repositories import prediction_repository


def get_dashboard_stats():
    db = get_db()
    try:
        rows = prediction_repository.latest_per_student(db)

        total = len(rows)
        high = sum(1 for r in rows if r["risk"] == "High")
        moderate = sum(1 for r in rows if r["risk"] == "Moderate")
        low = sum(1 for r in rows if r["risk"] == "Low")

        recent_rows = prediction_repository.recent(db, config.RECENT_LIMIT)

        recent = [{"id": r["id"], "name": r["name"], "score": round(r["score"], 1),
                   "risk": r["risk"], "date": r["date"]} for r in recent_rows]

        return {"total": total, "high": high, "moderate": moderate,
                "low": low, "recent": recent}
    finally:
        db.close()
