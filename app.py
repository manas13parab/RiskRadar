from flask import Flask, render_template, request, session, redirect, url_for, flash
from functools import wraps
from database import init_db, seed_db
from services import (check_login, get_students, get_dashboard_stats, predict,
                      get_history, get_latest, validate_roster)

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"

init_db()
seed_db()


def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("role_select"))
            if session["user"]["role"] != role:
                if session["user"]["role"] == "student":
                    return redirect(url_for("student_me"))
                return redirect(url_for("teacher_dashboard"))
            return f(*args, **kwargs)
        return wrapped
    return decorator


@app.route("/")
def role_select():
    if "user" in session:
        if session["user"]["role"] == "teacher":
            return redirect(url_for("teacher_dashboard"))
        return redirect(url_for("student_me"))
    return render_template("role_select.html")


@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if role not in ("teacher", "student"):
        return redirect(url_for("role_select"))
    if request.method == "POST":
        user_id = request.form.get("user_id", "").strip()
        password = request.form.get("password", "").strip()
        user = check_login(user_id, password, role)
        if user:
            session["user"] = user
            if role == "teacher":
                return redirect(url_for("teacher_dashboard"))
            return redirect(url_for("student_me"))
        flash("Invalid credentials. Please try again.", "error")
    return render_template("login.html", role=role)


@app.route("/teacher")
@login_required("teacher")
def teacher_dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


@app.route("/predict", methods=["GET", "POST"])
@login_required("teacher")
def predict_page():
    students = get_students()
    result = None
    selected_student = None
    if request.method == "POST":
        selected_student = request.form.get("student_id")
        features = {
            "midterm": float(request.form.get("midterm", 0)),
            "assignments": float(request.form.get("assignments", 0)),
            "quizzes": float(request.form.get("quizzes", 0)),
            "participation": float(request.form.get("participation", 0)),
            "projects": float(request.form.get("projects", 0)),
            "attendance": float(request.form.get("attendance", 0)),
            "study_hours": float(request.form.get("study_hours", 0)),
        }
        result = predict(features, student_id=selected_student)
    return render_template("predict.html", students=students, result=result,
                           selected_student=selected_student)


@app.route("/students")
@login_required("teacher")
def students_list():
    students = get_students()
    return render_template("students.html", students=students)


@app.route("/history/<student_id>")
@login_required("teacher")
def history(student_id):
    students = get_students()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("students_list"))
    records = get_history(student_id)
    return render_template("history.html", student=student, records=records)


@app.route("/upload", methods=["GET", "POST"])
@login_required("teacher")
def upload():
    return render_template("upload.html")


@app.route("/insights")
@login_required("teacher")
def insights():
    return render_template("insights.html")


@app.route("/me")
@login_required("student")
def student_me():
    user = session["user"]
    latest = get_latest(user["id"])
    return render_template("student_me.html", latest=latest)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("role_select"))
