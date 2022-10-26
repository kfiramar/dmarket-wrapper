'''This module sends all the API requests'''
from typing import Callable
import requests
from api_client.api_encryption import create_headers, create_headers
from common.config import API_URL


def generic_request(api_url_path: str, method: str) -> requests.models.Response:
    '''This is the most generic API request function'''
    headers = create_headers(api_url_path, method=method)
    response = getattr(requests, method.lower())(API_URL + api_url_path, headers=headers)
    return response


def generic_request_w_body(api_url_path: str, body: str, method: str) -> requests.models.Response:
    '''This is the most generic API request function with a body'''
    headers = create_headers(api_url_path, body=body, method=method)
    response = getattr(requests, method.lower())(API_URL + api_url_path, json=body, headers=headers)
    return response


def request_devider_listing(api_url_path: str, method: str, amount: int, body_func: Callable, price: str, asset_ids: list, offer_ids: list) -> list:
    '''splits requests to up to 100 items per request'''
    amount_array = split_to_100s(amount)
    responses = [generic_request_w_body(api_url_path=api_url_path, method=method, body=body_func(number, price, asset_ids, offer_ids)) for number in amount_array]
    return responses


def request_devider_buy_order(api_url_path: str, method: str, amount: int, body_func: Callable, price: str, asset_ids: list) -> list:
    '''splits requests to up to 100 items per request'''
    amount_array = split_to_100s(amount)
    responses = [generic_request_w_body(api_url_path=api_url_path, method=method, body=body_func(number, price, asset_ids)) for number in amount_array]
    return responses


def split_to_100s(number: int) -> list:
    '''devides the number by 100 and creates a list of 100s with leftovers'''
    amount_array = [100]*int(number/100)
    amount_array.append(number % 100)
    return amount_array
