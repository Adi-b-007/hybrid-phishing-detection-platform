from predict import predict_url

url = "https://paypal-login-update.xyz"

prediction, probability = predict_url(url)

print("Prediction:", prediction)
print("Probability:", probability)