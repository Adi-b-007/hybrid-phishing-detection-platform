import re
import math
from collections import Counter
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "bank",
    "confirm",
    "signin",
    "password",
    "wallet",
    "crypto",
    "payment"
]

SUSPICIOUS_TLDS = [
    ".xyz",
    ".top",
    ".tk",
    ".cf",
    ".gq",
    ".ml",
    ".work",
    ".click"
]


def calculate_entropy(text):

    if not text:
        return 0

    prob = [
        n / len(text)
        for n in Counter(text).values()
    ]

    return -sum(
        p * math.log2(p)
        for p in prob
    )


def extract_features(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    path = parsed.path.lower()

    query = parsed.query.lower()

    features = {

        # BASIC FEATURES
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),

        # CHARACTER COUNTS
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "slash_count": url.count("/"),
        "digit_count": sum(c.isdigit() for c in url),

        # SPECIAL CHARACTERS
        "special_char_count":
            len(re.findall(r'[@?&=%]', url)),

        "has_at":
            1 if "@" in url else 0,

        # HTTPS
        "has_https":
            1 if parsed.scheme == "https"
            else 0,

        # IP ADDRESS
        "has_ip":
            1 if re.search(
                r'(\d{1,3}\.){3}\d{1,3}',
                url
            )
            else 0,

        # SUBDOMAINS
        "subdomain_count":
            max(0, domain.count(".") - 1),

        # SUSPICIOUS WORDS
        "suspicious_keyword":
            1 if any(
                word in url.lower()
                for word in SUSPICIOUS_WORDS
            )
            else 0,

        # SUSPICIOUS TLD
        "suspicious_tld":
            1 if any(
                domain.endswith(tld)
                for tld in SUSPICIOUS_TLDS
            )
            else 0,

        # QUERY PARAMETERS
        "query_length":
            len(query),

        "query_param_count":
            query.count("&"),

        # DOMAIN DIGITS
        "domain_digit_count":
            sum(
                c.isdigit()
                for c in domain
            ),

        # RANDOMNESS
        "url_entropy":
            calculate_entropy(url),

        "domain_entropy":
            calculate_entropy(domain),

        # DOUBLE SLASH
        "double_slash_count":
            url.count("//"),

        # PATH DEPTH
        "path_depth":
            len(
                [
                    p for p in path.split("/")
                    if p
                ]
            ),

        # LONG DOMAIN
        "long_domain":
            1 if len(domain) > 25
            else 0,

        # LONG URL
        "long_url":
            1 if len(url) > 75
            else 0
    }

    return features