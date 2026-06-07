import pandas as pd

legit = pd.read_csv("dataset/legitimate_url2.csv")
phish = pd.read_csv("dataset/phishing_url1.csv")

print("Legit labels:")
print(legit["label"].value_counts())

print("\nPhishing labels:")
print(phish["label"].value_counts())