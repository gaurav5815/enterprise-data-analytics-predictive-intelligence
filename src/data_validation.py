import pandas as pd
import os

PROCESSED_PATH = "data/processed"

DATASETS = {
    "sales": "sales_data.csv",
    "customers": "customer_data.csv",
    "churn": "churn_data.csv"
}


def load_dataset(file):
    path = os.path.join(PROCESSED_PATH, file)
    return pd.read_csv(path)


def check_missing_values(df):
    missing = df.isnull().sum()
    print("\nMissing Values:")
    print(missing)


def check_data_types(df):
    print("\nColumn Data Types:")
    print(df.dtypes)


def detect_outliers(df):
    print("\nOutlier Detection (numeric columns):")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        print(f"{col}: {len(outliers)} potential outliers")


def dataset_report(name, df):

    print("\n===================================")
    print(f"Dataset Validation Report: {name}")
    print("===================================")

    print("Dataset Shape:", df.shape)

    check_missing_values(df)

    check_data_types(df)

    detect_outliers(df)


def main():

    print("\nEnterprise Data Analytics Platform")
    print("Data Validation Module\n")

    for name, file in DATASETS.items():

        df = load_dataset(file)

        dataset_report(name, df)


if __name__ == "__main__":
    main()