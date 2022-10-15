'''This module contains the main loop of the program and prints'''
import copy
import os
import time
from tabulate import tabulate
import numpy as np
from config import RAINBOW_TABLE


COLORS = ['\u001b[32;1m', '\u001b[32;1m', '\u001b[31;1m', '\u001b[31;1m', '\u001b[32;0m', '\u001b[32;0m', '\u001b[31;0m', '\u001b[31;0m']
TIME_TABLE = {'minute': -3, 'hour': -6, 'day': -9, 'month': -12, 'year': -15}


def print_table(rows: list):
    '''Prints tables with headers and totals at the end'''
    total_items, total_price, table = 0, 0, []
    try:
        headers = rows[0].get_keys()
        for row in rows:
            table.append(row.get_list())
            total_price += row.total_price
            total_items += row.total_items
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


def print_table_w_date_headers(rows: list, merge_by):
    '''Prints tables with date headers and totals at the end'''
    try:
        total_items, total_price, table, headers = 0, 0, [], rows[0].get_keys()
        empty_list, dash_list = list(np.full((len(headers)), '')), list(np.full((len(headers)), '-------')) 
        for i, row in enumerate(rows):
            if (rows[i-1].offer_closed_at[:TIME_TABLE[merge_by]] != row.offer_closed_at[:TIME_TABLE[merge_by]]):
                date_header_list = copy.deepcopy(empty_list)
                date_header_list[0] = row.offer_closed_at[:TIME_TABLE[merge_by]]
                table.append(dash_list)
                table.append(date_header_list)
                table.append(dash_list)
            table.append(row.get_list())
            total_price += row.total_price
            total_items += row.total_items
        last_row = copy.deepcopy(empty_list)
        last_row[headers.index("total_items")] = total_items
        last_row[headers.index("total_price")] = str(round(total_price, 2)) + '$'
        last_row[0] = "TOTAL:"
        table.append(last_row)
        if (len(table) < 10 and RAINBOW_TABLE == 'True'):
            print_rainbow_loop(tabulate(table, headers=headers, tablefmt='psql',
                               numalign='center', stralign='center',
                               floatfmt=".2f"))
        else:
            print(tabulate(table, headers=headers, tablefmt='psql',
                           numalign='center', stralign='center',
                           floatfmt=".2f"))
    except IndexError as error:
        raise IndexError("The table is completely empty") from error


def rainbow(text, pos):
    '''paint rainbow fumction'''
    rainbow_text = ""
    for char in text:
        rainbow_text += COLORS[pos] + char
        pos = 0 if pos == (len(COLORS)-1) else pos+1
    return rainbow_text


def print_rainbow_loop(text):
    '''prints rainbow loop for 3 seconds'''
    count = 0
    while count < 60:
        table = rainbow(text, count % (len(COLORS)-1))
        os.system('clear')
        print(table)
        count += 1
        time.sleep(0.05)
