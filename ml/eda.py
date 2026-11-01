"""Exploratory data analysis: prints a summary of the dataset before training."""
from ml import config
from ml.preprocessing import add_risk_column


def eda(df):
    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    print(f"\nDataset shape: {df.shape[0]} students, {df.shape[1]} columns\n")

    print("--- Numeric Summary ---")
    print(df[config.FEATURES + [config.TARGET]].describe().round(2).to_string())

    print("\n--- Department Distribution ---")
    print(df["Department"].value_counts().to_string())

    print("\n--- Grade Distribution ---")
    print(df["Grade"].value_counts().sort_index().to_string())

    df = add_risk_column(df)
    print("\n--- Risk Distribution ---")
    counts = df["Risk"].value_counts()
    for risk in ["High", "Moderate", "Low"]:
        n = counts.get(risk, 0)
        pct = n / len(df) * 100
        print(f"  {risk:10s}: {n:4d}  ({pct:.1f}%)")

    print("\n--- Correlation with Total_Score ---")
    corr = df[config.FEATURES + [config.TARGET]].corr()[config.TARGET].drop(config.TARGET).sort_values(ascending=False)
    for feat, val in corr.items():
        print(f"  {feat:25s}: {val:.4f}")

    return df
