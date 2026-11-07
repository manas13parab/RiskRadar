"""Rule-based advice for a student, based on the 7 inputs."""
from ml import config


def build_tips(features):
    tips = []
    if features.get("attendance", 0) < config.TIP_ATTENDANCE_BELOW:
        tips.append("Improve class attendance — aim for at least 85%.")
    if features.get("study_hours", 0) < config.TIP_STUDY_HOURS_BELOW:
        tips.append("Increase weekly study hours to at least 10–15 hours.")
    if features.get("assignments", 0) < config.TIP_ASSIGNMENTS_BELOW:
        tips.append("Focus on completing and improving assignment scores.")
    if features.get("midterm", 0) < config.TIP_MIDTERM_BELOW:
        tips.append("Seek tutoring or office hours to strengthen exam performance.")
    if features.get("participation", 0) < config.TIP_PARTICIPATION_BELOW:
        tips.append("Engage more actively in class discussions and activities.")
    if not tips:
        tips.append("Great work — keep up the consistent effort!")
    return tips
