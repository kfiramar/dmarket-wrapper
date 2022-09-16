'''This module sends all the API requests'''
import requests
from api_encryption import create_headers

API_URL = "https://api.dmarket.com"


def generic_request(api_url_path, method='GET'):
    '''This is the most generic API request function'''
    headers = create_headers(api_url_path, method=method)
    method_lower = method.lower()
    response = requests.__getattribute__(method_lower)(API_URL + api_url_path, headers=headers)
    # write_content(resp.json(),method)
    return response


# Creates a file and loads all the API request result into it
def write_content(content, method):
    '''debugging if you recive JSON and not sure how to handle it'''
    # f = open(os.path.join(f'',time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S"),"x"))
    file = open(time.strftime(f"{method}_request_%Y-%m-%d_%H:%M:%S"),"x")
    file.write(str(content))
