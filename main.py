from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Add to Shopify
    product_payload = {
        "product": {
            "title": data['title'],
            "body_html": data['body_html'],
            "vendor": data['vendor'],
            "product_type": data['product_type'],
            "variants": [
                {
                    "price": data['price']
                }
            ]
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": os.getenv("SHOPIFY_TOKEN")
    }

    shopify_url = f"https://{os.getenv('SHOPIFY_DOMAIN')}/admin/api/2023-10/products.json"
    response = requests.post(shopify_url, headers=headers, json=product_payload)

    return jsonify({
        "status": "sent to Shopify",
        "shopify_response": response.json()
    })
