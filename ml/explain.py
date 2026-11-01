"""Explains a prediction: which inputs matter most and whether each one helps or hurts."""
from ml import config


def impact_label(value):
    if value >= config.POSITIVE_FROM:
        return "positive"
    if value < config.NEGATIVE_BELOW:
        return "negative"
    return "neutral"


def top_factors(model, features):
    """The most important inputs of the model (by feature importance), with the student's value."""
    ranked = sorted(zip(config.FEATURE_LABELS, model.feature_importances_, config.FIELD_KEYS),
                    key=lambda x: -x[1])
    factors = []
    for name, _importance, key in ranked[:config.TOP_FACTORS]:
        value = features.get(key, 0)
        factors.append({"name": name, "value": value, "impact": impact_label(value)})
    return factors
