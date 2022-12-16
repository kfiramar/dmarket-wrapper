'''This module sends all the API aiohttp'''
import aiohttp
import asyncio
import click
import requests
from typing import Callable, List, Optional, Union
from api_client.api_encryption import create_headers
from common.config import API_URL, SPINNER_CONF
from table.rows.dmarket_item_row import DMarketItemRow
from table.rows.inventory_item_row import InventoryItemRow
from table.rows.listing_row import ListingRow



def generic_request(url_endpoint: str, method: str, session=requests.Session(), body: str = None):
    '''This is the most generic API request function with a body'''
    headers = create_headers(url_endpoint, body=body, method=method)
    response = session.request(method.lower(), API_URL + url_endpoint, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


async def async_generic_request(url_endpoint: str, method: str, session=aiohttp.ClientSession(), body: str = None):
    '''This is the most generic API request function with a body'''
    headers = create_headers(url_endpoint, body=body, method=method)
    response = await session.request(method.lower(), API_URL + url_endpoint, json=body, headers=headers, raise_for_status=True)
    return response


async def request_devider(
    url_endpoint: str,
    method: str,
    amount: int,
    price: str,
    row: Union[DMarketItemRow, InventoryItemRow, ListingRow],
    session: aiohttp.ClientSession,
) -> list:
    """Splits aiohttp requests to up to 100 items per request."""
    amount_array = devide_number_to_array(amount, divisor=100)
    async with asyncio.TaskGroup() as tasks:
        tasks = [
            tasks.create_task(
                generic_request(
                    url_endpoint=url_endpoint,
                    method=method,
                    session=session,
                    body=create_body(row, number, price),
                )
            )
            for number in amount_array
        ]
        results = [await (await task) for task in asyncio.as_completed(tasks)]
    return results


def create_body(
    row: Union[DMarketItemRow, InventoryItemRow, ListingRow],
    number: int,
    price: str,
) -> Optional[dict]:
    """Creates the body for the API request based on the type of row."""
    if isinstance(row, InventoryItemRow):
        return row.create_listing_json_body(number, price)
    elif isinstance(row, ListingRow):
        return row.delete_listing_json_body(number, price)
    elif isinstance(row, DMarketItemRow):
        return row.create_target_body(number, price)


def devide_number_to_array(number: int, divisor: int) -> list:
    '''devides the number by x and creates a list of x with leftovers'''
    quotient, remainder = divmod(number, divisor)
    amount_array = [divisor] * quotient
    if remainder:
        amount_array.append(remainder)

    return amount_array
