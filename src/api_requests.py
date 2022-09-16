import requests
from api_encryption import create_headers

rootApiUrl = "https://api.dmarket.com"

def generic_request(api_url_path,method='GET'):
  headers = create_headers(api_url_path,method=method)
  method_lower = method.lower()
  response = requests.__getattribute__(method_lower)(rootApiUrl + api_url_path, headers=headers)
  #write_content(resp.json(),method)
  return response

# Creates a file and loads all the API request result into it
def write_content(content,method):
  #f = open(os.path.join(f'',time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S"),"x"))
  f = open(time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S"),"x")
  f.write(str(content))