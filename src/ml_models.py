import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


PROCESSED_PATH = "data/processed"
MODEL_PATH = "models"

os.makedirs(MODEL_PATH, exist_ok=True)

# -------- NEW REPORT PATH --------
REPORT_PATH = "reports"
os.makedirs(REPORT_PATH, exist_ok=True)


# ---------------- LOAD DATA ----------------

def load_churn_data():
    path = os.path.join(PROCESSED_PATH, "churn_data.csv")
    return pd.read_csv(path)


# ---------------- PREPROCESSING ----------------

def preprocess_churn_data(df):

    df = df.drop("customerid", axis=1)

    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")

    df = df.fillna(df.median(numeric_only=True))

    encoder = LabelEncoder()

    for col in df.select_dtypes(include="object").columns:
        df[col] = encoder.fit_transform(df[col])

    X = df.drop("churn", axis=1)
    y = df["churn"]

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    return train_test_split(X, y, test_size=0.2, random_state=42)


# ---------------- MODEL EVALUATION ----------------

def evaluate_model(y_test, predictions, model_name):

    acc = accuracy_score(y_test, predictions)
    prec = precision_score(y_test, predictions)
    rec = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print(f"\nModel Evaluation: {model_name}")
    print("Accuracy:", acc)
    print("Precision:", prec)
    print("Recall:", rec)
    print("F1 Score:", f1)

    metrics = {
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1 Score": f1
    }

    fig, ax = plt.subplots()

    sns.barplot(x=list(metrics.keys()), y=list(metrics.values()), ax=ax)

    ax.set_title(f"{model_name} Performance")

    plt.savefig(os.path.join(REPORT_PATH, f"{model_name}_metrics.png"))

    plt.close()

    # Confusion Matrix

    cm = confusion_matrix(y_test, predictions)

    fig, ax = plt.subplots()

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)

    ax.set_title(f"{model_name} Confusion Matrix")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    plt.savefig(os.path.join(REPORT_PATH, f"{model_name}_confusion_matrix.png"))

    plt.close()


# ---------------- LOGISTIC REGRESSION ----------------

def train_logistic_regression(X_train, X_test, y_train, y_test):

    print("\nTraining Logistic Regression")

    model = LogisticRegression(max_iter=2000)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    evaluate_model(y_test, predictions, "logistic_regression")

    joblib.dump(model, os.path.join(MODEL_PATH, "logistic_regression.pkl"))


# ---------------- RANDOM FOREST ----------------

def train_random_forest(X_train, X_test, y_train, y_test):

    print("\nTraining Random Forest")

    model = RandomForestClassifier(n_estimators=200)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    evaluate_model(y_test, predictions, "random_forest")

    joblib.dump(model, os.path.join(MODEL_PATH, "random_forest.pkl"))


# ---------------- CUSTOMER SEGMENTATION ----------------

def customer_segmentation():

    print("\nRunning Customer Segmentation")

    path = os.path.join(PROCESSED_PATH, "sales_data.csv")

    df = pd.read_csv(path)

    features = df[["age", "total_amount"]]

    scaler = StandardScaler()

    X = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=4, random_state=42)

    clusters = kmeans.fit_predict(X)

    df["cluster"] = clusters

    output = os.path.join(PROCESSED_PATH, "customer_segments.csv")

    df.to_csv(output, index=False)

    print("Customer segmentation saved →", output)


# ---------------- MAIN PIPELINE ----------------

def main():

    print("\nEnterprise Data Analytics Platform")
    print("Machine Learning Engine\n")

    churn = load_churn_data()

    X_train, X_test, y_train, y_test = preprocess_churn_data(churn)

    train_logistic_regression(X_train, X_test, y_train, y_test)

    train_random_forest(X_train, X_test, y_train, y_test)

    customer_segmentation()


if __name__ == "__main__":
    main()