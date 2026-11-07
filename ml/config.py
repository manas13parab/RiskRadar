"""
Central settings for the ML package: file paths, feature names, risk bands,
advice thresholds and model settings. Change a value here and training and
prediction both follow it.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "students.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Column names in students.csv. The ORDER is the order the model was trained with.
FEATURES = [
    "Midterm_Score",
    "Assignments_Avg",
    "Quizzes_Avg",
    "Participation_Score",
    "Projects_Score",
    "Attendance (%)",
    "Study_Hours_per_Week",
]
TARGET = "Total_Score"

# The same 7 inputs as named on the Predict form (same order as FEATURES)
FIELD_KEYS = ["midterm", "assignments", "quizzes", "participation",
              "projects", "attendance", "study_hours"]

# Names shown to the teacher in the "key factors" list (same order as FEATURES)
FEATURE_LABELS = ["Midterm", "Assignments", "Quizzes", "Participation",
                  "Projects", "Attendance", "Study Hours"]

# Risk bands on the predicted score
HIGH_RISK_BELOW = 60
MODERATE_RISK_BELOW = 70

# How a single input is labelled in the factors list
POSITIVE_FROM = 70
NEGATIVE_BELOW = 50
TOP_FACTORS = 5

# Training settings
TEST_SIZE = 0.2
RANDOM_STATE = 42
MODEL_PARAMS = {"n_estimators": 200, "max_depth": 15, "random_state": 42, "n_jobs": -1}

# Advice thresholds
TIP_ATTENDANCE_BELOW = 70
TIP_STUDY_HOURS_BELOW = 40
TIP_ASSIGNMENTS_BELOW = 60
TIP_MIDTERM_BELOW = 60
TIP_PARTICIPATION_BELOW = 50
