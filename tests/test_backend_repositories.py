import pytest

from backend.db import get_db
from backend.repositories import prediction_repository, student_repository, teacher_repository


@pytest.fixture
def conn(db):
    connection = get_db()
    yield connection
    connection.close()


def test_teacher_lookup(conn):
    row = teacher_repository.get_by_id(conn, "T01")
    assert row["name"] == "Dr. Sarah Mitchell"
    assert teacher_repository.get_by_id(conn, "T99") is None


def test_student_lookup_insert_and_count(conn):
    assert student_repository.get_by_id(conn, "S1000")["name"] == "Omar Williams"
    before = student_repository.count(conn)
    student_repository.insert(conn, "S9001", "New Student", "n@x.com", "Physics", "F", 20, "hash")
    assert student_repository.count(conn) == before + 1
    assert student_repository.get_by_id(conn, "S9001")["name"] == "New Student"


def test_student_list_shows_the_newest_prediction_and_all_students(conn):
    student_repository.insert(conn, "S9002", "No Prediction", "", "Physics", "M", 21, "hash")
    prediction_repository.insert(conn, "S1000", 91.5, "Low", "Oct 01, 2026")
    rows = {r["id"]: r for r in student_repository.list_with_latest_prediction(conn)}
    assert rows["S1000"]["score"] == 91.5
    assert rows["S9002"]["score"] is None and rows["S9002"]["risk"] is None
    assert len(rows) == 31


def test_prediction_insert_history_latest(conn):
    prediction_repository.insert(conn, "S1001", 50.0, "High", "Oct 01, 2026", '["f"]', '["t"]')
    prediction_repository.insert(conn, "S1001", 75.0, "Low", "Oct 02, 2026")
    history = prediction_repository.history_of(conn, "S1001")
    assert [r["score"] for r in history][-2:] == [50.0, 75.0]
    assert prediction_repository.latest_of(conn, "S1001")["score"] == 75.0
    assert prediction_repository.latest_of(conn, "NOPE") is None
    assert prediction_repository.history_of(conn, "NOPE") == []


def test_latest_per_student_and_recent(conn):
    prediction_repository.insert(conn, "S1002", 10.0, "High", "Oct 01, 2026")
    prediction_repository.insert(conn, "S1002", 99.0, "Low", "Oct 02, 2026")
    latest = {r["student_id"]: r for r in prediction_repository.latest_per_student(conn)}
    assert len(latest) == 30 and latest["S1002"]["score"] == 99.0
    recent = prediction_repository.recent(conn, 2)
    assert len(recent) == 2 and recent[0]["score"] == 99.0 and recent[0]["name"]
