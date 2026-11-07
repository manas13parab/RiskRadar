"""Step 4 of training: create the (not yet trained) model."""
from sklearn.ensemble import RandomForestRegressor

from ml import config


def build_model():
    return RandomForestRegressor(**config.MODEL_PARAMS)
