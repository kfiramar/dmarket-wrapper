'''This module sends all the API requests'''
from typing_extensions import assert_type
import requests
# import substitute
import math
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

def request_devider(api_url_path, method, amount,body_func, price, asset_ids, offer_ids):
    '''splits requests to up to 100 items per request'''
    amount_array = []
    responses = []
    if amount > 100:
        for _ in range(math.floor(amount/100)):
            amount_array.append(100)
    amount_array.append(amount%100)
    for number in amount_array:
        if (body_func.__name__ == 'listings_body'):
            response = generic_request_w_body(api_url_path= api_url_path, method=method, body=body_func(number, price, asset_ids,offer_ids))
        else:
            response = generic_request_w_body(api_url_path= api_url_path, method=method, body=body_func(number, price, asset_ids))
        responses.append(response)
    return responses
