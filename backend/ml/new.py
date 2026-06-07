from predict import predict_url

test_urls = [
    "https://google.com",
    "https://youtube.com",
    "https://facebook.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://paypal-login-update.xyz",
    "https://secure-bank-verify-account.xyz"
]

for url in test_urls:

    pred, prob = predict_url(url)

    print(url)
    print("Prediction:", pred)
    print("Risk:", prob)
    print("-" * 50)