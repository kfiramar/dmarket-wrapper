
'''This module contains the main loop of the program and prints'''
from datetime import datetime
from pathlib import Path
import inspect
from types import NoneType
import click
from halo import Halo
from api_client.api_requests import (generic_request)
from common.config import (BALANCE_ENDPOINT, DM_INVENTORY_ENDPOINT, PURCHASE_HISTORY_ENDPOINT,
                    STEAM_INVENTORY_ENDPOINT, SELL_LISTINGS_ENDPOINT, LOGGING, RECIVED_ITEMS, LISTING_ZERO_ITEMS, BALANCE_TEXT, ATTEMPTING_GET_ITEMS )
from common.logger import log, merge_dicts
from table.tables.listing_table import ListingTable
from table.tables.inventory_item_table import InventoryItemTable
from table.tables.purchese_table import PurcheseTable
from table.print import print_table, print_table_with_date_headers


func_name = Path(__file__).stem
api_spinner = Halo(text=ATTEMPTING_GET_ITEMS, spinner='dots', animation='bounce', color='green')


@click.group()
def view() -> None:
    '''viewing listings, inventory -all, dm inventory and steam inventory'''


@click.command()
@click.option('--inventory_source', required = True, type=click.Choice(['dm', 'steam','all']), prompt=True, help='choose inventory_source: dm, steamm, all.')
def inventory(inventory_source: str) -> None:
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    print_table(get_inventory(inventory_source))
    api_spinner.succeed(text=RECIVED_ITEMS)


@click.command()
def listings() -> None:
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    current_listings = get_listings()
    if not isinstance(current_listings, NoneType):
        print_table(current_listings.rows)
        api_spinner.succeed(text=RECIVED_ITEMS)
    else:
        api_spinner.fail(text=LISTING_ZERO_ITEMS)


@click.command()
@click.option('--merge_by', default='day',type=click.Choice(['minute', 'hour', 'day', 'month', 'year']), help='a period of time which you want to merge your purcheses by.')
def purchases(merge_by: str) -> None:
    '''Prints the purchases history'''
    api_spinner.start()
    response = generic_request(api_url_path=f"{PURCHASE_HISTORY_ENDPOINT}", method='GET')
    purchase_rows = PurcheseTable.parse_jsons_to_table(response.json())
    api_spinner.succeed(text=RECIVED_ITEMS)
    print_table_with_date_headers(purchase_rows.rows, merge_by)
    if LOGGING:
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")


@click.command()
@click.option('--date', required=True, prompt=True, help='Date from which you want to see your purchase history (%d/%m/%Y).')
def purchases_from(date: str) -> None:
    '''Prints the purchases history'''
    date = datetime.strptime(date, '%d/%m/%Y')
    api_spinner.start()
    response = generic_request(api_url_path=f"{PURCHASE_HISTORY_ENDPOINT}", method='GET')
    purchase_rows = PurcheseTable.parse_jsons_to_purchese_table_from_date(response.json(), date)
    api_spinner.succeed(text=RECIVED_ITEMS)
    print_table(purchase_rows.rows)
    if LOGGING:
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")


def get_inventory(inventory_source: str) -> list:
    '''Prints all of your inventory'''
    returned_rows, responses = [], []
    if inventory_source in ('dm', 'all'):
        dm_response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
        dm_rows = InventoryItemTable.parse_jsons_to_table(dm_response.json())
        returned_rows.extend(dm_rows.rows)
        responses.append(dm_response)
    if inventory_source in ('steam', 'all'):
        steam_response = generic_request(api_url_path=STEAM_INVENTORY_ENDPOINT, method='GET')
        steam_rows = InventoryItemTable.parse_jsons_to_table(steam_response.json())
        returned_rows.extend(steam_rows.rows)
        responses.append(steam_response)
    if LOGGING:
        log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
    return returned_rows


def get_listings() -> None:
    '''Prints all the listings on Dmarket'''
    response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if LOGGING:
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")
    return ListingTable.parse_jsons_to_table(response.json())



@click.command()
def balance() -> None:
    '''View your current Dmarket balance'''
    response = generic_request(api_url_path=BALANCE_ENDPOINT, method='GET')
    click.echo(BALANCE_TEXT.format(str(float(response.json()['usd'])/100)))
    if LOGGING:
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")


view.add_command(inventory)
view.add_command(listings)
view.add_command(balance)
view.add_command(purchases)
view.add_command(purchases_from)


if __name__ == '__main__':
    view()
