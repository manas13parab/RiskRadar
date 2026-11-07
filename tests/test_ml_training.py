import pytest

from ml import config, model_store
from ml.data_loader import check_columns, load_data
from ml.eda import eda
from ml.evaluator import evaluate, print_feature_importance, print_metrics
from ml.model_builder import build_model
from ml.pipeline import run
from ml.preprocessing import add_risk_column, prepare_xy
from ml.splitter import split_data
from ml.trainer import train


def test_load_data_reads_the_real_csv():
    df = load_data()
    assert df.shape == (5000, 23)


def test_load_data_rejects_a_csv_with_missing_columns(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("Student_ID,Midterm_Score\nS1,50\n")
    with pytest.raises(ValueError, match="missing column"):
        load_data(str(bad))


def test_check_columns_lists_what_is_missing():
    df = load_data().drop(columns=["Quizzes_Avg"])
    with pytest.raises(ValueError, match="Quizzes_Avg"):
        check_columns(df)


def test_prepare_xy_gives_7_features_and_the_target():
    X, y = prepare_xy(load_data())
    assert list(X.columns) == config.FEATURES and len(X) == len(y) == 5000


def test_add_risk_column_uses_the_risk_bands():
    df = add_risk_column(load_data())
    assert set(df["Risk"]) <= {"High", "Moderate", "Low"}
    assert (df.loc[df["Risk"] == "High", config.TARGET] < 60).all()
    assert (df.loc[df["Risk"] == "Low", config.TARGET] >= 70).all()


def test_split_is_80_20_and_repeatable():
    X, y = prepare_xy(load_data())
    a = split_data(X, y)
    b = split_data(X, y)
    assert len(a[0]) == 4000 and len(a[1]) == 1000
    assert list(a[0].index) == list(b[0].index)


def test_build_model_uses_the_configured_settings():
    model = build_model()
    assert model.n_estimators == 200 and model.max_depth == 15 and model.random_state == 42


def test_train_evaluate_and_reports(tiny_training, capsys):
    df = load_data()
    model = train(df)
    out = capsys.readouterr().out
    assert "MODEL TRAINING" in out and "Test Metrics" in out and "Feature Importance" in out
    assert len(model.feature_importances_) == 7
    X, y = prepare_xy(df)
    metrics = evaluate(model, X, y)
    assert set(metrics) == {"mae", "rmse", "r2"} and metrics["mae"] >= 0
    print_metrics(metrics)
    print_feature_importance(model)
    assert "MAE" in capsys.readouterr().out


def test_eda_prints_every_section(capsys):
    eda(load_data())
    out = capsys.readouterr().out
    for title in ["EXPLORATORY DATA ANALYSIS", "Numeric Summary", "Department Distribution",
                  "Grade Distribution", "Risk Distribution", "Correlation with Total_Score"]:
        assert title in out


def test_model_store_round_trip_and_cache(tiny_training, monkeypatch):
    model = build_model().fit(*prepare_xy(load_data()))
    model_store.save_model(model)
    assert (tiny_training / "model.pkl").exists()

    calls = []
    real_load = model_store.load_model
    monkeypatch.setattr(model_store, "load_model", lambda: calls.append(1) or real_load())
    model_store.reset_cache()
    first = model_store.get_model()
    assert model_store.get_model() is first and len(calls) == 1      # loaded only once
    model_store.reset_cache()


def test_whole_pipeline_creates_a_model_file(tiny_training, capsys):
    model_store.reset_cache()
    run()
    assert (tiny_training / "model.pkl").exists()
    assert capsys.readouterr().out.rstrip().endswith("Done.")
    model_store.reset_cache()
