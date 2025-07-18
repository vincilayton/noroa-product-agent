from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Noroa Agent is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Example response
    return jsonify({"status": "received", "data": data})

@app.route("/add_product", methods=["POST"])
def add_product():
    data = request.get_json()

    product_data = {
        "product": {
            "title": data.get("title"),
            "body_html": data.get("body_html"),
            "vendor": data.get("vendor"),
            "product_type": data.get("product_type"),
            "variants": [
                {
                    "price": data.get("price")
                }
            ]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": os.getenv("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
    }

    response = requests.post(
        f"{os.getenv('SHOPIFY_ADMIN_URL')}/products.json",
        headers=headers,
        data=json.dumps(product_data)
    )

    return jsonify(response.json())
if __name__ == "__main__":
    app.run(debug=True)
