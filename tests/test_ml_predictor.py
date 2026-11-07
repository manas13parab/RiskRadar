import pytest

from conftest import STRONG, WEAK
from ml import model_store, predictor
from ml.predictor import predict_score, run_prediction


def test_result_has_the_four_keys_the_templates_use():
    result = run_prediction(STRONG)
    assert set(result) == {"score", "risk", "factors", "tips"}
    assert len(result["factors"]) == 5 and result["tips"]


def test_strong_student_is_low_risk_and_weak_student_is_high_risk():
    assert run_prediction(STRONG)["risk"] == "Low"
    assert run_prediction(WEAK)["risk"] == "High"
    assert predict_score(STRONG) > predict_score(WEAK)


def test_score_is_between_0_and_100_with_one_decimal():
    for features in (STRONG, WEAK, {}):
        score = predict_score(features)
        assert 0 <= score <= 100 and round(score, 1) == score


def test_missing_inputs_count_as_zero():
    assert predict_score({}) == predict_score(dict.fromkeys(STRONG, 0))


def test_risk_matches_the_score():
    result = run_prediction(dict(midterm=60, assignments=65, quizzes=60, participation=55,
                                 projects=66, attendance=72, study_hours=45))
    expected = "High" if result["score"] < 60 else "Moderate" if result["score"] < 70 else "Low"
    assert result["risk"] == expected


class Stub:
    def __init__(self, value):
        self.value = value

    def predict(self, rows):
        return [self.value]


@pytest.mark.parametrize("raw, shown", [(150.0, 100), (-12.0, 0), (64.26, 64.3)])
def test_score_is_clamped_and_rounded(monkeypatch, raw, shown):
    monkeypatch.setattr(predictor, "get_model", lambda: Stub(raw))
    assert predict_score(STRONG) == shown


def test_the_model_is_loaded_only_once():
    model_store.reset_cache()
    first = model_store.get_model()
    run_prediction(STRONG)
    assert model_store.get_model() is first
