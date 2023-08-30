from base64 import b64encode

import requests
from django.conf import settings

from .constants import PAYPAL_URL

clientId = settings.PAYPAL_CLIENT_ID
secret = settings.PAYPAL_CLIENT_SECRET

def create_order(price):
    token = generate_auth_token()

    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {token}"
    }
    body = {
      "intent": "CAPTURE",
      "purchase_units": [
        {
          "amount": {
            "currency_code": "USD",
            "value": str(int(float(price))),
          },
        },
      ],
    }
    response = requests.post(f"{PAYPAL_URL}/v2/checkout/orders", headers=headers, json=body)

    return response.json()

def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

def generate_auth_token():
    url = f"{PAYPAL_URL}/v1/oauth2/token"

    payload = 'grant_type=client_credentials'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': basic_auth(clientId,secret)}

    response = requests.post(url, headers=headers, data=payload)

    return response.json()["access_token"]

def capture_order(id):
    token = generate_auth_token()
    url = f"{PAYPAL_URL}/v2/checkout/orders/{id}/capture"
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    return response.json()
