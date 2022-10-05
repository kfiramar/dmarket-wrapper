
'''This module contains the main loop of the program and prints'''
from typing import List
import inspect
import click
import copy
from tabulate import tabulate
import numpy as np
from api_requests import (generic_request, request_devider_buy_order, request_devider_listing)
from config import (BALANCE_ENDPOINT, INVENTORY_ENDPOINT,
                    SELL_LISTINGS_ENDPOINT, LOGGING)
from parsing import (parse_jsons_to_listings, parse_jsons_to_inventoryitems,
                     parse_listings_to_listingrows, write_content, merge_dicts,
                     parse_inventoryitems_to_inventoryitemrow)
from row import (InventoryItemRow, ListingRow)



@click.group()
def view():
    '''viewing listings, inventory -all, dm inventory and steam inventory'''
    pass



def print_table(rows: List):
    '''Prints tables with headers and total at the end'''
    total_items, total_price, table = 0, 0, []
    is_listing, is_inventory_item_row = isinstance(rows[0], ListingRow), isinstance(rows[0], InventoryItemRow)
    for row in rows:
        if is_listing:
            total_price += float(row.listing_price)*row.total_items
        elif is_inventory_item_row:
            total_price += float(row.market_price)*row.total_items
        table.append(row.get_list())
        total_items += row.total_items
    headers = rows[0].get_keys()
    last_row = list(np.full((len(headers)), '.........'))
    last_row[headers.index("total_items")] = total_items
    last_row[headers.index("total_price")] = str(round(total_price, 2)) + '$'
    last_row[0] = "TOTAL:"
    table.append(last_row)
    print(tabulate(table, headers=headers, tablefmt='psql',
                   numalign='center', stralign='center',
                   floatfmt=".2f", showindex='always'))

@click.command()
def dmarket_inventory():
    '''Prints all the inventory found on DMarket'''
    response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
    items = parse_jsons_to_inventoryitems(response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(items)
    dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(dm_rows))
    if LOGGING == 'True':
        write_content(response.json(), inspect.stack()[0][3])


@click.command()
def steam_inventory():
    '''Prints all of your inventory found on Steam'''
    response = generic_request(api_url_path=INVENTORY_ENDPOINT, method='GET')
    items = parse_jsons_to_inventoryitems(response.json())
    steam_rows = parse_inventoryitems_to_inventoryitemrow(items)
    steam_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(steam_rows))
    if LOGGING == 'True':
        write_content(response.json(), inspect.stack()[0][3])


@click.command()
def inventory():
    '''Prints all of your inventory'''
    dm_response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
    dm_items = parse_jsons_to_inventoryitems(dm_response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
    dm_rows.sort(key=lambda x: getattr(x, 'total_price'))
    steam_response = generic_request(api_url_path=INVENTORY_ENDPOINT, method='GET')
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
        write_content(response.json(),inspect.stack()[0][3])

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
