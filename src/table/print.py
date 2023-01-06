'''This module contains the main loop of the program and prints'''
import time
from typing import List
from tabulate import tabulate
from common.config import MAXIMUM_ROWS, RAINBOW_TABLE, COLORS, TIME_TABLE, RAINBOW_SPEED, RAINBOW_DURATION, TABLE_LINE, TABLEFMT, NUMALIGN, STRALIGN, FLOATFMT, SHOWINDEX, EMPTY_TABLE, CLEAR_SHELL
from common.formatting import format_floats_to_usd


def print_table(rows: list) -> None:
    """
    Prints tables with totals at the end.

    Parameters:
    - rows: the rows of the table (list of row object)
    """
    if not rows:
        raise IndexError(EMPTY_TABLE)
    amount, total_price = 0, 0
    table = []
    headers = rows[0].get_rows_headers()
    colunm_count = len(headers)
    for row in rows:
        table.append(row.get_rows_values())
        total_price += row.total_price
        amount += row.amount
    table.append([TABLE_LINE]*colunm_count)
    table.append(create_last_row(headers, amount, total_price))
    print_table_tabulate(table, headers)


def print_table_with_date_headers(rows: list, merge_by: str = "day") -> None:
    """
    Prints tables with date headers and totals at the end.

    Parameters:
    - rows: the rows of the table (list of row object)
    - merge_by: the level at which the dates should be merged (str, optional, default="day")
    """
    if not rows:
        raise IndexError(EMPTY_TABLE)
    amount, total_price, table = 0, 0, []
    headers = rows[0].get_rows_headers()
    devider_line = [TABLE_LINE]*len(headers)
    for i, row in enumerate(rows):
        if rows[i-1].offer_closed_at[:TIME_TABLE[merge_by]] != row.offer_closed_at[:TIME_TABLE[merge_by]]:
            date_header_list = row.offer_closed_at[:TIME_TABLE[merge_by]]
            table.append(devider_line)
            table.append([date_header_list])
            table.append(devider_line)
        table.append(row.get_rows_values())
        total_price += row.total_price
        amount += row.amount
    table.append(devider_line)
    table.append(create_last_row(headers, amount, total_price))
    print_table_tabulate(table, headers)


def print_table_tabulate(table: List["BasicRow"], headers: List[str]) -> None:
    """
    Prints a table.

    Parameters:
    - table: the table to be printed (list of rows, should be BasicTable)
    - headers: the headers of the table (list of str)
    """

    if len(table) > MAXIMUM_ROWS or not RAINBOW_TABLE:
        print(tabulate(table, headers=headers, tablefmt=TABLEFMT,
                       numalign=NUMALIGN, stralign=STRALIGN,
                       floatfmt=FLOATFMT, showindex=SHOWINDEX))
    else:
        print_rainbow_loop(tabulate(table, headers=headers, tablefmt=TABLEFMT,
                                    numalign=NUMALIGN, stralign=STRALIGN,
                                    floatfmt=FLOATFMT, showindex=SHOWINDEX))


def create_last_row(headers: List[str], item_count: int, total_price: int) -> List[str]:
    """
    Creates the last row (the totals) of a table.

    Parameters:
    - headers: the headers of the table (list)
    - item_count: the total number of items (int)
    - total_price: the total price of all items (int)

    Returns:
    - last_row: the last row of the table, with the totals (list of str or int)
    """
    last_row = ['']*len(headers)
    last_row[0] = "TOTAL:"
    last_row[headers.index("amount")] = item_count
    last_row[headers.index("total_price")] = f"{total_price:0.2f}$"
    return format_floats_to_usd(last_row)


def rainbow(text: str, pos: int = 0) -> str:
    """
    Turns text into rainbow text by assigning a different color to each character.

    Parameters:
    - text: the text to be turned into rainbow text (str)
    - pos: the starting position in the list of colors (int, optional, default=0)

    Returns:
    - rainbow_text: the text with each character displayed in a different color (str)
    """
    rainbow_text = ""
    for char in text:
        rainbow_text += COLORS[pos] + char
        pos = (pos + 1) % len(COLORS)
    return rainbow_text


def print_rainbow_loop(text: str) -> None:
    """
    Looping function that prints rainbow text.

    Parameters:
    - text: the text to be turned into rainbow text (str)
    """
    for count in range(int(RAINBOW_SPEED*RAINBOW_DURATION)):
        print(CLEAR_SHELL + rainbow(text, count % (len(COLORS)-1)))
        time.sleep(1/RAINBOW_SPEED)
