"""Turns what the teacher typed into the numbers the model needs."""
from ml import config


def parse_form(form):
    """Read the 7 numbers of the Predict form into {key: float}."""
    return {key: float(form.get(key, 0)) for key in config.FIELD_KEYS}


def to_vector(features):
    """The 7 values in the exact order the model was trained with."""
    return [features.get(key, 0) for key in config.FIELD_KEYS]
