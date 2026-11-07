"""Role selection, login and logout pages."""
from flask import flash, redirect, render_template, request, session, url_for

from backend.services import check_login


def role_select():
    if "user" in session:
        if session["user"]["role"] == "teacher":
            return redirect(url_for("teacher_dashboard"))
        return redirect(url_for("student_me"))
    return render_template("role_select.html")


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


def logout():
    session.clear()
    return redirect(url_for("role_select"))


def register(app):
    app.add_url_rule("/", "role_select", role_select)
    app.add_url_rule("/login/<role>", "login", login, methods=["GET", "POST"])
    app.add_url_rule("/logout", "logout", logout)
