'''This module sends all the API requests'''
import time
import asyncio
import click
from typing import Callable
import requests
from api_client.api_encryption import create_headers, create_headers
from common.config import API_URL
from table.rows.dmarket_item_row import DMarketItemRow
from table.rows.inventory_item_row import InventoryItemRow
from table.rows.listing_row import ListingRow


def generic_request(url_endpoint: str, method:str, body: str = None) -> requests.models.Response:
    '''This is the most generic API request function with a body'''
    headers = create_headers(url_endpoint, method, body=body)
    response = getattr(requests, method.lower())(API_URL + url_endpoint, json=body, headers=headers)
    response.raise_for_status()
    return response


def session_generic_request(url_endpoint: str, method: str, session, body: str = None) -> requests.models.Response:
    '''This is the most generic API request function with a body'''
    headers = create_headers(url_endpoint, body=body, method=method)
    response = getattr(session, method.lower())(API_URL + url_endpoint, json=body, headers=headers)
    response.raise_for_status()
    return response


# def request_devider(url_endpoint: str, method: str, amount: int, body_func: Callable, price: str,asset_ids: list = None,  offer_ids: list = None, title: str = None) -> list:
#     '''splits requests to up to 100 items per request'''
#     loop = asyncio.get_event_loop
#     amount_array = devide_number_to_array(amount, devider= 100)
#     responses =  [generic_request(url_endpoint=url_endpoint, method=method, body=body_func(number, price, asset_ids, offer_ids)) for number in amount_array] \
#             if offer_ids else \
#                  [generic_request(url_endpoint=url_endpoint, method=method, body=body_func(number, price, asset_ids)) for number in amount_array] \
#             if asset_ids else \
#                  [generic_request(url_endpoint=url_endpoint, method=method, body=body_func(number, price, title)) for number in amount_array]
#     return responses
    #How to inplement it generically?
    
     
async def async_generic_request(url_endpoint: str, method: str, body: str = None) -> requests.models.Response:
    '''This is the most generic API request function with a body'''
    headers = create_headers(url_endpoint, body=body, method=method)
    response = await getattr(requests, method.lower())(API_URL + url_endpoint, json=body, headers=headers)
    response.raise_for_status()
    return response


def request_devider(url_endpoint: str, method: str, amount: int, price: str, row) -> list:
    '''splits requests to up to 100 items per request'''
    start = time.time()
    # loop = asyncio.get_event_loop
    amount_array = devide_number_to_array(amount, devider= 100)
    with requests.Session() as session:
        responses = [session_generic_request(url_endpoint=url_endpoint, method=method, session=session, body=create_body(row, number, price)) for number in amount_array]
        # responses = [generic_request(url_endpoint=url_endpoint, method=method, body=create_body(row, number, price)) for number in amount_array]
    timee = time.time() - start
    print(timee)
    click.echo("banana")
    return responses
    #How to inplement it generically?

 
def create_body(row, number, price):
    body = None
    if isinstance(row, InventoryItemRow):
        body = row.create_listing_json_body(number, price)
    elif isinstance(row, ListingRow):
        body = row.delete_listing_json_body(number, price)
    elif isinstance(row, DMarketItemRow):
        body = row.create_target_body(number, price)
    return body

def devide_number_to_array(number: int, devider: int) -> list:
    '''devides the number by 100 and creates a list of 100s with leftovers'''
    amount_array = [devider]*int(number/devider)
    amount_array.append(number % devider)
    return amount_array
