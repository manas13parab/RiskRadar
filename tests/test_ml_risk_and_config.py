import pytest

from ml import config
from ml.risk import score_to_risk


def test_feature_lists_have_the_same_length():
    assert len(config.FEATURES) == len(config.FIELD_KEYS) == len(config.FEATURE_LABELS) == 7


def test_form_keys_are_the_ones_on_the_predict_page():
    assert config.FIELD_KEYS == ["midterm", "assignments", "quizzes", "participation",
                                 "projects", "attendance", "study_hours"]


@pytest.mark.parametrize("score, risk", [
    (0, "High"), (59.9, "High"), (60, "Moderate"), (69.9, "Moderate"),
    (70, "Low"), (100, "Low"),
])
def test_score_to_risk_boundaries(score, risk):
    assert score_to_risk(score) == risk
