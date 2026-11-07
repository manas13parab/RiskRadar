"""Runs the ML prediction and (when a student is chosen) saves it to their history."""
import json

from backend.db.connection import get_db
from backend.repositories import prediction_repository
from backend.utils import today_str
from ml.predictor import run_prediction


def predict(features, student_id=None):
    result = run_prediction(features)

    if student_id:
        db = get_db()
        try:
            prediction_repository.insert(
                db, student_id, result["score"], result["risk"], today_str(),
                json.dumps(result["factors"]), json.dumps(result["tips"]))
            db.commit()
        finally:
            db.close()

    return result
