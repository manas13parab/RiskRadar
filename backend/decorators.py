"""login_required(role): only lets a logged-in user of that role open a page."""
from functools import wraps

from flask import redirect, session, url_for


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
