
'''This module contains the main loop of the program and prints'''
from datetime import datetime
import os
import inspect
import copy
import click
from halo import Halo
from simple_chalk import chalk
from api_client.api_requests import (generic_request)
from common.config import (BALANCE_ENDPOINT, DM_INVENTORY_ENDPOINT, PURCHASE_HISTORY_ENDPOINT,
                    STEAM_INVENTORY_ENDPOINT, SELL_LISTINGS_ENDPOINT, LOGGING)
from common.parsing import (parse_jsons_to_listings, parse_jsons_to_inventoryitems, parse_jsons_to_purcheserows,
                     parse_listings_to_listingrows,
                     parse_inventoryitems_to_inventoryitemrow, parse_jsons_to_rows,
                     parse_jsons_to_purchases, parse_purchases_to_purcheserows_by_date, parse_purchases_to_purcheserows_merge)
from table.print import print_table, print_table_w_date_headers
from common.logger import log, merge_dicts


api_spinner = Halo(text='Attempting to get your items', spinner='dots', animation='bounce', color='green')


@click.group()
def view():
    '''viewing listings, inventory -all, dm inventory and steam inventory'''


@click.command()
def dm_inventory():
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
    dm_rows = parse_jsons_to_rows(response.json(), parse_jsons_to_inventoryitems,
                                  parse_inventoryitems_to_inventoryitemrow, 'total_price')
    api_spinner.succeed(text="Recived and pared API request")
    print_table(copy.deepcopy(dm_rows))
    if LOGGING == 'True':
        log(response.json(), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")


@click.command()
@click.option('--merge_by', default='day', help='a period of time which you want to merge your purcheses by.')
def purchase_history(merge_by: str):
    '''Prints the purchases history'''
    api_spinner.start()
    response = generic_request(api_url_path=f"{PURCHASE_HISTORY_ENDPOINT}", method='GET')
    purchase_rows = parse_jsons_to_purcheserows(response.json(), parse_jsons_to_purchases,
                                                parse_purchases_to_purcheserows_merge, 'offer_closed_at', merge_by)
    api_spinner.succeed(text="Recived and pared API request")
    print_table_w_date_headers(copy.deepcopy(purchase_rows), merge_by)
    if LOGGING == 'True':
        log(response.json(), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")


@click.command()
@click.option('--date', required=True, prompt=True, help='Date from which you want to see your purchase history (%Y-%m-%d).')
def purchase_history_from(date: str):
    '''Prints the purchases history'''
    date = datetime.strptime(date, '%Y-%m-%d')
    api_spinner.start()
    response = generic_request(api_url_path=f"{PURCHASE_HISTORY_ENDPOINT}", method='GET')
    purchase_rows = parse_jsons_to_purcheserows(response.json(), parse_jsons_to_purchases,
                                                parse_purchases_to_purcheserows_by_date, 'offer_closed_at', date)
    api_spinner.succeed(text="Recived and pared API request")
    print_table(copy.deepcopy(purchase_rows))
    if LOGGING == 'True':
        log(response.json(), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")


@click.command()
def steam_inventory():
    '''Prints all of your inventory found on Steam'''
    api_spinner.start()
    response = generic_request(api_url_path=STEAM_INVENTORY_ENDPOINT, method='GET')
    steam_rows = parse_jsons_to_rows(response.json(), parse_jsons_to_inventoryitems,
                                     parse_inventoryitems_to_inventoryitemrow, 'total_price')
    api_spinner.succeed(text="Recived and pared API request")
    print_table(copy.deepcopy(steam_rows))
    if LOGGING == 'True':
        log(response.json(), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")


@click.command()
def inventory():
    '''Prints all of your inventory'''
    api_spinner.start()
    dm_response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
    dm_rows = parse_jsons_to_rows(dm_response.json(), parse_jsons_to_inventoryitems,
                                  parse_inventoryitems_to_inventoryitemrow, 'total_price')
    steam_response = generic_request(api_url_path=STEAM_INVENTORY_ENDPOINT, method='GET')
    steam_rows = parse_jsons_to_rows(steam_response.json(), parse_jsons_to_inventoryitems,
                                     parse_inventoryitems_to_inventoryitemrow, 'total_price')
    api_spinner.succeed(text="Recived and pared API request")
    responses = [steam_response, dm_response]
    print_table(copy.deepcopy(dm_rows + steam_rows))
    if LOGGING == 'True':
        log(merge_dicts(responses), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")


@click.command()
def listings():
    '''Prints all the listings on Dmarket'''
    api_spinner.start()
    response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if response.json()['Total'] != '0':
        listings_rows = parse_jsons_to_rows(response.json(), parse_jsons_to_listings,
                                            parse_listings_to_listingrows, 'total_price')
        api_spinner.succeed(text="Recived and pared API request")
        print_table(copy.deepcopy(listings_rows))
    else:
        click.prompt(chalk.cyan('There are ZERO items listed'))
    if LOGGING == 'True':
        log(response.json(), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")


@click.command()
def balance():
    '''View your current Dmarket balance'''
    click.echo(chalk.cyan('Your DMarket balance: ' +
               str(float(generic_request(api_url_path=BALANCE_ENDPOINT,
                   method='GET').json()['usd'])/100) + '$'))


view.add_command(dm_inventory)
view.add_command(steam_inventory)
view.add_command(inventory)
view.add_command(listings)
view.add_command(balance)
view.add_command(purchase_history)
view.add_command(purchase_history_from)


if __name__ == '__main__':
    view()
