import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "PAYPAL_BASE_URL",
    "https://api-m.sandbox.paypal.com"
).rstrip("/")

CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError(
            "Missing PAYPAL_CLIENT_ID or PAYPAL_CLIENT_SECRET in .env"
        )

    # Step 1: Get an OAuth access token
    token_response = requests.post(
        f"{BASE_URL}/v1/oauth2/token",
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
        data={"grant_type": "client_credentials"},
        timeout=30,
    )

    print("Token HTTP status:", token_response.status_code)

    if not token_response.ok:
        print("Token error:", token_response.text)
        return

    access_token = token_response.json()["access_token"]

    # Step 2: Create a fresh Sandbox order
    order_payload = {
        "intent": "CAPTURE",
        "application_context": {
            "return_url": "https://example.com/paypal/return",
            "cancel_url": "https://example.com/paypal/cancel",
        },
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "1.00",
                }
            }
        ],
    }

    order_response = requests.post(
        f"{BASE_URL}/v2/checkout/orders",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json=order_payload,
        timeout=30,
    )

    print("Order HTTP status:", order_response.status_code)

    if not order_response.ok:
        print("Order error:", order_response.text)
        return

    order = order_response.json()

    print("Order ID:", order.get("id"))
    print("Order status:", order.get("status"))

    # Step 3: Find the buyer approval link
    approval_url = next(
        (
            link["href"]
            for link in order.get("links", [])
            if link.get("rel") in ("approve", "payer-action")
        ),
        None,
    )

    if approval_url:
        print("\nOpen this NEW approval URL in your browser:\n")
        print(approval_url)
    else:
        print("\nNo approval link was returned.")
        print("Returned links:", order.get("links", []))


if __name__ == "__main__":
    main()