import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.environ["PAYPAL_BASE_URL"]
client_id = os.environ["PAYPAL_CLIENT_ID"]
client_secret = os.environ["PAYPAL_CLIENT_SECRET"]

response = requests.post(
    f"{base_url}/v1/oauth2/token",
    auth=(client_id, client_secret),
    data={"grant_type": "client_credentials"},
    headers={"Accept": "application/json"},
    timeout=30,
)

if not response.ok:
    print("HTTP status:", response.status_code)
    print("PayPal error:", response.json().get("error", "unknown"))
    raise SystemExit("Token request failed; check credentials and configuration.")

data = response.json()

print("OAuth successful!")
print("Token type:", data.get("token_type"))
print("Expires in (seconds):", data.get("expires_in"))
print("Access token received:", bool(data.get("access_token")))
print("Scope returned:", bool(data.get("scope")))