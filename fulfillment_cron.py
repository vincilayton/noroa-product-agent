import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

SHOPIFY_ADMIN_URL = os.getenv("SHOPIFY_ADMIN_URL")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")
EMAIL_WEBHOOK_URL = os.getenv("EMAIL_WEBHOOK_URL")  # e.g., Formsubmit or Zapier

def fetch_orders():
    url = f"{SHOPIFY_ADMIN_URL}/orders.json?status=unfulfilled"
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": SHOPIFY_TOKEN
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("orders", [])
    return []

def extract_order_info(order):
    line_items = []
    for item in order["line_items"]:
        line_items.append(f"- {item['quantity']}x {item['title']}")

    return {
        "order_id": order["id"],
        "customer": order["customer"]["first_name"] + " " + order["customer"]["last_name"],
        "email": order["email"],
        "address": order["shipping_address"],
        "items": line_items
    }

def format_email_body(order_info):
    address = order_info["address"]
    full_address = f"{address['address1']}, {address['city']}, {address['province_code']} {address['zip']}, {address['country_code']}"

    body = f"""
New Order Received 🚀

Customer: {order_info['customer']}
Email: {order_info['email']}
Shipping Address: {full_address}

Items:
{chr(10).join(order_info['items'])}

Order ID: {order_info['order_id']}
    """
    return body.strip()

def send_email(content):
    data = {
        "subject": "New Order for Fulfillment",
        "message": content
    }
    response = requests.post(EMAIL_WEBHOOK_URL, data=data)
    print("Email sent:", response.status_code, response.text)

def main():
    orders = fetch_orders()
    if not orders:
        print("No unfulfilled orders found.")
        return

    for order in orders:
        info = extract_order_info(order)
        email_content = format_email_body(info)
        send_email(email_content)

if __name__ == "__main__":
    main()
