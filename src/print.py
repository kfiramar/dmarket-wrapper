'''This module contains the main loop of the program and prints'''
import os
import time
from tabulate import tabulate
import numpy as np
from row import InventoryItemRow, ListingRow
from config import RAINBOW_TABLE


# colors = ['\u001b[31;1m', '\u001b[31;1m', '\u001b[32m', '\u001b[32;1m', '\u001b[33m', '\u001b[33;1m', '\u001b[34m', '\u001b[34;1m', '\u001b[35m', '\u001b[35;1m', '\u001b[36m', '\u001b[36;1m', '\u001b[37m', , '\u001b[37m', '\u001b[37m']
colors = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']


def print_table(rows: list):
    '''Prints tables with headers and total at the end'''
    total_items, total_price, table = 0, 0, []
    try:
        for row in rows:
            table.append(row.get_list())
            total_price += row.total_price
            total_items += row.total_items
        headers = rows[0].get_keys()
        last_row = list(np.full((len(headers)), '.........'))
        last_row[headers.index("total_items")] = total_items
        last_row[headers.index("total_price")] = str(round(total_price, 2)) + '$'
        last_row[0] = "TOTAL:"
        table.append(last_row)
        if (len(table) < 10 and RAINBOW_TABLE == 'True'):
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
    '''prints rainbow loop for 3 seconds'''
    count = 0
    while count < 60:
        table = rainbow(text, count % (len(colors)-1))
        os.system('clear')
        print(table)
        count += 1
        time.sleep(0.05)
