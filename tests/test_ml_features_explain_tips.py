import pytest

from ml.explain import impact_label, top_factors
from ml.features import parse_form, to_vector
from ml.recommendations import build_tips

GOOD = dict(midterm=90, assignments=90, quizzes=90, participation=90,
            projects=90, attendance=90, study_hours=45)


# ---- features
def test_parse_form_turns_text_into_floats():
    form = {"midterm": "80", "assignments": "75.5", "quizzes": "70", "participation": "60",
            "projects": "85", "attendance": "90", "study_hours": "15"}
    parsed = parse_form(form)
    assert parsed["assignments"] == 75.5 and list(parsed) == list(form)


def test_parse_form_missing_field_is_zero_but_blank_text_is_an_error():
    assert parse_form({})["midterm"] == 0.0
    with pytest.raises(ValueError):
        parse_form({"midterm": ""})


def test_to_vector_keeps_the_training_order():
    features = {"midterm": 1, "assignments": 2, "quizzes": 3, "participation": 4,
                "projects": 5, "attendance": 6, "study_hours": 7}
    assert to_vector(features) == [1, 2, 3, 4, 5, 6, 7]
    assert to_vector({}) == [0] * 7


# ---- explain
@pytest.mark.parametrize("value, label", [(70, "positive"), (95, "positive"), (50, "neutral"),
                                           (69.9, "neutral"), (49.9, "negative"), (0, "negative")])
def test_impact_label(value, label):
    assert impact_label(value) == label


class FakeModel:
    feature_importances_ = [0.05, 0.10, 0.02, 0.30, 0.20, 0.25, 0.08]


def test_top_factors_are_ranked_by_importance_and_limited_to_five():
    features = dict(midterm=80, assignments=45, quizzes=60, participation=30,
                    projects=75, attendance=90, study_hours=20)
    factors = top_factors(FakeModel(), features)
    assert [f["name"] for f in factors] == ["Participation", "Attendance", "Projects",
                                           "Assignments", "Study Hours"]
    assert factors[0] == {"name": "Participation", "value": 30, "impact": "negative"}
    assert factors[1]["impact"] == "positive"


# ---- recommendations
def test_no_problems_gives_the_praise_message():
    assert build_tips(GOOD) == ["Great work — keep up the consistent effort!"]


@pytest.mark.parametrize("field, bad_value, words", [
    ("attendance", 65, "attendance"),
    ("study_hours", 30, "study hours"),
    ("assignments", 55, "assignment"),
    ("midterm", 55, "tutoring"),
    ("participation", 40, "discussions"),
])
def test_each_rule_fires_on_its_own(field, bad_value, words):
    tips = build_tips({**GOOD, field: bad_value})
    assert len(tips) == 1 and words in tips[0].lower()


def test_rules_use_strict_limits():
    assert build_tips({**GOOD, "attendance": 70}) == build_tips(GOOD)      # 70 is not below 70
    assert len(build_tips({**GOOD, "attendance": 69.9})) == 1
