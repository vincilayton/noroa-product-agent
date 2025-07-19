from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_URL = os.getenv("SHOPIFY_ADMIN_URL")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        raw_data = request.get_data(as_text=True)
        print("Raw data:", raw_data)

        data = request.get_json(silent=True)
        print("Parsed JSON:", data)

        if not data:
            return jsonify({"status": "error", "message": "No JSON payload received"}), 400

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_TOKEN
        }

        response = requests.post(
            f"{SHOPIFY_API_URL}/products.json",
            headers=headers,
            json={"product": data}
        )

        print("Shopify status code:", response.status_code)
        print("Shopify raw response:", response.text)

        try:
            shopify_json = response.json()
        except ValueError:
            shopify_json = {"error": "Invalid JSON from Shopify", "raw": response.text}

        if response.status_code == 201:
            return jsonify({"status": "success", "shopify": shopify_json})
        else:
            return jsonify({
                "status": "error",
                "shopify": shopify_json,
                "code": response.status_code
            }), response.status_code

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
