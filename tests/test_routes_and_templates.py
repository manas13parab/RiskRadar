import re
from pathlib import Path

import pytest

from conftest import ROOT

TEMPLATES = ROOT / "templates"


# ---------------------------------------------------------------- public pages
def test_start_page_and_login_pages(client):
    assert client.get("/").status_code == 200
    assert b"Teacher" in client.get("/login/teacher").data
    assert client.get("/login/student").status_code == 200
    assert client.get("/login/bogus").headers["Location"] == "/"


def test_wrong_password_shows_the_error_message(client):
    response = client.post("/login/teacher", data={"user_id": "T01", "password": "nope"})
    assert response.status_code == 200 and b"Invalid credentials" in response.data


def test_teacher_login_goes_to_dashboard(client):
    response = client.post("/login/teacher", data={"user_id": "T01", "password": "admin123"})
    assert response.status_code == 302 and response.headers["Location"].endswith("/teacher")


def test_student_login_goes_to_my_page(client):
    response = client.post("/login/student", data={"user_id": "S1000", "password": "omar@1000"})
    assert response.headers["Location"].endswith("/me")


# ---------------------------------------------------------------- role guards
@pytest.mark.parametrize("path", ["/teacher", "/predict", "/students", "/upload", "/insights",
                                  "/history/S1000", "/me"])
def test_pages_need_login(client, path):
    response = client.get(path)
    assert response.status_code == 302 and response.headers["Location"] == "/"


def test_student_cannot_open_teacher_pages(student_client):
    for path in ["/teacher", "/predict", "/students", "/upload", "/insights", "/history/S1000"]:
        assert student_client.get(path).headers["Location"].endswith("/me")


def test_teacher_cannot_open_student_page(teacher_client):
    assert teacher_client.get("/me").headers["Location"].endswith("/teacher")


def test_logged_in_user_is_sent_away_from_the_start_page(teacher_client):
    assert teacher_client.get("/").headers["Location"].endswith("/teacher")


def test_logout_clears_the_session(teacher_client):
    assert teacher_client.get("/logout").headers["Location"] == "/"
    assert teacher_client.get("/teacher").headers["Location"] == "/"


# ---------------------------------------------------------------- teacher pages
@pytest.mark.parametrize("path", ["/teacher", "/predict", "/students", "/upload", "/insights",
                                  "/history/S1000"])
def test_teacher_pages_render(teacher_client, path):
    assert teacher_client.get(path).status_code == 200


def test_dashboard_shows_the_stats(teacher_client):
    html = teacher_client.get("/teacher").get_data(as_text=True)
    assert "Total Students" in html and ">30<" in html.replace(" ", "").replace("\n", "")


def test_prediction_is_shown_and_saved_to_history(teacher_client):
    data = {"student_id": "S1002", "midterm": "95", "assignments": "95", "quizzes": "95",
            "participation": "95", "projects": "95", "attendance": "95", "study_hours": "95"}
    html = teacher_client.post("/predict", data=data).get_data(as_text=True)
    assert "84.9" in html and "Great work" in html
    assert "84.9" in teacher_client.get("/history/S1002").get_data(as_text=True)


def test_prediction_without_a_student_is_not_saved(teacher_client):
    data = {"student_id": "", "midterm": "40", "assignments": "40", "quizzes": "40",
            "participation": "40", "projects": "40", "attendance": "40", "study_hours": "40"}
    assert "58.1" in teacher_client.post("/predict", data=data).get_data(as_text=True)
    assert "58.1" not in teacher_client.get("/history/S1002").get_data(as_text=True)


def test_unknown_student_history_redirects_with_a_message(teacher_client):
    response = teacher_client.get("/history/NOPE")
    assert response.headers["Location"].endswith("/students")
    assert b"Student not found." in teacher_client.get("/students").data


def test_student_page_shows_the_latest_result(student_client):
    assert b"My Performance" in student_client.get("/me").data


def test_static_javascript_is_served(client):
    assert b"theme-toggle" in client.get("/static/app.js").data


# ---------------------------------------------------------------- frontend integration
def test_every_endpoint_used_by_a_template_exists(client):
    import app as app_module
    endpoints = {rule.endpoint for rule in app_module.app.url_map.iter_rules()}
    used = set()
    for html_file in TEMPLATES.glob("*.html"):
        used |= set(re.findall(r"url_for\(['\"]([a-z_]+)['\"]", html_file.read_text()))
    assert used and used <= endpoints, used - endpoints


def test_every_page_link_in_the_templates_is_a_real_route(client):
    import app as app_module
    paths = set()
    for html_file in TEMPLATES.glob("*.html"):
        paths |= set(re.findall(r'href="(/[a-z]*)"', html_file.read_text()))
    known = {rule.rule for rule in app_module.app.url_map.iter_rules()}
    assert paths <= known, paths - known


def test_all_endpoint_names_are_kept():
    import app as app_module
    endpoints = {rule.endpoint for rule in app_module.app.url_map.iter_rules()}
    assert {"role_select", "login", "logout", "teacher_dashboard", "predict_page", "students_list",
            "history", "upload", "insights", "student_me", "static"} == endpoints
