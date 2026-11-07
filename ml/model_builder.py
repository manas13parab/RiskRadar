<<<<<<< HEAD
"""Step 4 of training: create the (not yet trained) model."""
=======
﻿"""Step 4 of training: create the (not yet trained) model."""
>>>>>>> origin/master
from sklearn.ensemble import RandomForestRegressor

from ml import config


def build_model():
    return RandomForestRegressor(**config.MODEL_PARAMS)
