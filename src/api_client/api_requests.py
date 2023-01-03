'''This module sends all the API aiohttp'''
import aiohttp
import asyncio
import requests
from api_client.api_encryption import create_headers
from common.config import API_URL, SPINNER_CONF



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


async def request_devider(url_endpoint: str, method: str, amount: int, price: str, row) -> list:
    '''splits aiohttp to up to 100 items per request'''
    # Divide the amount into chunks of up to 100 items
    amount_array = devide_number_to_array(amount, divisor=100)
    
    # Create an HTTP session
    async with aiohttp.ClientSession() as session:
        # Create a task group to track the tasks
        async with asyncio.TaskGroup() as tg:
            # Create a task for each chunk of items
            tasks = [
                tg.create_task(
                    async_generic_request(url_endpoint=url_endpoint,
                                          method=method,
                                          session=session,
                                          body=row.change_state_body(number, price)))
                for number in amount_array
            ]
        # Wait for all the tasks to be completed and store the results in a list
        response_contents = [await (await task).json() for task in tasks]
        # response_contents = await asyncio.gather(*[result.json() for result in await asyncio.gather(*tasks)])
    return response_contents


def devide_number_to_array(number: int, divisor: int) -> list:
    '''devides the number by x and creates a list of x with leftovers'''
    quotient, remainder = divmod(number, divisor)
    amount_array = [divisor] * quotient
    if remainder:
        amount_array.append(remainder)

    return amount_array
