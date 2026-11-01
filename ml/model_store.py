"""Saving the trained model to model.pkl and loading it again (cached) for predictions."""
import os

import joblib

from ml import config

_model = None


def save_model(model, path=None):
    path = path or config.MODEL_PATH
    joblib.dump(model, path)
    size_kb = os.path.getsize(path) / 1024
    print(f"\nModel saved to {path} ({size_kb:.0f} KB)")


def load_model(path=None):
    return joblib.load(path or config.MODEL_PATH)


def get_model():
    """Load model.pkl once and keep it in memory for every later prediction."""
    global _model
    if _model is None:
        _model = load_model()
    return _model


def reset_cache():
    global _model
    _model = None