"""Database package: connection, table creation, first-run seeding."""
from backend.db.connection import get_db
from backend.db.schema import init_db
from backend.db.seed import seed_db

__all__ = ["get_db", "init_db", "seed_db"]
