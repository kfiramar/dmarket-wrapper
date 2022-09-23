import json
from datetime import datetime

from nacl.bindings import crypto_sign
import requests

# replace with your api keys
public_key = "875dad0a1a7c2bf9146f24aa82cc51a6f54eb389d73342d61475b624a21575d2"
secret_key = "95bf02a93d0243ccfd234117c5005bf20767896b874ad226e37d4392c68629b3875dad0a1a7c2bf9146f24aa82cc51a6f54eb389d73342d61475b624a21575d2"

# change url to prod
rootApiUrl = "https://api.dmarket.com"


def get_offer_from_market():
    market_response = requests.get(rootApiUrl + "/exchange/v1/market/items?gameId=a8db&limit=1&currency=USD")
    offers = json.loads(market_response.text)["objects"]
    return offers[0]


def build_target_body_from_offer(offer):
    return {"targets": [
        {"amount": 1, "gameId": offer["gameId"], "price": {"amount": "2", "currency": "USD"},
         "attributes": {"gameId": offer["gameId"],
                        "categoryPath": offer["extra"]["categoryPath"],
                        "title": offer["title"],
                        "name": offer["title"],
                        "image": offer["image"],
                        "ownerGets": {"amount": "1", "currency": "USD"}}}
    ]}


def buy_order_body(amount, price):
    '''lksjdhflasj'''
    item_order = {"Offers": [
                {
                    "AssetID": "string",
                    "Price": {
                            "Currency": "string",
                            "Amount": price
                            }
                }
            ]}
    for i in range(amount-1):
        item_order['Offers'].append(item_order['Offers'][0])
    return json.dumps(item_order)


nonce = str(round(datetime.now().timestamp()))
api_url_path = "/exchange/v1/target/create"
method = "POST"
offer_from_market = get_offer_from_market()
body = build_target_body_from_offer(offer_from_market)
string_to_sign = method + api_url_path + json.dumps(body) + nonce
signature_prefix = "dmar ed25519 "
encoded = string_to_sign.encode('utf-8')
secret_bytes = bytes.fromhex(secret_key)
signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
signature = signature_bytes[:64].hex()
headers = {
    "X-Api-Key": public_key,
    "X-Request-Sign": signature_prefix + signature,
    "X-Sign-Date": nonce
}

resp = requests.post(rootApiUrl + api_url_path, json=body, headers=headers)
print(resp.text)