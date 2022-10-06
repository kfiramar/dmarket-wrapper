'''This module contains the main loop of the program and prints'''
from textwrap import indent
from simple_chalk import chalk
from tabulate import tabulate
import numpy as np
from row import InventoryItemRow, ListingRow
import time


# colors = ['\u001b[31;1m', '\u001b[31;1m', '\u001b[32m', '\u001b[32;1m', '\u001b[33m', '\u001b[33;1m', '\u001b[34m', '\u001b[34;1m', '\u001b[35m', '\u001b[35;1m', '\u001b[36m', '\u001b[36;1m', '\u001b[37m', , '\u001b[37m', '\u001b[37m']
colors = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']
# colors = ['\u001b[38;5;6n6']


def print_table(rows: list):
    '''Prints tables with headers and total at the end'''
    total_items, total_price, table = 0, 0, []
    try:
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
        if(len(table) < 10):
            print_rainbow_loop(tabulate(table, headers=headers, tablefmt='psql',
                numalign='center', stralign='center',
                floatfmt=".2f", showindex='always'))
        else:
            print(tabulate(table, headers=headers, tablefmt='psql',
                numalign='center', stralign='center',
                floatfmt=".2f", showindex='always'))
    except IndexError as error:
        raise IndexError("The table is completely empty") from error


def rainbow(text, pos):
    '''paint rainbow fumction'''
    rainbow_text = ""
    for char in text:
        rainbow_text += colors[pos] + char
        pos = 0 if pos == (len(colors)-1) else pos+1
    return rainbow_text




def print_rainbow_loop(text): 
    count = 0
    while count < 20:  # Main program loop.
        print(rainbow(text, count % (len(colors)-1)))
        print('\n\n\n')
        time.sleep(0.1)  # Add a slight pause.
        count += 1
