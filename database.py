"""
RiskRadar — Database setup (SQLite) (kept for older imports and for `python database.py`).

The real code now lives in backend/db/ (connection, schema, seed).
"""
from backend.config import CSV_PATH, DB_PATH  # noqa: F401
from backend.db import get_db, init_db, seed_db  # noqa: F401

if __name__ == "__main__":
    init_db()
    seed_db()
