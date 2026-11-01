"""The prediction step: inputs in, {score, risk, factors, tips} out."""
from ml.explain import top_factors
from ml.features import to_vector
from ml.model_store import get_model
from ml.recommendations import build_tips
from ml.risk import score_to_risk


def predict_score(features):
    """Predicted Total_Score, rounded to 1 decimal and kept between 0 and 100."""
    model = get_model()
    score = float(model.predict([to_vector(features)])[0])
    return max(0, min(100, round(score, 1)))


def run_prediction(features):
    score = predict_score(features)
    return {
        "score": score,
        "risk": score_to_risk(score),
        "factors": top_factors(get_model(), features),
        "tips": build_tips(features),
    }
