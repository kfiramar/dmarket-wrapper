
'''This module contains the main loop of the program and prints'''
from datetime import datetime
from email.policy import default
import os
import inspect
import copy
import click
from halo import Halo
from simple_chalk import chalk
from api_requests import (generic_request)
from config import (ACTIVE_TARGETS_ENDPOINT, BALANCE_ENDPOINT, DM_INVENTORY_ENDPOINT, INACTIVE_TARGETS_ENDPOINT, PURCHASE_HISTORY_ENDPOINT,
                    STEAM_INVENTORY_ENDPOINT, SELL_LISTINGS_ENDPOINT, LOGGING)
from parsing import (parse_jsons_to_listings, parse_jsons_to_inventoryitems, parse_jsons_to_purcheserows,
                     parse_listings_to_listingrows,
                     parse_inventoryitems_to_inventoryitemrow, parse_jsons_to_rows,
                     parse_jsons_to_purchases, parse_purchases_to_purcheserows_by_date, parse_purchases_to_purcheserows_merge)
from print import print_table, print_table_w_date_headers
from logger import log, merge_dicts


api_spinner = Halo(text='Attempting to get your items', spinner='dots', animation='bounce', color='green')


@click.group()
def view():
    '''viewing listings, inventory -all, dm inventory and steam inventory'''





@click.command()
@click.option('--active-target', required=True, prompt=True, help='a period of time which you want to merge your purcheses by.')
def targets(active_target) -> None:
    '''Prints all the inventory found on DMarket'''
    target = ACTIVE_TARGETS_ENDPOINT if active_target != 'False' else INACTIVE_TARGETS_ENDPOINT
    api_spinner.start()
    response = generic_request(api_url_path=f"{target}", method='GET')
    # dm_rows = parse_jsons_to_rows(response.json(), parse_jsons_to_inventoryitems,
    #                               parse_inventoryitems_to_inventoryitemrow, 'total_price')
    api_spinner.succeed(text="Recived and pared API request")
    # print_table(copy.deepcopy(dm_rows))
    if LOGGING == 'True':
        log(response.json(), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")        


@click.command()
@click.option('--merge_by', default='day', help='a period of time which you want to merge your purcheses by.')
def purchase_history(merge_by: str) -> None:
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
def purchase_history_from(date: str) -> None:
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
@click.option('--source', required=True, prompt=True, help='a period of time which you want to merge your purcheses by.')
def inventory(source) -> None:
    '''Prints all of your inventory'''
    responses = []
    rows = []
    api_spinner.start()
    if source in ('dm', 'all'):
        dm_response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
        dm_rows = parse_jsons_to_rows(dm_response.json(), parse_jsons_to_inventoryitems,
                                      parse_inventoryitems_to_inventoryitemrow, 'total_price')
        responses.append(dm_response)
        rows.extend(dm_rows)
    if source in ('steam', 'all'):
        steam_response = generic_request(api_url_path=STEAM_INVENTORY_ENDPOINT, method='GET')
        steam_rows = parse_jsons_to_rows(steam_response.json(), parse_jsons_to_inventoryitems,
                                         parse_inventoryitems_to_inventoryitemrow, 'total_price')
        responses.append(steam_response)
        rows.extend(steam_rows)
    api_spinner.succeed(text="Recived and pared API request")
    print_table(copy.deepcopy(rows))
    if LOGGING == 'True':
        log(merge_dicts(responses), f"{os.path.basename(__file__)[:-3]}_{inspect.stack()[0][3]}")













@click.command()
def listings() -> None:
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
def balance() -> None:
    '''View your current Dmarket balance'''
    click.echo(chalk.cyan('Your DMarket balance: ' +
               str(float(generic_request(api_url_path=BALANCE_ENDPOINT,
                   method='GET').json()['usd'])/100) + '$'))


view.add_command(inventory)
view.add_command(listings)
view.add_command(balance)
view.add_command(purchase_history)
view.add_command(purchase_history_from)
view.add_command(targets)


if __name__ == '__main__':
    view()
