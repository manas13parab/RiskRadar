"""Step 5 of training: split, fit the model, evaluate it and print the report."""
from ml.evaluator import evaluate, print_feature_importance, print_metrics
from ml.model_builder import build_model
from ml.preprocessing import prepare_xy
from ml.splitter import split_data


def train(df):
    print("\n" + "=" * 60)
    print("MODEL TRAINING")
    print("=" * 60)

    X, y = prepare_xy(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")

    model = build_model()
    model.fit(X_train, y_train)

    print_metrics(evaluate(model, X_test, y_test))
    print_feature_importance(model)
    return model
