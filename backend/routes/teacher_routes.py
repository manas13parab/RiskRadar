"""Teacher pages: dashboard, predict, students, history, upload, insights."""
from flask import flash, redirect, render_template, request, url_for

from backend.decorators import login_required
from backend.services import get_dashboard_stats, get_history, get_students, predict
from ml.features import parse_form


def teacher_dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


def predict_page():
    students = get_students()
    result = None
    selected_student = None
    if request.method == "POST":
        selected_student = request.form.get("student_id")
        features = parse_form(request.form)
        result = predict(features, student_id=selected_student)
    return render_template("predict.html", students=students, result=result,
                           selected_student=selected_student)


def students_list():
    students = get_students()
    return render_template("students.html", students=students)


def history(student_id):
    students = get_students()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for("students_list"))
    records = get_history(student_id)
    return render_template("history.html", student=student, records=records)


def upload():
    return render_template("upload.html")


def insights():
    return render_template("insights.html")


def register(app):
    teacher_only = login_required("teacher")
    app.add_url_rule("/teacher", "teacher_dashboard", teacher_only(teacher_dashboard))
    app.add_url_rule("/predict", "predict_page", teacher_only(predict_page), methods=["GET", "POST"])
    app.add_url_rule("/students", "students_list", teacher_only(students_list))
    app.add_url_rule("/history/<student_id>", "history", teacher_only(history))
    app.add_url_rule("/upload", "upload", teacher_only(upload), methods=["GET", "POST"])
    app.add_url_rule("/insights", "insights", teacher_only(insights))
