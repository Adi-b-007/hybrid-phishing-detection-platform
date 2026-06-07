from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["phishing_detection"]

scan_collection = db["scan_history"]