import os
import joblib
from urllib.parse import urlparse
# =====================================================
# NORMALIZATION
# =====================================================

def normalize_url(url):
    

    url = str(url).strip().lower()

    url = url.replace("https://", "")
    url = url.replace("http://", "")
    url = url.replace("www.", "")

    return url
def extract_domain(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    return parsed.netloc.replace("www.", "")
# =====================================================
# THREAT ANALYSIS
# =====================================================

def get_threat_reasons(url):

    reasons = []

    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "bank",
        "paypal",
        "signin"
    ]

    for word in suspicious_words:

        if word in url:

            reasons.append(
                f"Contains suspicious keyword: {word}"
            )

    if ".xyz" in url:

        reasons.append(
            "Uses high-risk TLD (.xyz)"
        )

    if ".top" in url:

        reasons.append(
            "Uses high-risk TLD (.top)"
        )

    if url.count("-") >= 2:

        reasons.append(
            "Contains multiple hyphens"
        )

    if len(url) > 50:

        reasons.append(
            "URL length is unusually long"
        )

    return reasons
# =====================================================
# DOMAIN INTELLIGENCE
# =====================================================

# =====================================================
# DOMAIN INTELLIGENCE
# =====================================================

def get_domain_info(original_url):

    if original_url.startswith("http://"):

        protocol = "HTTP"

        full_url = original_url

    elif original_url.startswith("https://"):

        protocol = "HTTPS"

        full_url = original_url

    else:

        protocol = "UNKNOWN"

        full_url = "https://" + original_url

    parsed = urlparse(full_url)

    domain = parsed.netloc.replace(
        "www.",
        ""
    )

    tld = "." + domain.split(".")[-1]

    domain_length = len(domain)

    hyphens = domain.count("-")

    contains_digits = any(
        char.isdigit()
        for char in domain
    )

    risk_level = "Low"

    if (
        protocol == "HTTP"
        or tld in [".xyz", ".top", ".tk"]
        or hyphens >= 2
        or domain_length > 30
    ):
        risk_level = "High"

    elif (
        hyphens == 1
        or domain_length > 20
    ):
        risk_level = "Medium"

    return {

        "domain": domain,

        "tld": tld,

        "length": domain_length,

        "hyphens": hyphens,

        "contains_digits":
            "Yes"
            if contains_digits
            else "No",

        "protocol": protocol,

        "risk_level": risk_level
    }
# =====================================================
# LOAD MODEL
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "..",
    "models",
    "phishing_model.pkl"
)

print("\nLoading model:")
print(MODEL_PATH)

model = joblib.load(
    MODEL_PATH
)

print("Model loaded successfully")

# =====================================================
# TRUSTED DOMAINS
# =====================================================

TRUSTED_DOMAINS = [

    "google.com",
    "gemini.google.com",
    "github.com",
    "microsoft.com",
    "amazon.com",
    "wikipedia.org",
    "openai.com",
    "chatgpt.com"

]

# =====================================================
# RISK SCORING ENGINE
# =====================================================

def calculate_risk_score(
    confidence,
    prediction,
    reasons,
    domain_info
):

    score = 0

    # ML Contribution

    if prediction == 0:
        score += confidence * 0.5

    # HTTP Protocol

    if domain_info["protocol"] == "HTTP":
        score += 25

    # Threat Reasons

    score += len(reasons) * 10

    # Risky TLD

    if domain_info["tld"] in [
        ".xyz",
        ".top",
        ".tk"
    ]:
        score += 20

    # Hyphens

    if domain_info["hyphens"] >= 2:
        score += 15

    # Long Domain

    if domain_info["length"] > 25:
        score += 10

    # Digits

    if (
        domain_info["contains_digits"]
        == "Yes"
    ):
        score += 10

    return min(
        round(score),
        100
    )
# =====================================================
# PREDICTION
# =====================================================

def predict_url(url):

    original_url = url.strip()

    is_http = False

    if original_url.lower().startswith(
        "http://"
    ):
        is_http = True

    normalized_url = normalize_url(
        original_url
    )

    # -------------------------
    # ML Prediction
    # -------------------------

    prediction = model.predict(
        [normalized_url]
    )[0]

    probabilities = model.predict_proba(
        [normalized_url]
    )[0]

    confidence = round(
        max(probabilities) * 100,
        2
    )

    # -------------------------
    # Rule Engine
    # -------------------------

    reasons = get_threat_reasons(
        normalized_url
    )

    if is_http:

        reasons.append(
            "Uses insecure HTTP protocol"
        )

        reasons.append(
            "Website does not use encrypted HTTPS"
        )

    # -------------------------
    # Domain Intelligence
    # -------------------------

    domain_info = get_domain_info(
        original_url
    )

    # -------------------------
    # Trusted Domain Check
    # -------------------------

    trusted = False

    for trusted_domain in TRUSTED_DOMAINS:

        if trusted_domain in normalized_url:

            trusted = True
            break

    # -------------------------
    # Risk Score Calculation
    # -------------------------

    risk_score = calculate_risk_score(

        confidence,

        prediction,

        reasons,

        domain_info

    )

    # -------------------------
    # Final Decision Engine
    # -------------------------

    if trusted:

        final_prediction = "Legitimate"

        risk_score = min(
            risk_score,
            15
        )

    elif risk_score >= 70:

        final_prediction = "Phishing"

    elif risk_score >= 40:

        final_prediction = "Suspicious"

    else:

        final_prediction = "Legitimate"

    # -------------------------
    # Debug Logs
    # -------------------------

    print("\n========== URL ANALYSIS ==========")
    print("URL:", normalized_url)
    print("ML Prediction:", prediction)
    print("ML Confidence:", confidence)
    print("Risk Score:", risk_score)
    print("Final:", final_prediction)
    print("==================================")

    return {

        "url":
            normalized_url,

        "prediction":
            final_prediction,

        "status_code":
            int(prediction),

        "confidence":
            confidence,

        "risk_score":
            risk_score,

        "reasons":
            reasons,

        "domain_info":
            domain_info
    }
# =====================================================
# DIRECT TESTING
# =====================================================

if __name__ == "__main__":

    urls = [

        "google.com",
        "github.com",
        "amazon.com",
        "microsoft.com",

        "paypal-login-security.xyz",
        "secure-paypal-verification-login.xyz"
    ]

    for url in urls:

        print(
            "\n",
            predict_url(url)
        )
