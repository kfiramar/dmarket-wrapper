from datetime import datetime
from nacl.bindings import crypto_sign
from Item import *


# replace with your api keys
public_key = "875dad0a1a7c2bf9146f24aa82cc51a6f54eb389d73342d61475b624a21575d2"
secret_key = "95bf02a93d0243ccfd234117c5005bf20767896b874ad226e37d4392c68629b3875dad0a1a7c2bf9146f24aa82cc51a6f54eb389d73342d61475b624a21575d2"


def create_headers(api_url_path, method, body=''):
  nonce = str(round(datetime.now().timestamp()))
  # string_to_sign = method + api_url_path + json.dumps(body) + nonce
  string_to_sign = method + api_url_path + nonce
  encoded = string_to_sign.encode('utf-8')
  signature_bytes = crypto_sign(encoded, bytes.fromhex(secret_key))
  signature = signature_bytes[:64].hex()
  return {
      "X-Api-Key": public_key,
      "X-Request-Sign": signature_prefix + signature,
      "X-Sign-Date": nonce
  }