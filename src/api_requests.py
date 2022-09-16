from itertools import count
from operator import truediv
import time
import requests
from Item import *
from api_encryption import *

rootApiUrl = "https://api.dmarket.com"

def generic_request(api_url_path,method='GET'):
  headers = create_headers(api_url_path,method=method)
  method_lower = method.lower()
  response = requests.__getattribute__(method_lower)(rootApiUrl + api_url_path, headers=headers)
  #write_content(resp.json(),method)
  return response