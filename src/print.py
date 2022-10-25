'''This module contains the main loop of the program and prints'''
import copy
import os
import time
from tabulate import tabulate
from config import RAINBOW_TABLE, COLORS, TIME_TABLE, RAINBOW_SPEED, RAINBOW_DURATION


def print_table(rows: list) -> None:
    '''Prints tables with headers and totals at the end'''
    try:
        total_items, total_price, table = 0, 0, []
        headers = rows[0].get_keys_list()
        empty_list, dash_list = ['']*len(headers), ['------------']*len(headers)
        for row in rows:
            table.append(row.get_values_list())
            total_price += row.total_price
            total_items += row.total_items
        last_row = copy.deepcopy(empty_list)
        last_row[headers.index("total_items")] = total_items
        last_row[headers.index("total_price")] = f"{total_price:0.2f}$"
        last_row[0] = "TOTAL:"
        table.append(dash_list)
        table.append(last_row)
        if (len(table) < 15 and RAINBOW_TABLE == 'True'):
            print_rainbow_loop(tabulate(table, headers=headers, tablefmt='psql',
                               numalign='center', stralign='center',
                               floatfmt=".2f", showindex='always'))
        else:
            print(tabulate(table, headers=headers, tablefmt='psql',
                           numalign='center', stralign='center',
                           floatfmt=".2f", showindex='always'))
    except IndexError as error:
        raise IndexError("The table is completely empty") from error


def print_table_w_date_headers(rows: list, merge_by: str) -> None:
    '''Prints tables with date headers and totals at the end'''
    try:
        total_items, total_price, table, headers = 0, 0, [], rows[0].get_keys_list()
        empty_list, dash_list = ['']*len(headers), ['------------']*len(headers)
        for i, row in enumerate(rows):
            if rows[i-1].offer_closed_at[:TIME_TABLE[merge_by]] != row.offer_closed_at[:TIME_TABLE[merge_by]]:
                date_header_list = copy.deepcopy(empty_list)
                date_header_list[0] = row.offer_closed_at[:TIME_TABLE[merge_by]]
                table.append(dash_list)
                table.append(date_header_list)
                table.append(dash_list)
            table.append(row.get_values_list())
            total_price += row.total_price
            total_items += row.total_items
        last_row = copy.deepcopy(empty_list)
        last_row[headers.index("total_items")] = total_items
        last_row[headers.index("total_price")] = f"{total_price:0.2f}$"
        last_row[0] = "TOTAL:"
        table.append(dash_list)
        table.append(last_row)
        if (len(table) < 15 and RAINBOW_TABLE == 'True'):
            print_rainbow_loop(tabulate(table, headers=headers, tablefmt='psql',
                               numalign='center', stralign='center',
                               floatfmt=".2f"))
        else:
            print(tabulate(table, headers=headers, tablefmt='psql',
                           numalign='center', stralign='center',
                           floatfmt=".2f"))
    except IndexError as error:
        raise IndexError("The table is completely empty") from error


def rainbow(text: str, pos: int) -> str:
    '''paint rainbow fumction'''
    rainbow_text = ""
    for char in text:
        rainbow_text += COLORS[pos] + char
        pos = 0 if pos == (len(COLORS)-1) else pos+1
    return rainbow_text


def print_rainbow_loop(text: str) -> None:
    '''prints rainbow loop for X seconds'''
    for count in range(int(RAINBOW_SPEED*RAINBOW_DURATION)):
        print("\033[H\033[J" + rainbow(text, count % (len(COLORS)-1)))
        time.sleep(1/RAINBOW_SPEED)
