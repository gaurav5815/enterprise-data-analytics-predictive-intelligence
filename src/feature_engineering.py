import pandas as pd
import os
import numpy as np

PROCESSED_PATH = "data/processed"
FINAL_PATH = "data/final"

os.makedirs(FINAL_PATH, exist_ok=True)


def load_sales():
    return pd.read_csv(os.path.join(PROCESSED_PATH, "sales_data.csv"))


def create_features(df):

    df["date"] = pd.to_datetime(df["date"])

    # Expand data across multiple years
    years = [2021, 2022, 2023, 2024]

    expanded = []

    for year in years:
        temp = df.copy()
        temp["date"] = temp["date"] + pd.DateOffset(years=(year - 2023))
        expanded.append(temp)

    df = pd.concat(expanded)

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # Add more product categories
    categories = [
        "Electronics",
        "Clothing",
        "Beauty",
        "Sports",
        "Home",
        "Books",
        "Accessories"
    ]

    df["product_category"] = np.random.choice(categories, len(df))

    # Age groups
    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 25, 35, 50, 65],
        labels=["18-25", "26-35", "36-50", "50+"]
    )

    df["revenue_per_item"] = df["total_amount"] / df["quantity"]

    return df


def save_final_dataset(df):

    output = os.path.join(FINAL_PATH, "analytics_dataset.csv")

    df.to_csv(output, index=False)

    print("Final analytics dataset saved →", output)


def main():

    print("\nFeature Engineering Module\n")

    sales = load_sales()

    sales = create_features(sales)

    save_final_dataset(sales)


if __name__ == "__main__":
    main()