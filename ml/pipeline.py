"""The whole training run in order: load -> EDA -> train -> save."""
from ml.data_loader import load_data
from ml.eda import eda
from ml.model_store import save_model
from ml.trainer import train


def run():
    df = load_data()
    df = eda(df)
    model = train(df)
    save_model(model)
    print("\nDone.")
    return model
