import pandas as pd
import os

RAW_PATH = "data/raw"
PROCESSED_PATH = "data/processed"

DATASETS = {
    "sales": "sales_data.csv",
    "customers": "customer_data.csv",
    "churn": "churn_data.csv"
}


def load_data(file):
    path = os.path.join(RAW_PATH, file)
    return pd.read_csv(path, encoding="latin1")


def standardize_columns(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df


def remove_duplicates(df):
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]

    print(f"Removed {before - after} duplicate rows")
    return df


def handle_missing_values(df):
    missing = df.isnull().sum()

    print("\nMissing values:")
    print(missing)

    df = df.ffill()

    return df


def save_clean_data(df, filename):
    path = os.path.join(PROCESSED_PATH, filename)
    df.to_csv(path, index=False)
    print(f"Saved cleaned dataset → {path}")


def clean_dataset(name, file):

    print("\n=============================")
    print(f"Cleaning dataset: {name}")
    print("=============================")

    df = load_data(file)

    df = standardize_columns(df)

    df = remove_duplicates(df)

    df = handle_missing_values(df)

    save_clean_data(df, file)


def main():

    print("\nEnterprise Data Analytics Platform")
    print("Data Cleaning Module\n")

    for name, file in DATASETS.items():
        clean_dataset(name, file)


if __name__ == "__main__":
    main()