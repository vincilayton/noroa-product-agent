import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
SHOPIFY_STORE = os.getenv("SHOPIFY_STORE")

@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.json
    payload = {
        "product": {
            "title": data["title"],
            "body_html": data.get("body_html", ""),
            "vendor": data.get("vendor", "Noroa"),
            "variants": [{"price": data["price"]}],
            "images": [{"src": data["image_url"]}]
        }
    }
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }
    url = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/2024-01/products.json"
    res = requests.post(url, json=payload, headers=headers)
    return jsonify(res.json())

