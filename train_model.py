"""
RiskRadar — Model Training & EDA

Run:  python train_model.py
Trains a Random Forest to predict Total_Score from the 7 features the teacher
enters on the prediction form, and saves it to model.pkl.

The work is split into small files inside the ml/ package
(data_loader, preprocessing, splitter, model_builder, trainer, evaluator, model_store ...).
This file is the entry point and keeps the old names importable.
"""
from ml.config import CSV_PATH, FEATURES, MODEL_PATH, TARGET  # noqa: F401
from ml.data_loader import load_data  # noqa: F401
from ml.eda import eda  # noqa: F401
from ml.model_store import save_model  # noqa: F401
from ml.pipeline import run
from ml.trainer import train  # noqa: F401

if __name__ == "__main__":
    run()
