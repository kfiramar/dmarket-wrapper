'''This module sends all the API requests'''
import requests
from api_encryption import create_headers, create_headers_w_body
from config import API_URL


def generic_request(api_url_path, method):
    '''This is the most generic API request function'''
    headers = create_headers(api_url_path, method=method)
    method_lower = method.lower()
    response = requests.__getattribute__(method_lower)(API_URL + api_url_path, headers=headers)
    return response

def generic_request_w_body(api_url_path, body, method):
    '''This is the most generic API request function with a body'''
    headers = create_headers_w_body(api_url_path, body=body, method=method)
    method_lower = method.lower()
    response = requests.__getattribute__(method_lower)(API_URL + api_url_path, json=body, headers=headers)
    return response

# def request_devider(api_url_path, method, amount,func, body = ''):
#     amount_array = []
#     if amount > 100:
#         for _ in range(amount/100):
#             amount_array.append(100)
#     amount_array.append(amount%100)
#     for number in amount_array:
#         response = func(api_url_path= api_url_path, method='POST', body=body)
