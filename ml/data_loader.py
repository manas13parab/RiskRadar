"""Step 1 of training: read students.csv and check it has the columns we need."""
import pandas as pd

from ml import config

# Columns used by training (features + target) and by the EDA printout
REQUIRED_COLUMNS = config.FEATURES + [config.TARGET, "Department", "Grade"]


def check_columns(df):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("students.csv is missing column(s): " + ", ".join(missing))


def load_data(csv_path=None):
    df = pd.read_csv(csv_path or config.CSV_PATH)
    check_columns(df)
<<<<<<< HEAD
    return df
=======
    return df
>>>>>>> origin/master
