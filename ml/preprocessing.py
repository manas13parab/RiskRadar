"""Step 2 of training: pick the model inputs and the target out of the data."""
from ml import config
from ml.risk import score_to_risk


def prepare_xy(df):
    """Return (X, y): the 7 feature columns and the Total_Score column."""
    return df[config.FEATURES], df[config.TARGET]


def add_risk_column(df):
    """Add a 'Risk' column (High / Moderate / Low) based on Total_Score."""
    df["Risk"] = df[config.TARGET].apply(score_to_risk)
    return df
