'''This module contains the main loop of the program and prints'''
from typing import List
import sys
import inspect
import click
import copy
from tabulate import tabulate
import numpy as np
from api_requests import (generic_request, request_devider_buy_order, request_devider_listing)
from config import (BUY_ORDER_ENDPOINT, INVENTORY_ENDPOINT,LOGGING)
from parsing import (listing_error_parsing,
                     parse_jsons_to_inventoryitems,
                     buy_order_body, write_content, merge_dicts,
                     parse_inventoryitems_to_inventoryitemrow)
from row import (InventoryItemRow, ListingRow)


@click.group()
def create():
    '''creating listings,'''
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
def listing():
    '''Creates listing on Dmarket'''
    dm_response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
    dm_items = parse_jsons_to_inventoryitems(dm_response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
    dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(dm_rows))
    row_number = click.prompt(f'What item would you like to sell? choose index number - up to {len(dm_rows) - 1}\n', type=str)
    choosen_row = (vars(dm_rows[int(row_number)]))
    amount = click.prompt(f'how many items? You can sell up to {choosen_row["total_items"]} \n', type=int)
    price = click.prompt(f'for how much? the current market price is: {choosen_row["market_price"]}$ \n', type=float)
    responses = request_devider_buy_order(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=amount, body_func=buy_order_body, price=price, asset_ids=choosen_row["asset_ids"])
    error_list = listing_error_parsing(responses)
    print(f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were listed" if len(error_list) == 0 else f"{len(error_list)} items FAILED (and {amount - len(error_list)} succseeded) \nERROR: {error_list}")
    if LOGGING == 'True': 
        write_content(merge_dicts(responses), inspect.stack()[0][3])


create.add_command(listing)


if __name__ == '__main__':
    create()
