"""Student page: "My Performance"."""
from flask import render_template, session

from backend.decorators import login_required
from backend.services import get_latest


def student_me():
    user = session["user"]
    latest = get_latest(user["id"])
    return render_template("student_me.html", latest=latest)


def register(app):
    app.add_url_rule("/me", "student_me", login_required("student")(student_me))
