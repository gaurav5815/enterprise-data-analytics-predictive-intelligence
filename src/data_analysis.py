import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

PROCESSED_PATH = "data/processed"
REPORT_PATH = "reports"

os.makedirs(REPORT_PATH, exist_ok=True)


def load_data(file):
    path = os.path.join(PROCESSED_PATH, file)
    return pd.read_csv(path)


def sales_statistics(df):

    print("\nSales Dataset Statistics\n")

    print(df.describe())


def top_product_categories(df):

    print("\nTop Product Categories\n")

    category_sales = df.groupby("product_category")["total_amount"].sum().sort_values(ascending=False)

    print(category_sales)

    plt.figure(figsize=(8,5))
    sns.barplot(x=category_sales.index, y=category_sales.values)

    plt.title("Top Product Categories by Revenue")
    plt.xticks(rotation=45)

    plt.savefig(os.path.join(REPORT_PATH, "top_categories.png"))
    plt.close()


def monthly_sales_trend(df):

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.to_period("M")

    monthly_sales = df.groupby("month")["total_amount"].sum()

    print("\nMonthly Sales Trend\n")

    print(monthly_sales)

    plt.figure(figsize=(10,5))
    monthly_sales.plot()

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")

    plt.savefig(os.path.join(REPORT_PATH, "monthly_sales.png"))
    plt.close()


def revenue_distribution(df):

    plt.figure(figsize=(8,5))
    sns.histplot(df["total_amount"], bins=30)

    plt.title("Revenue Distribution")

    plt.savefig(os.path.join(REPORT_PATH, "revenue_distribution.png"))
    plt.close()


def main():

    print("\nEnterprise Data Analytics Platform")
    print("EDA & Analytics Engine\n")

    sales = load_data("sales_data.csv")

    sales_statistics(sales)

    top_product_categories(sales)

    monthly_sales_trend(sales)

    revenue_distribution(sales)


if __name__ == "__main__":
    main()