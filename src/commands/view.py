
'''This module contains the main loop of the program and prints'''
import inspect
import copy
import click
from api_requests import (generic_request)
from config import (BALANCE_ENDPOINT, DM_INVENTORY_ENDPOINT,
                    STEAM_INVENTORY_ENDPOINT, SELL_LISTINGS_ENDPOINT, LOGGING)
from parsing import (parse_jsons_to_listings, parse_jsons_to_inventoryitems,
                     parse_listings_to_listingrows, write_content, merge_dicts,
                     parse_inventoryitems_to_inventoryitemrow)
from print import print_table


@click.group()
def view():
    '''viewing listings, inventory -all, dm inventory and steam inventory'''


@click.command()
def dmarket_inventory():
    '''Prints all the inventory found on DMarket'''
    response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
    items = parse_jsons_to_inventoryitems(response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(items)
    dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(dm_rows))
    if LOGGING == 'True':
        write_content(response.json(), inspect.stack()[0][3])


@click.command()
def steam_inventory():
    '''Prints all of your inventory found on Steam'''
    response = generic_request(api_url_path=STEAM_INVENTORY_ENDPOINT, method='GET')
    items = parse_jsons_to_inventoryitems(response.json())
    steam_rows = parse_inventoryitems_to_inventoryitemrow(items)
    steam_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(steam_rows))
    if LOGGING == 'True':
        write_content(response.json(), inspect.stack()[0][3])


@click.command()
def inventory():
    '''Prints all of your inventory'''
    dm_response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
    dm_items = parse_jsons_to_inventoryitems(dm_response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
    dm_rows.sort(key=lambda x: getattr(x, 'total_price'))
    steam_response = generic_request(api_url_path=STEAM_INVENTORY_ENDPOINT, method='GET')
    steam_items = parse_jsons_to_inventoryitems(steam_response.json())
    steam_rows = parse_inventoryitems_to_inventoryitemrow(steam_items)
    steam_rows.sort(key=lambda row: getattr(row, 'total_price'))
    responses = [steam_response, dm_response]
    print_table(copy.deepcopy(dm_rows + steam_rows))
    if LOGGING == 'True':
        write_content(merge_dicts(responses), inspect.stack()[0][3])


@click.command()
def listings():
    '''Prints all the listings on Dmarket'''
    response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if response.json()['Total'] != '0':
        item_listings = parse_jsons_to_listings(response.json())
        listings_rows = parse_listings_to_listingrows(item_listings)
        listings_rows.sort(key=lambda row: getattr(row, 'total_price'))
        print_table(copy.deepcopy(listings_rows))
    else:
        print('There are ZERO items listed')
    if LOGGING == 'True':
        write_content(response.json(), inspect.stack()[0][3])


@click.command()
def balance():
    '''View your current Dmarket balance'''
    print('Your DMarket balance: ' +
          str(float(generic_request(api_url_path=BALANCE_ENDPOINT, method='GET').json()['usd'])/100) + '$')


view.add_command(dmarket_inventory)
view.add_command(steam_inventory)
view.add_command(inventory)
view.add_command(listings)
view.add_command(balance)


if __name__ == '__main__':
    view()
