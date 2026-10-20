import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.environ["PAYPAL_BASE_URL"].rstrip("/")
client_id = os.environ["PAYPAL_CLIENT_ID"]
client_secret = os.environ["PAYPAL_CLIENT_SECRET"]

# Get an access token
token_response = requests.post(
    f"{base_url}/v1/oauth2/token",
    auth=(client_id, client_secret),
    data={"grant_type": "client_credentials"},
    headers={"Accept": "application/json"},
    timeout=30,
)
print("Token HTTP status:", token_response.status_code)
token_response.raise_for_status()
access_token = token_response.json()["access_token"]

# Check the order
order_id = input("Paste the new PayPal Order ID: ").strip()

order_response = requests.get(
    f"{base_url}/v2/checkout/orders/{order_id}",
    headers={"Authorization": f"Bearer {access_token}"},
    timeout=30,
)

print("Order HTTP status:", order_response.status_code)

data = order_response.json()
print("Order status:", data.get("status"))
print("Intent:", data.get("intent"))
print("Purchase units:", len(data.get("purchase_units", [])))
units = data.get("purchase_units", [])

if units:
    print("Payee email:", units[0].get("payee", {}).get("email_address", "Not provided"))
    print("Amount:", units[0].get("amount", {}).get("value"))
    print("Currency:", units[0].get("amount", {}).get("currency_code"))

if not order_response.ok:
    print("PayPal error name:", data.get("name", "unknown"))
    print("PayPal error message:", data.get("message", "unknown"))