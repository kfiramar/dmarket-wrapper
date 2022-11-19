'''This module contains the main loop of the program and prints'''
import time
from types import NoneType
from tabulate import tabulate
from common.config import MAXIMUM_ROWS, RAINBOW_TABLE, COLORS, TIME_TABLE, RAINBOW_SPEED, RAINBOW_DURATION, TABLE_LINE, TABLEFMT, NUMALIGN, STRALIGN, FLOATFMT, SHOWINDEX, EMPTY_TABLE, CLEAR_SHELL

def print_table(rows: list) -> None:
    '''Prints tables with headers and totals at the end'''
    if not rows:
        raise IndexError(EMPTY_TABLE)
    else:
        amount, total_price = 0, 0
        table = []
        headers = rows[0].get_keys_list()
        colunm_count = len(headers)
        for row in rows:
            table.append(row.get_values_list())
            total_price += row.total_price
            amount += row.amount
        table.append([TABLE_LINE]*colunm_count)
        table.append(create_last_row(headers, amount, total_price))
        print_table_tabulate(table, headers)


def print_table_tabulate(table, headers) -> None:
    '''print a table with a configuration from configparser'''
    if (len(table) < MAXIMUM_ROWS and RAINBOW_TABLE):
        print_rainbow_loop(tabulate(table, headers=headers, tablefmt=TABLEFMT,
                        numalign=NUMALIGN, stralign=STRALIGN,
                        floatfmt=FLOATFMT, showindex=SHOWINDEX))
    else:
        print(tabulate(table, headers=headers, tablefmt=TABLEFMT,
                        numalign=NUMALIGN, stralign=STRALIGN,
                        floatfmt=FLOATFMT, showindex=SHOWINDEX))


def print_table_with_date_headers(rows: list, merge_by: str) -> None:
    '''Prints tables with date headers and totals at the end'''
    if not rows:
        raise IndexError(EMPTY_TABLE)
    else:
        amount, total_price, table = 0, 0, []
        headers = rows[0].get_keys_list()
        devider_line = [TABLE_LINE]*len(headers)
        for i, row in enumerate(rows):
            if rows[i-1].offer_closed_at[:TIME_TABLE[merge_by]] != row.offer_closed_at[:TIME_TABLE[merge_by]]:
                date_header_list = row.offer_closed_at[:TIME_TABLE[merge_by]]
                table.append(devider_line)
                table.append([date_header_list])
                table.append(devider_line)
            table.append(row.get_values_list())
            total_price += row.total_price
            amount += row.amount
        table.append(devider_line)
        table.append(create_last_row(headers, amount, total_price))
        print_table_tabulate(table, headers)


def create_last_row(headers: list, amount: int, total_price: int) -> list:
    '''creates last row (the totals) of a table'''
    last_row = ['']*len(headers)
    last_row[0] = "TOTAL:"
    last_row[headers.index("amount")] = amount
    last_row[headers.index("total_price")] = f"{total_price:0.2f}$"
    return last_row

def rainbow(text: str, pos: int) -> str:
    '''turns text to rainbow text'''
    rainbow_text = ""
    for char in text:
        rainbow_text += COLORS[pos] + char
        pos = 0 if pos == (len(COLORS)-1) else pos+1
    return rainbow_text


def print_rainbow_loop(text: str) -> None:
    '''loop function that prints rainbow text'''
    for count in range(int(RAINBOW_SPEED*RAINBOW_DURATION)):
        print(CLEAR_SHELL + rainbow(text, count % (len(COLORS)-1)))
        time.sleep(1/RAINBOW_SPEED)
