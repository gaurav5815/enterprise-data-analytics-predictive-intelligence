import streamlit as st
import pandas as pd
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Enterprise Data Intelligence Platform",
    layout="wide"
)

DATA_PATH = "data/final"
MODEL_PATH = "models"


@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(DATA_PATH, "analytics_dataset.csv"))


@st.cache_data
def load_segments():
    return pd.read_csv("data/processed/customer_segments.csv")


def load_model():
    return joblib.load(os.path.join(MODEL_PATH, "random_forest.pkl"))


st.title("Enterprise Data Analytics Platform")

st.sidebar.title("Dashboard Controls")

data = load_data()

# ---------------- FILTERS ----------------

year_filter = st.sidebar.multiselect(
    "Year",
    options=data["year"].unique(),
    default=data["year"].unique()
)

category_filter = st.sidebar.multiselect(
    "Product Category",
    options=data["product_category"].unique(),
    default=data["product_category"].unique()
)

# Safe gender filter
if "gender" in data.columns:
    gender_filter = st.sidebar.multiselect(
        "Gender",
        options=data["gender"].dropna().unique(),
        default=data["gender"].dropna().unique()
    )
else:
    gender_filter = []

# Apply filters
filtered_data = data[
    (data["year"].isin(year_filter)) &
    (data["product_category"].isin(category_filter))
]

if "gender" in data.columns and gender_filter:
    filtered_data = filtered_data[
        filtered_data["gender"].isin(gender_filter)
    ]


# ---------------- NAVIGATION ----------------

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Sales Analytics",
        "Product Insights",
        "Customer Segmentation",
        "Churn Prediction"
    ]
)

# ---------------- SALES ANALYTICS ----------------

if page == "Sales Analytics":

    st.header("Sales Analytics")

    total_revenue = filtered_data["total_amount"].sum()
    total_transactions = filtered_data["transaction_id"].count()

    col1, col2 = st.columns(2)

    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Transactions", total_transactions)

    monthly_sales = filtered_data.groupby("month")["total_amount"].sum()

    fig, ax = plt.subplots()

    monthly_sales.plot(ax=ax)

    ax.set_title("Monthly Revenue Trend")

    st.pyplot(fig)

# ---------------- PRODUCT INSIGHTS ----------------

elif page == "Product Insights":

    st.header("Revenue by Product Category")

    category_sales = filtered_data.groupby("product_category")["total_amount"].sum()

    fig, ax = plt.subplots()

    sns.barplot(x=category_sales.index, y=category_sales.values, ax=ax)

    ax.set_ylabel("Revenue")

    st.pyplot(fig)

    st.subheader("Customer Age Distribution")

    if "age_group" in filtered_data.columns:
        st.bar_chart(filtered_data["age_group"].value_counts())

# ---------------- CUSTOMER SEGMENTATION ----------------

elif page == "Customer Segmentation":

    st.header("Customer Segmentation")

    segments = load_segments()

    fig, ax = plt.subplots()

    sns.scatterplot(
        x=segments["age"],
        y=segments["total_amount"],
        hue=segments["cluster"],
        palette="Set2",
        ax=ax
    )

    st.pyplot(fig)

# ---------------- CHURN PREDICTION ----------------

elif page == "Churn Prediction":

    st.header("Customer Churn Prediction")

    model = load_model()

    gender = st.selectbox("Gender", ["Male", "Female"])
    tenure = st.slider("Tenure (months)", 0, 72)
    monthly = st.number_input("Monthly Charges", 0.0, 200.0)
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

    if st.button("Predict Churn"):

        input_data = pd.DataFrame({
            "gender": [1 if gender == "Male" else 0],
            "tenure": [tenure],
            "monthlycharges": [monthly],
            "internetservice": [1 if internet == "Fiber optic" else 0],
            "contract": [0 if contract == "Month-to-month" else 1]
        })

        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)[0][1]

        if prediction[0] == 1:
            st.error(f"Customer likely to churn (Probability: {probability:.2%})")
        else:
            st.success(f"Customer likely to stay (Probability: {(1-probability):.2%})")