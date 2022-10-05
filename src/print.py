'''This module contains the main loop of the program and prints'''
# from typing import List
from tabulate import tabulate
import numpy as np
from row import InventoryItemRow, ListingRow


def print_table(rows: list):
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

