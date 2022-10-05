'''This module contains the main loop of the program and prints'''
from typing import List
import sys
import inspect
import click
import copy
from tabulate import tabulate
import numpy as np
from api_requests import (generic_request, request_devider_buy_order, request_devider_listing)
from config import (BUY_ORDER_ENDPOINT, BALANCE_ENDPOINT, INVENTORY_ENDPOINT,
                    SELL_LISTINGS_ENDPOINT, DELETE_LISTING_ENDPOINT, LOGGING)
from parsing import (listing_error_parsing, parse_jsons_to_listings,
                     parse_jsons_to_inventoryitems, parse_listings_to_listingrows,
                     buy_order_body, write_content, listings_body, merge_dicts,
                     parse_inventoryitems_to_inventoryitemrow)
from row import (InventoryItemRow, ListingRow)
from commands.view import view
from commands.delete import delete
from commands.create import create


@click.group()
def commands():
    pass


commands.add_command(view)
commands.add_command(delete)
commands.add_command(create)

if __name__ == '__main__':
    commands()
