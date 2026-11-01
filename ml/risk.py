"""Turns a predicted score into a risk level (High / Moderate / Low)."""
from ml import config


def score_to_risk(score):
    if score < config.HIGH_RISK_BELOW:
        return "High"
    if score < config.MODERATE_RISK_BELOW:
        return "Moderate"
    return "Low"
