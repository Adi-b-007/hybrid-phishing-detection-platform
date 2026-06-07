import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# =====================================================
# URL NORMALIZATION
# =====================================================

def normalize_url(url):

    url = str(url).strip().lower()

    url = url.replace("https://", "")
    url = url.replace("http://", "")
    url = url.replace("www.", "")

    return url


# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LEGIT_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "legitimate_url2.csv"
)

PHISH_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset",
    "phishing_url1.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "..",
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "phishing_model.pkl"
)


# =====================================================
# LOAD DATASETS
# =====================================================

print("\nLoading datasets...")

legit = pd.read_csv(LEGIT_PATH)
phish = pd.read_csv(PHISH_PATH)

print("Legitimate URLs:", len(legit))
print("Phishing URLs:", len(phish))


# =====================================================
# ASSIGN LABELS
# =====================================================

legit["status"] = 1
phish["status"] = 0


# =====================================================
# BALANCE DATASET
# =====================================================

sample_size = min(
    60000,
    len(legit),
    len(phish)
)

legit = legit.sample(
    n=sample_size,
    random_state=42
)

phish = phish.sample(
    n=sample_size,
    random_state=42
)

data = pd.concat(
    [legit, phish],
    ignore_index=True
)

print("\nBalanced Dataset Size:", len(data))


# =====================================================
# KEEP REQUIRED COLUMNS
# =====================================================

data = data[["url", "status"]]

data["url"] = data["url"].apply(normalize_url)

data.drop_duplicates(
    subset=["url"],
    inplace=True
)

print(
    "Unique URLs:",
    data["url"].nunique()
)


# =====================================================
# FEATURES
# =====================================================

X = data["url"]
y = data["status"]


# =====================================================
# SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# =====================================================
# MODEL
# =====================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=50000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=3000
        )
    )
])


# =====================================================
# TRAIN
# =====================================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed.")


# =====================================================
# EVALUATE
# =====================================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nAccuracy: {accuracy*100:.2f}%"
)

print(
    classification_report(
        y_test,
        predictions
    )
)


# =====================================================
# SAVE MODEL
# =====================================================

joblib.dump(
    model,
    MODEL_PATH
)

print("\nModel saved:")
print(MODEL_PATH)


# =====================================================
# TEST URLs
# =====================================================

print("\nTESTING\n")

test_urls = [

    "google.com",
    "github.com",
    "amazon.com",
    "microsoft.com",

    "paypal-login-security.xyz",
    "secure-paypal-verification-login.xyz"
]

for url in test_urls:

    pred = model.predict([url])[0]

    print(
        url,
        "=>",
        "Legitimate"
        if pred == 1
        else "Phishing"
    )