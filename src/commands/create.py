'''This module contains the main loop of the program and prints'''

from pathlib import Path
import inspect
import copy
import click
from simple_chalk import chalk
from halo import Halo
from api_client.api_requests import request_devider
from common.config import ATTEMPTING_GET_ITEMS, BUY_ORDER_ENDPOINT, CREATE_LISTINGS_AMOUNT, CREATE_LISTINGS_PRICE, LOGGING, CREATE_LISTINGS_ITEMS, SUCCESSFULLY_CREATED, UNSUCSESSFULLY_CREATED
from items.ListingItem import listing_error_parsing
from commands.view import get_inventory
from table.print import print_table
from api_client.request_body import create_listing_body
from common.logger import log, merge_dicts

func_name = Path(__file__).stem
items_api_spinner = Halo(text=ATTEMPTING_GET_ITEMS, spinner='dots', animation='bounce', color='green')
create_api_spinner = Halo(text='Attempting to create', spinner='dots', animation='bounce', color='green')


@click.group()
def create():
    '''creating listings'''


@click.command()
def listing():
    '''Creates listing on Dmarket'''
    dm_rows = get_inventory(inventory_source='dm')
    print_table(copy.deepcopy(dm_rows))
    row_number = click.prompt(CREATE_LISTINGS_ITEMS.format(len(dm_rows) - 1))
    choosen_row = (vars(dm_rows[int(row_number)]))
    amount = click.prompt(CREATE_LISTINGS_AMOUNT.format(choosen_row["total_items"]))
    price = click.prompt(CREATE_LISTINGS_PRICE.format(choosen_row["market_price"]))
    create_api_spinner.start()
    responses = request_devider(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=int(amount), body_func=create_listing_body, price=price, asset_ids=choosen_row["asset_ids"])
    error_list = listing_error_parsing(responses)
    if len(error_list) == 0:
        create_api_spinner.succeed(text=SUCCESSFULLY_CREATED.format(amount, choosen_row['title']))
    else:
        create_api_spinner.fail(text=UNSUCSESSFULLY_CREATED.format(error_list, amount))
    if LOGGING:
        log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")


create.add_command(listing)


if __name__ == '__main__':
    create()
