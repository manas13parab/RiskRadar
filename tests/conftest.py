"""
Shared test setup.

A small database (30 students taken from students.csv) is created ONCE before the app is
imported, then every test gets its own private copy of it. The real riskradar.db is never touched.
"""
import os
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

_TMP = Path(tempfile.mkdtemp(prefix="riskradar_tests_"))
_MINI_CSV = _TMP / "students_mini.csv"
_TEMPLATE_DB = _TMP / "template.db"
_MINI_CSV.write_text("\n".join((ROOT / "students.csv").read_text().splitlines()[:31]) + "\n")
os.environ["RISKRADAR_CSV"] = str(_MINI_CSV)
os.environ["RISKRADAR_DB"] = str(_TEMPLATE_DB)

from backend import config  # noqa: E402  (must come after the environment is set)
from backend.db import init_db, seed_db  # noqa: E402

init_db()
seed_db()

STRONG = dict(midterm=95, assignments=95, quizzes=95, participation=95,
              projects=95, attendance=95, study_hours=95)
WEAK = dict(midterm=40, assignments=40, quizzes=40, participation=40,
            projects=40, attendance=40, study_hours=40)


@pytest.fixture
def db(tmp_path, monkeypatch):
    """A fresh copy of the 30-student test database for one test."""
    path = tmp_path / "test.db"
    shutil.copy(_TEMPLATE_DB, path)
    monkeypatch.setattr(config, "DB_PATH", str(path))
    return path


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    """An empty database file (no tables yet)."""
    path = tmp_path / "empty.db"
    monkeypatch.setattr(config, "DB_PATH", str(path))
    return path


@pytest.fixture
def client(db):
    import app as app_module
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


@pytest.fixture
def teacher_client(client):
    client.post("/login/teacher", data={"user_id": "T01", "password": "admin123"})
    return client


@pytest.fixture
def student_client(client):
    client.post("/login/student", data={"user_id": "S1000", "password": "omar@1000"})
    return client


@pytest.fixture
def tiny_training(monkeypatch, tmp_path):
    """Makes training fast: 300 rows, 10 trees, model saved in a temp folder."""
    from ml import config as ml_config
    small = tmp_path / "small.csv"
    small.write_text("\n".join((ROOT / "students.csv").read_text().splitlines()[:301]) + "\n")
    monkeypatch.setattr(ml_config, "CSV_PATH", str(small))
    monkeypatch.setattr(ml_config, "MODEL_PATH", str(tmp_path / "model.pkl"))
    monkeypatch.setattr(ml_config, "MODEL_PARAMS", {"n_estimators": 10, "max_depth": 5,
                                                      "random_state": 42, "n_jobs": 1})
    return tmp_path
