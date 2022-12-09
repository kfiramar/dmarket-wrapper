'''this module sends all API requests headers and encryptions'''
import json
from datetime import datetime
from nacl.bindings import crypto_sign
from common.config import SECRET_KEY, PUBLIC_KEY, SIGNATURE_PREFIX


def create_headers(url_endpoint: str, method: str, body: str) -> dict:
    '''this function creates the headers for the API requests'''
    nonce = str(round(datetime.now().timestamp()))
    string_to_sign = (method + url_endpoint + nonce) if not body else (method + url_endpoint + json.dumps(body) + nonce)
    encoded = string_to_sign.encode('utf-8')
    signature_bytes = crypto_sign(encoded, bytes.fromhex(SECRET_KEY))
    signature = signature_bytes[:64].hex()
    return {
        "X-Api-Key": PUBLIC_KEY,
        "X-Request-Sign": SIGNATURE_PREFIX + signature,
        "X-Sign-Date": nonce
    }
