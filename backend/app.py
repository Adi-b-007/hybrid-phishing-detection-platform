from flask import Flask, request, jsonify
from ml.predict import predict_url
from database import scan_collection
from datetime import datetime
from flask_cors import CORS
import validators
from bson import ObjectId

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "message": "Phishing Detection API Running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    print("===== PREDICT CALLED =====")
    data = request.get_json()
    print("Received:", data)

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        url = data.get("url", "").strip()

        # Empty URL check
        if not url:
            return jsonify({
                "error": "URL cannot be empty"
            }), 400

        # URL validation
        valid_url = validators.url(url)

        if not valid_url:
            valid_url = validators.url(
                "https://" + url
            )

        if not valid_url:
            return jsonify({
                "error": "Please enter a valid URL"
            }), 400

        result = predict_url(url)

        # Save only valid predictions
        scan_collection.update_one(

    {"url": result["url"]},

    {
        "$set": {
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "timestamp": datetime.now()
        }
    },

    upsert=True
)

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/history")
def history():

    records = []

    for item in scan_collection.find():

        records.append({
            "_id": str(item["_id"]),
            "url": item["url"],
            "prediction": item["prediction"],
            "confidence": item["confidence"],
            "timestamp": str(item["timestamp"])
        })

    return jsonify(records)

@app.route("/stats", methods=["GET"])
def stats():

    try:

        total = scan_collection.count_documents({})

        phishing = scan_collection.count_documents({
            "prediction": "Phishing"
        })

        legitimate = scan_collection.count_documents({
            "prediction": "Legitimate"
        })

        return jsonify({
            "total_scans": total,
            "phishing_urls": phishing,
            "legitimate_urls": legitimate
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/clear-history", methods=["DELETE"])
def clear_history():

    try:

        result = scan_collection.delete_many({})

        return jsonify({
            "message": "History cleared successfully",
            "deleted_records": result.deleted_count
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
@app.route("/history/delete/<id>", methods=["DELETE"])
def delete_history(id):

    try:

        result = scan_collection.delete_one({
            "_id": ObjectId(id)
        })

        return jsonify({
            "success": True,
            "deleted_count": result.deleted_count
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )