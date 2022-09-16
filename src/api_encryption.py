'''asdfasf'''
from datetime import datetime
from nacl.bindings import crypto_sign


# replace with your api keys
PUBLIC_KEY = "1e198fb8b17faad422b1c2780b2b8b4e9725e5785500589966c1e26790a71a44"
SECRET_KEY = "26fcde3e6fe0f98c9751a629a71e798d77bb001d2235fda86f8bc5f3af41b1661e198fb8b17faad422b1c2780b2b8b4e9725e5785500589966c1e26790a71a44"

# DMarket signature prefix
SIGNATURE_PREFIX = "dmar ed25519 "


def create_headers(api_url_path, method, body=''):
    '''sdasdads'''
    nonce = str(round(datetime.now().timestamp()))
    # string_to_sign = method + api_url_path + json.dumps(body) + nonce
    string_to_sign = method + api_url_path + nonce
    encoded = string_to_sign.encode('utf-8')
    signature_bytes = crypto_sign(encoded, bytes.fromhex(SECRET_KEY))
    signature = signature_bytes[:64].hex()
    return {
        "X-Api-Key": PUBLIC_KEY,
        "X-Request-Sign": SIGNATURE_PREFIX + signature,
        "X-Sign-Date": nonce
    }
