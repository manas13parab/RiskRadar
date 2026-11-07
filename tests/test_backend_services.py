import json

import mock
import services
import database
from backend import services as backend_services
from backend.db import get_db
from backend.services import (check_login, get_dashboard_stats, get_history, get_latest,
                              get_students, predict, validate_roster)
from conftest import STRONG, WEAK

SEVEN = ["check_login", "get_students", "get_dashboard_stats", "predict",
         "get_history", "get_latest", "validate_roster"]


def test_login_for_teacher_and_student(db):
    assert check_login("T01", "admin123", "teacher") == {"id": "T01", "name": "Dr. Sarah Mitchell", "role": "teacher"}
    assert check_login("S1000", "omar@1000", "student")["role"] == "student"


def test_wrong_password_unknown_user_and_wrong_role_are_rejected(db):
    assert check_login("T01", "wrong", "teacher") is None
    assert check_login("T99", "admin123", "teacher") is None
    assert check_login("T01", "admin123", "student") is None      # teacher id is not a student id
    assert check_login("S1000", "omar@1000", "teacher") is None


def test_students_list_has_everyone_with_score_and_risk(db):
    students = get_students()
    assert len(students) == 30
    assert set(students[0]) == {"id", "name", "department", "score", "risk"}
    assert all(s["risk"] in {"High", "Moderate", "Low"} for s in students)


def test_student_without_a_prediction_shows_na(db):
    conn = get_db()
    conn.execute("INSERT INTO students (id, name, password_hash) VALUES ('S9999', 'No Pred', 'x')")
    conn.commit()
    conn.close()
    new = next(s for s in get_students() if s["id"] == "S9999")
    assert new["risk"] == "N/A" and new["score"] == 0


def test_dashboard_counts_add_up(db):
    stats = get_dashboard_stats()
    assert stats["total"] == 30
    assert stats["high"] + stats["moderate"] + stats["low"] == 30
    assert len(stats["recent"]) == 5 and set(stats["recent"][0]) == {"id", "name", "score", "risk", "date"}


def test_predict_with_a_student_saves_to_history(db):
    before = len(get_history("S1000"))
    result = predict(STRONG, student_id="S1000")
    assert set(result) == {"score", "risk", "factors", "tips"}
    history = get_history("S1000")
    assert len(history) == before + 1
    assert history[-1]["score"] == result["score"] and history[-1]["risk"] == result["risk"]
    assert get_latest("S1000")["score"] == result["score"]


def test_saved_prediction_keeps_factors_and_tips_as_json(db):
    result = predict(WEAK, student_id="S1001")
    conn = get_db()
    row = conn.execute("SELECT factors, tips FROM predictions WHERE student_id='S1001' ORDER BY id DESC").fetchone()
    conn.close()
    assert json.loads(row["factors"]) == result["factors"]
    assert json.loads(row["tips"]) == result["tips"]


def test_predict_without_a_student_saves_nothing(db):
    predict(STRONG)
    predict(STRONG, student_id="")
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    conn.close()
    assert total == 30


def test_latest_and_history_for_unknown_student(db):
    assert get_latest("NOPE") is None
    assert get_history("NOPE") == []


def test_validate_roster():
    assert validate_roster(["student_id", "name", "department"]) == []
    errors = validate_roster(["student_id", "age"])
    assert any("Missing required columns: department, name" in e for e in errors)
    assert any("Unexpected columns: age" in e for e in errors)


def test_old_import_paths_still_work():
    for name in SEVEN:
        assert getattr(services, name) is getattr(backend_services, name)
        assert hasattr(mock, name)                      # mock.py has the same 7 functions
    assert hasattr(database, "get_db") and hasattr(database, "init_db") and hasattr(database, "seed_db")
