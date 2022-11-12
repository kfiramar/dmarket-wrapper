
'''This module contains the main loop of the program and prints'''
from datetime import datetime
from importlib.metadata import requires

from pathlib import Path
import inspect
import copy
from types import NoneType
import click
from halo import Halo
from simple_chalk import chalk
from api_client.api_requests import (generic_request)
from common.config import (BALANCE_ENDPOINT, DM_INVENTORY_ENDPOINT, PURCHASE_HISTORY_ENDPOINT,
                    STEAM_INVENTORY_ENDPOINT, SELL_LISTINGS_ENDPOINT, LOGGING)
from table.tables.ListingTable import ListingTable
from table.tables.InventoryItemTable import InventoryItemTable
from table.tables.PurcheseTable import PurcheseTable
from table.print import print_table, print_table_w_date_headers
from common.logger import log, merge_dicts

func_name = Path(__file__).stem
api_spinner = Halo(text='Attempting to get your items', spinner='dots', animation='bounce', color='green')


@click.group()
def view():
    '''viewing listings, inventory -all, dm inventory and steam inventory'''



@click.command()
@click.option('--inventory_source', required = True, type=click.Choice(['dm', 'steam','all']), prompt=True, help='choose inventory_source: dm, steamm, all.')
def inventory(inventory_source: str):
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    print_table(copy.deepcopy(get_inventory(inventory_source)))
    api_spinner.succeed(text="Recived and pared API request")


@click.command()
def listings():
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    current_listings = get_listings()
    if not isinstance(current_listings.rows, NoneType):
        print_table(copy.deepcopy(current_listings.rows))
        api_spinner.succeed(text="Recived and pared API request")
    else:
        api_spinner.fail(text="There are ZERO items listed")



@click.command()
@click.option('--merge_by', default='day',type=click.Choice(['minute', 'hour', 'day', 'month', 'year']), help='a period of time which you want to merge your purcheses by.')
def purchases(merge_by: str):
    '''Prints the purchases history'''
    api_spinner.start()
    response = generic_request(api_url_path=f"{PURCHASE_HISTORY_ENDPOINT}", method='GET')
    purchase_rows = PurcheseTable.parse_jsons_to_table(response.json())
    api_spinner.succeed(text="Recived and pared API request")
    print_table_w_date_headers(copy.deepcopy(purchase_rows.rows), merge_by)
    if LOGGING == 'True':
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")


@click.command()
@click.option('--date', required=True, prompt=True, help='Date from which you want to see your purchase history (%Y-%m-%d).')
def purchases_from(date: str):
    '''Prints the purchases history'''
    date = datetime.strptime(date, '%d/%m/%Y')
    api_spinner.start()
    response = generic_request(api_url_path=f"{PURCHASE_HISTORY_ENDPOINT}", method='GET')
    purchase_rows = PurcheseTable.parse_jsons_to_purchese_table_from_date(response.json(), date)
    api_spinner.succeed(text="Recived and pared API request")
    print_table(copy.deepcopy(purchase_rows.rows))
    if LOGGING == 'True':
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")


def get_inventory(inventory_source: str):
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
    if LOGGING == 'True':
        log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
    return returned_rows


def get_listings():
    '''Prints all the listings on Dmarket'''
    response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if LOGGING == 'True':
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")
    if response.json()['Total'] != '0':
        # return parse_jsons_to_rows(response.json(), parse_jsons_to_listings,
        #                                     parse_listings_to_listingrows, 'total_price')
        return ListingTable.parse_jsons_to_table(response.json())

@click.command()
def balance():
    '''View your current Dmarket balance'''
    response = generic_request(api_url_path=BALANCE_ENDPOINT, method='GET')
    click.echo(chalk.cyan('Your DMarket balance: ' + str(float(response.json()['usd'])/100) + '$'))
    if LOGGING == 'True':
        log(response.json(), f"{func_name}_{inspect.stack()[0][3]}")


view.add_command(inventory)
view.add_command(listings)
view.add_command(balance)
view.add_command(purchases)
view.add_command(purchases_from)


if __name__ == '__main__':
    view()
