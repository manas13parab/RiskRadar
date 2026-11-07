"""Backend settings: database/CSV paths, demo teacher account, secret key, date format."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# RISKRADAR_DB / RISKRADAR_CSV can point to other files (the tests use this).
DB_PATH = os.environ.get("RISKRADAR_DB") or os.path.join(BASE_DIR, "riskradar.db")
CSV_PATH = os.environ.get("RISKRADAR_CSV") or os.path.join(BASE_DIR, "students.csv")

SECRET_KEY = "dev-secret-key-change-in-production"

# Teacher account created on the first run: T01 / admin123
TEACHER_ID = "T01"
TEACHER_NAME = "Dr. Sarah Mitchell"
TEACHER_PASSWORD = "admin123"

DATE_FORMAT = "%b %d, %Y"      # e.g. Oct 24, 2026
RECENT_LIMIT = 5               # rows in "recent predictions" on the dashboard
SEED_COMMIT_EVERY = 500        # progress message / commit while seeding
SEED_HISTORY_DAYS = 30         # seeded predictions are spread over this many days
