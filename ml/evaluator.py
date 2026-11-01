"""Step 6 of training: measure how good the model is and print the results."""
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml import config


def evaluate(model, X_test, y_test):
    """Return the test metrics as a dict: mae, rmse, r2."""
    y_pred = model.predict(X_test)
    return {
        "mae": mean_absolute_error(y_test, y_pred),
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
        "r2": r2_score(y_test, y_pred),
    }


def print_metrics(metrics):
    print(f"\n--- Test Metrics ---")
    print(f"  MAE  : {metrics['mae']:.2f}")
    print(f"  RMSE : {metrics['rmse']:.2f}")
    print(f"  R²   : {metrics['r2']:.4f}")


def print_feature_importance(model):
    print(f"\n--- Feature Importance ---")
    for feat, imp in sorted(zip(config.FEATURES, model.feature_importances_), key=lambda x: -x[1]):
        bar = "█" * int(imp * 50)
        print(f"  {feat:25s}: {imp:.4f}  {bar}")