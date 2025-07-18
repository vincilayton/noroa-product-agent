from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_URL = os.getenv("SHOPIFY_API_URL")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("Received data:", data)

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": SHOPIFY_TOKEN
        }

        response = requests.post(
            f"{SHOPIFY_API_URL}/products.json",
            headers=headers,
            json={"product": data}
        )

        print("Shopify response:", response.text)

        if response.status_code == 201:
            return jsonify({"status": "success", "shopify": response.json()})
        else:
            return jsonify({
                "status": "error",
                "shopify": response.json(),
                "code": response.status_code
            }), response.status_code

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
