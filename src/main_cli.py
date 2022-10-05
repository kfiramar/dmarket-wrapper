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



@click.group()
def mycommands():
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
def view_dmarket_inventory():
    '''Prints all the inventory found on DMarket'''
    response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
    items = parse_jsons_to_inventoryitems(response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(items)
    dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(dm_rows))
    if LOGGING == 'True':
        write_content(response.json(),inspect.stack()[0][3])


@click.command()
def view_steam_inventory():
    '''Prints all of your inventory found on Steam'''
    response = generic_request(api_url_path=INVENTORY_ENDPOINT, method='GET')
    items = parse_jsons_to_inventoryitems(response.json())
    steam_rows = parse_inventoryitems_to_inventoryitemrow(items)
    steam_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(steam_rows))
    if LOGGING == 'True':
        write_content(response.json(),inspect.stack()[0][3])

@click.command()
def view_inventory():
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
        write_content(merge_dicts(responses),inspect.stack()[0][3])


@click.command()
def create_listing():
    '''Creates listing on Dmarket'''
    dm_response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
    dm_items = parse_jsons_to_inventoryitems(dm_response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
    dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(dm_rows))
    row_number = click.prompt(f'What item would you like to sell? choose index number - up to {len(dm_rows) - 1}\n', type=str)
    choosen_row = (vars(dm_rows[int(row_number)]))
    amount = click.prompt(f'how many items? You can sell up to {choosen_row["total_items"]} \n', type=int)
    price = click.prompt(f'for how much? the current market price is: {choosen_row["market_price"]}$ \n', type=int)
    responses = request_devider_buy_order(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=amount, body_func=buy_order_body, price=price, asset_ids=choosen_row["asset_ids"])
    error_list = listing_error_parsing(responses)
    print(f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were listed" if len(error_list) == 0 else f"{len(error_list)} items FAILED (and {amount - len(error_list)} succseeded) \nERROR: {error_list}")
    if LOGGING == 'True': 
        write_content(merge_dicts(responses),inspect.stack()[0][3])


@click.command()
def view_listings():
    '''Prints all the listings on Dmarket'''
    response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if response.json()['Total'] != '0':
        listings = parse_jsons_to_listings(response.json())
        listings_rows = parse_listings_to_listingrows(listings)
        listings_rows.sort(key=lambda row: getattr(row, 'total_price'))
        print_table(copy.deepcopy(listings_rows))
    else:
        print('There are ZERO items listed')
    if LOGGING == 'True':
        write_content(response.json(),inspect.stack()[0][3])

@click.command()
def delete_listing():
    '''Delete a listings on Dmarket'''
    listings_response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if listings_response.json()['Total'] != '0':
        listings = parse_jsons_to_listings(listings_response.json())
        listings_rows = parse_listings_to_listingrows(listings)
        listings_rows.sort(key=lambda row: getattr(row, 'total_price'))
        print_table(copy.deepcopy(listings_rows))
        row_number = input(f'What listings would you like to remove? choose an index number - up to {len(listings_rows) - 1} \n')
        choosen_row = (vars(listings_rows[int(row_number)]))
        amount = int(input(f'How many items would you like to delete? You can remove the listing of up to {choosen_row["total_items"]} \n'))

        responses = request_devider_listing(api_url_path=DELETE_LISTING_ENDPOINT,
                                            method='DELETE', amount=amount,
                                            body_func=listings_body,
                                            price=choosen_row['market_price'],
                                            asset_ids=choosen_row["asset_ids"],
                                            offer_ids=choosen_row["offer_ids"])

        merged_response = merge_dicts(responses)
        print(f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were deleted"
                if merged_response['fail'] is None else
                f"{len(merged_response['fail'])} items FAILED (and \
                {amount - len(merged_response['fail'])} succseeded) \
                \nERROR: {merged_response['fail']}")
    else:
        print('There are ZERO items listed')
    if LOGGING == 'True':
        write_content(merge_dicts(responses),inspect.stack()[0][3])



mycommands.add_command(view_dmarket_inventory)
mycommands.add_command(view_steam_inventory)
mycommands.add_command(view_inventory)
mycommands.add_command(create_listing)
mycommands.add_command(view_listings)
mycommands.add_command(delete_listing)


if __name__ == '__main__':
    mycommands()
