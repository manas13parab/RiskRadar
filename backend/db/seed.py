"""
First-run seeding: if the database has no students, create the demo teacher
and load every student from students.csv together with a first prediction.
"""
import csv

from backend import config
from backend.db.connection import get_db
from backend.repositories import prediction_repository, student_repository, teacher_repository
from backend.security import default_student_password, hash_password
from backend.utils import days_ago_str
from ml.risk import score_to_risk


def seed_db():
    conn = get_db()
    count = student_repository.count(conn)
    if count > 0:
        print(f"Database already has {count} students — skipping seed.")
        conn.close()
        return

    print("Seeding database...")

    teacher_repository.insert(conn, config.TEACHER_ID, config.TEACHER_NAME,
                              hash_password(config.TEACHER_PASSWORD))

    with open(config.CSV_PATH) as f:
        reader = list(csv.DictReader(f))

    total = len(reader)
    for i, row in enumerate(reader):
        sid = row["Student_ID"]
        first = row["First_Name"]
        last = row["Last_Name"]
        name = f"{first} {last}"

        student_repository.insert(
            conn, sid, name, row["Email"], row["Department"], row["Gender"],
            int(row["Age"]), hash_password(default_student_password(first, sid)))

        # Initial prediction from CSV scores
        score = float(row["Total_Score"])
        days_ago = (total - i) % config.SEED_HISTORY_DAYS
        prediction_repository.insert(conn, sid, round(score, 1), score_to_risk(score),
                                     days_ago_str(days_ago))

        if (i + 1) % config.SEED_COMMIT_EVERY == 0:
            conn.commit()
            print(f"  {i + 1}/{total} students...")

    conn.commit()
    conn.close()
    print(f"Seeded {total} students + 1 teacher.")
