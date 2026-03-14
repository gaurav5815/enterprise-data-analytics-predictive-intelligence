import pandas as pd
import os

# Path configuration
RAW_DATA_PATH = "data/raw"

DATASETS = {
    "sales": "sales_data.csv",
    "customers": "customer_data.csv",
    "churn": "churn_data.csv"
}


def check_files():
    """Verify datasets exist"""
    print("Checking datasets...\n")

    for name, file in DATASETS.items():
        path = os.path.join(RAW_DATA_PATH, file)

        if os.path.exists(path):
            print(f"[OK] {file} found")
        else:
            print(f"[ERROR] {file} missing")


def load_dataset(file):
    """Load dataset using pandas"""
    path = os.path.join(RAW_DATA_PATH, file)
    df = pd.read_csv(path, encoding="latin1")
    return df


def summarize_dataset(name, df):
    """Print dataset summary"""
    print("\n----------------------------")
    print(f"Dataset: {name}")
    print("----------------------------")

    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns)

    print("\nFirst 5 rows:")
    print(df.head())


def main():

    print("\nEnterprise Data Analytics Platform")
    print("Data Ingestion Module\n")

    check_files()

    sales = load_dataset(DATASETS["sales"])
    customers = load_dataset(DATASETS["customers"])
    churn = load_dataset(DATASETS["churn"])

    summarize_dataset("Sales", sales)
    summarize_dataset("Customers", customers)
    summarize_dataset("Churn", churn)


if __name__ == "__main__":
    main()