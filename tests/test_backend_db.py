import sqlite3

from backend import config
from backend.db import get_db, init_db, seed_db
from backend.repositories import student_repository
from ml.risk import score_to_risk


def test_init_db_creates_the_three_tables_and_can_run_twice(empty_db):
    init_db()
    init_db()
    names = {r[0] for r in sqlite3.connect(empty_db).execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"teachers", "students", "predictions"} <= names


def test_get_db_returns_rows_that_work_like_dicts(db):
    conn = get_db()
    try:
        row = conn.execute("SELECT id FROM teachers").fetchone()
        assert row["id"] == "T01"
    finally:
        conn.close()


def test_seed_loads_the_demo_teacher_students_and_first_predictions(empty_db, capsys):
    init_db()
    seed_db()
    conn = get_db()
    try:
        assert student_repository.count(conn) == 30
        assert conn.execute("SELECT COUNT(*) FROM teachers").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0] == 30
        for row in conn.execute("SELECT score, risk FROM predictions"):
            assert row["risk"] == score_to_risk(row["score"])
    finally:
        conn.close()
    assert "Seeded 30 students + 1 teacher." in capsys.readouterr().out


def test_seed_does_nothing_when_students_already_exist(db, capsys):
    seed_db()
    assert "already has 30 students" in capsys.readouterr().out
    conn = get_db()
    try:
        assert student_repository.count(conn) == 30
    finally:
        conn.close()


def test_seed_paths_come_from_the_config(db):
    assert config.CSV_PATH.endswith("students_mini.csv")
