'''This module sends all the API requests'''
import requests
from api_encryption import create_headers, create_headers_w_body

API_URL = "https://api.dmarket.com"


def generic_request(api_url_path, method='GET'):
    '''This is the most generic API request function'''
    headers = create_headers(api_url_path, method=method)
    method_lower = method.lower()
    response = requests.__getattribute__(method_lower)(API_URL + api_url_path, headers=headers)
    return response

def generic_request_w_body(api_url_path, body, method='GET'):
    '''This is the most generic API request function with a body'''
    headers = create_headers_w_body(api_url_path, body=body, method=method)
    method_lower = method.lower()
    response = requests.__getattribute__(method_lower)(API_URL + api_url_path, json=body, headers=headers)
    return response
