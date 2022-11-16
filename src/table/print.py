'''This module contains the main loop of the program and prints'''
import time
from types import NoneType
from tabulate import tabulate
from common.config import MAXIMUM_ROWS, RAINBOW_TABLE, COLORS, TIME_TABLE, RAINBOW_SPEED, RAINBOW_DURATION, TABLE_LINE


def print_table(rows: list):
    '''Prints tables with headers and totals at the end'''
    if not isinstance(rows, NoneType):
        try:
            total_items, total_price, table = 0, 0, []
            headers = rows[0].get_keys_list()
            colunm_count = len(headers)
            for row in rows:
                table.append(row.get_values_list())
                total_price += row.total_price
                total_items += row.total_items
            table.append([TABLE_LINE]*colunm_count)
            table.append(create_last_row(headers, total_items, total_price))
            if (len(table) < MAXIMUM_ROWS and RAINBOW_TABLE):
                print_rainbow_loop(tabulate(table, headers=headers, tablefmt='psql',
                                numalign='center', stralign='center',
                                floatfmt=".2f", showindex='always'))
            else:
                print(tabulate(table, headers=headers, tablefmt='psql',
                            numalign='center', stralign='center',
                            floatfmt=".2f", showindex='always'))
        except IndexError as error:
            raise IndexError("The table is completely empty") from error



def print_table_w_date_headers(rows: list, merge_by: str):
    '''Prints tables with date headers and totals at the end'''
    try:
        total_items, total_price, table = 0, 0, []
        headers = rows[0].get_keys_list()
        colunm_count = len(headers)
        empty_list = ['']* colunm_count
        for i, row in enumerate(rows):
            if rows[i-1].offer_closed_at[:TIME_TABLE[merge_by]] != row.offer_closed_at[:TIME_TABLE[merge_by]]:
                date_header_list = empty_list
                date_header_list[0] = row.offer_closed_at[:TIME_TABLE[merge_by]]
                table.append([TABLE_LINE]*colunm_count)
                table.append(date_header_list)
                table.append([TABLE_LINE]*colunm_count) 
            table.append(row.get_values_list())
            total_price += row.total_price
            total_items += row.total_items
        table.append([TABLE_LINE]*colunm_count)
        table.append(create_last_row(headers, total_items, total_price))
        if (len(table) < MAXIMUM_ROWS and RAINBOW_TABLE):
            print_rainbow_loop(tabulate(table, headers=headers, tablefmt='psql',
                               numalign='center', stralign='center',
                               floatfmt=".2f"))
        else:
            print(tabulate(table, headers=headers, tablefmt='psql',
                           numalign='center', stralign='center',
                           floatfmt=".2f"))
    except IndexError as error:
        raise IndexError("The table is completely empty") from error

def create_last_row(headers, total_items, total_price):
    '''creates last row (the totals) of a table'''
    last_row = ['']*len(headers)
    last_row[0] = "TOTAL:"  
    last_row[headers.index("total_items")] = total_items
    last_row[headers.index("total_price")] = f"{total_price:0.2f}$"
    return last_row

def rainbow(text: str, pos: int) -> str:
    '''turns text to rainbow text'''
    rainbow_text = ""
    for char in text:
        rainbow_text += COLORS[pos] + char
        pos = 0 if pos == (len(COLORS)-1) else pos+1
    return rainbow_text


def print_rainbow_loop(text: str):
    '''loop function that prints rainbow text'''
    for count in range(int(RAINBOW_SPEED*RAINBOW_DURATION)):
        print("\033[H\033[J" + rainbow(text, count % (len(COLORS)-1)))
        time.sleep(1/RAINBOW_SPEED)
