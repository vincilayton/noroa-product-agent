import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

SHOPIFY_API_URL = os.getenv("SHOPIFY_ADMIN_URL")  # e.g. https://yourstore.myshopify.com/admin/api/2023-10
SHOPIFY_TOKEN = os.getenv("SHOPIFY_TOKEN")

HEADERS = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_TOKEN
}

def get_recent_products(hours=48):
    since = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"
    url = f"{SHOPIFY_API_URL}/products.json?published_status=published&created_at_min={since}&limit=250"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"❌ Failed to fetch products: {res.text}")
        return []
    return res.json().get("products", [])

def get_orders():
    since = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
    url = f"{SHOPIFY_API_URL}/orders.json?status=any&created_at_min={since}&limit=250"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print(f"❌ Failed to fetch orders: {res.text}")
        return []
    return res.json().get("orders", [])

def build_sales_lookup(orders):
    sales_count = {}
    for order in orders:
        for item in order.get("line_items", []):
            product_id = item.get("product_id")
            if product_id:
                sales_count[product_id] = sales_count.get(product_id, 0) + 1
    return sales_count

def unpublish_product(product_id):
    url = f"{SHOPIFY_API_URL}/products/{product_id}.json"
    data = {
        "product": {
            "id": product_id,
            "published": False
        }
    }
    res = requests.put(url, json=data, headers=HEADERS)
    if res.status_code == 200:
        print(f"✅ Unpublished product {product_id}")
    else:
        print(f"❌ Failed to unpublish product {product_id}: {res.text}")

def run_auto_remove():
    products = get_recent_products()
    orders = get_orders()
    sales_lookup = build_sales_lookup(orders)

    print(f"🔍 Checking {len(products)} products published in the last 48 hours...")
    
    for product in products:
        product_id = product["id"]
        sales = sales_lookup.get(product_id, 0)

        if sales == 0:
            unpublish_product(product_id)
        else:
            print(f"🟢 Product {product_id} has {sales} sale(s) — kept published.")

if __name__ == "__main__":
    run_auto_remove()
