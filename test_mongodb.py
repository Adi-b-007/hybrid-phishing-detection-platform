from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/")

    client.admin.command("ping")

    print("MongoDB Connected Successfully!")

except Exception as e:
    print("Error:", e)