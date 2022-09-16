import json
from datetime import datetime
from nacl.bindings import crypto_sign
import requests

# replace with your api keys
public_key = "875dad0a1a7c2bf9146f24aa82cc51a6f54eb389d73342d61475b624a21575d2"
secret_key = "95bf02a93d0243ccfd234117c5005bf20767896b874ad226e37d4392c68629b3875dad0a1a7c2bf9146f24aa82cc51a6f54eb389d73342d61475b624a21575d2"

# change url to prod
rootApiUrl = "https://api.dmarket.com"

#DMarket signature prefix
signature_prefix = "dmar ed25519 "


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


def inventory_request():
  api_url_path = "/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=1"
  headers = create_headers(api_url_path)
  resp = requests.get(rootApiUrl + api_url_path, headers=headers)
  write_content('response.txt',resp.json())
  
  
def generic_request(api_url_path,method='GET'):
  headers = create_headers(api_url_path,method=method)
  method_lower = method.lower()
  resp = requests.__getattribute__(method_lower)(rootApiUrl + api_url_path, headers=headers)
  write_content('response.txt',resp.json())
  

def write_content(file_name,content):
  f = open(file_name,"w")
  f.write(str(content['Items']))
  
if __name__ == '__main__':
  generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=1",method='GET')