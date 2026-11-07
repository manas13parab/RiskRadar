import random
from datetime import datetime, timedelta

_DEPARTMENTS = ["Computer Science", "Mathematics", "Physics", "Biology", "Chemistry",
                "Economics", "Psychology", "Engineering", "English", "History"]

_FIRST_NAMES = ["Omar", "Priya", "Liam", "Fatima", "Chen", "Amara", "James", "Sofia",
                "Yuki", "Aisha", "Noah", "Isabella", "Mateo", "Zara", "Ethan",
                "Mei", "Lucas", "Nadia", "Aarav", "Chloe", "Daniel", "Leila",
                "Ryan", "Hannah", "Kai"]

_LAST_NAMES = ["Williams", "Patel", "O'Brien", "Al-Rashid", "Wei", "Okafor", "Thompson",
               "Rodriguez", "Tanaka", "Hassan", "Carter", "Moretti", "Garcia", "Ahmed",
               "Kim", "Zhang", "Silva", "Johansson", "Sharma", "Dubois", "Park",
               "Fernandez", "Murphy", "Larsson", "Nakamura"]

random.seed(42)

_STUDENTS = []
for i in range(25):
    sid = f"S{1000 + i}"
    score = random.randint(35, 98)
    if score < 60:
        risk = "High"
    elif score < 70:
        risk = "Moderate"
    else:
        risk = "Low"
    _STUDENTS.append({
        "id": sid,
        "name": f"{_FIRST_NAMES[i]} {_LAST_NAMES[i]}",
        "department": random.choice(_DEPARTMENTS),
        "score": score,
        "risk": risk,
    })


def check_login(user_id, password, role):
    if role == "teacher" and user_id == "T01" and password == "admin123":
        return {"id": "T01", "name": "Dr. Sarah Mitchell", "role": "teacher"}
    if role == "student" and user_id == "S1000" and password == "omar@1000":
        return {"id": "S1000", "name": "Omar Williams", "role": "student"}
    return None


def get_students():
    return list(_STUDENTS)


def get_dashboard_stats():
    high = sum(1 for s in _STUDENTS if s["risk"] == "High")
    moderate = sum(1 for s in _STUDENTS if s["risk"] == "Moderate")
    low = sum(1 for s in _STUDENTS if s["risk"] == "Low")
    by_risk = {"High": [], "Moderate": [], "Low": []}
    for s in _STUDENTS:
        by_risk[s["risk"]].append(s)
    recent = []
    for group in [by_risk["High"], by_risk["Moderate"], by_risk["Low"]]:
        random.seed(42)
        picked = random.sample(group, min(2, len(group)))
        recent.extend(picked)
    recent = recent[:5]
    return {
        "total": len(_STUDENTS),
        "high": high,
        "moderate": moderate,
        "low": low,
        "recent": [{"id": s["id"], "name": s["name"], "score": s["score"],
                     "risk": s["risk"], "date": (datetime.now() - timedelta(days=random.randint(0, 6))).strftime("%b %d, %Y")}
                    for s in recent],
    }


def predict(features):
    weights = {
        "midterm": 0.25,
        "assignments": 0.20,
        "quizzes": 0.15,
        "participation": 0.10,
        "projects": 0.15,
        "attendance": 0.10,
        "study_hours": 0.05,
    }
    score = sum(features.get(k, 0) * w for k, w in weights.items())
    score = max(0, min(100, round(score, 1)))

    if score < 60:
        risk = "High"
    elif score < 70:
        risk = "Moderate"
    else:
        risk = "Low"

    sorted_factors = sorted(weights.items(), key=lambda x: abs(features.get(x[0], 0) * x[1]), reverse=True)
    factors = []
    for name, weight in sorted_factors[:5]:
        val = features.get(name, 0)
        impact = "positive" if val >= 70 else "negative" if val < 50 else "neutral"
        factors.append({"name": name.replace("_", " ").title(), "value": val, "impact": impact})

    tips = []
    if features.get("attendance", 0) < 70:
        tips.append("Improve class attendance — aim for at least 85%.")
    if features.get("study_hours", 0) < 40:
        tips.append("Increase weekly study hours to at least 10–15 hours.")
    if features.get("assignments", 0) < 60:
        tips.append("Focus on completing and improving assignment scores.")
    if features.get("midterm", 0) < 60:
        tips.append("Seek tutoring or office hours to strengthen exam performance.")
    if features.get("participation", 0) < 50:
        tips.append("Engage more actively in class discussions and activities.")
    if not tips:
        tips.append("Great work — keep up the consistent effort!")

    return {"score": score, "risk": risk, "factors": factors, "tips": tips}


def get_history(student_id):
    student = next((s for s in _STUDENTS if s["id"] == student_id), None)
    if not student:
        return []
    random.seed(hash(student_id))
    base = student["score"]
    history = []
    for i in range(6):
        dt = datetime.now() - timedelta(days=30 * (5 - i))
        s = max(0, min(100, base + random.randint(-15, 10)))
        if s < 60:
            r = "High"
        elif s < 70:
            r = "Moderate"
        else:
            r = "Low"
        history.append({"date": dt.strftime("%b %d, %Y"), "score": s, "risk": r})
    random.seed(42)
    return history


def get_latest(student_id):
    history = get_history(student_id)
    return history[-1] if history else None


def validate_roster(dataframe_columns):
    required = {"student_id", "name", "department"}
    cols = set(dataframe_columns)
    errors = []
    missing = required - cols
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
    extra = cols - required
    if extra:
        errors.append(f"Unexpected columns: {', '.join(sorted(extra))}")
    return errors
