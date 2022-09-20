'''This module contains the main loop of the program and prints'''
from email import header
from itertools import count
import sys
from tabulate import tabulate
import numpy as np
from api_requests import generic_request
from api_requests import generic_request_2
from parsing import parse_json_to_items, parse_items_to_rows, buy_order_body
from api_requests import write_content
from typing import List
import copy

LOGGING = False
BUY_ORDER_ENDOINT = '/marketplace-api/v1/user-offers/create'
BALANCE_ENDPOINT = '/account/v1/balance'
INVENTORY_ENDPOINT = '/marketplace-api/v1/user-inventory?Limit=10000'
SHOW_ASSET_ID = False

balance = float(generic_request(api_url_path=BALANCE_ENDPOINT, method='GET').json()['usd'])/100
inventory_response_dm = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true",method='GET')
inventory_response_steam = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}",method='GET')

def print_table(rows: List):
    '''Prints tables with headers and total at the end'''
    total_price = 0
    total_items = 0
    table = []
    headers = list(vars(rows[0]).keys())
    if not SHOW_ASSET_ID:  headers.remove('asset_ids')
    
    for row in rows:
        if not SHOW_ASSET_ID: delattr(row,'asset_ids')
        # row.market_price = str('       ' + row.market_price)
        table.append(list(vars(row).values()))
        total_price += float(row.market_price)*row.count
        total_items += row.count
    last_row = list(np.full((len(headers)), ''))
    last_row[-2:-1] = total_items,total_price
    table.append(last_row)
    print(tabulate(table, headers=headers, tablefmt='psql',
                   numalign='center', stralign='center', floatfmt=(".2f", ".2f"), showindex='always'))
    return table


def sort_rows(items: List):
    rows = parse_items_to_rows(items)
    rows.sort(key=lambda x: x.total_price)
    return rows


def cli_loop():
    '''main function - it is a cli loop that uses all the other functions'''

    dm_rows = sort_rows(parse_json_to_items(inventory_response_dm.json()))
    steam_rows = sort_rows(parse_json_to_items(inventory_response_steam.json()))
    all_rows = dm_rows + steam_rows
    print(f"Welcome! this is Kfir's DMarket trading CLI! Your balance is: {balance}$")
    client_choice = input('\n What would you like to do?\n 1 - View DMarket inventory \n 2 - View Steam inventory \n 3 - View Total inventory \n 4 - Sell items \n 5 - Buy items \n 6 - Filter inventory for a spesific item \n 9 - To quit \n ')
    while client_choice != 9:
        if client_choice == '1':
            print_table(copy.deepcopy(dm_rows))

        elif client_choice == '2':
            print_table(copy.deepcopy(steam_rows))

        elif client_choice == '3':
            print_table(copy.deepcopy(all_rows))

        elif client_choice == '4':
            print_table(copy.deepcopy(dm_rows))
            row_number = input('What item would you like to sell? choose index number\n')
            choosen_row = (vars(dm_rows[int(row_number)]))
            amount = int(input(f'how many items? You can sell up to {choosen_row["count"]} \n'))
            price = input(f'for how much? the current market price is: {choosen_row["market_price"]}$ \n')
            print(((generic_request_2(api_url_path= BUY_ORDER_ENDOINT, method='POST', body=buy_order_body(amount, price, choosen_row["asset_ids"]))).json())['Result'])

            
        elif client_choice == '5':
            print('You choose 5')

        elif client_choice == '6':
            print('You choose 6')

        elif client_choice == '9':
            sys.exit()

        else:
            print(' Wrong input, try again')

        client_choice = input('\n What else would you like to do?\n 1 - View DMarket inventory \n 2 - View Steam inventory \n 3 - View Total inventory \n 4 - Sell items \n 5 - Buy items \n 6 - Filter inventory for a spesific item \n 9 - To quit \n ')

def asset_id_to_row(asset_id : int, rows : List):
    for row in rows:
        if (row.asset_id == asset_id):
            return row


if __name__ == '__main__':
    if LOGGING:
        # write_content(inventory_response_dm.json(), 'GET')
        print(balance)
    else:
        cli_loop()
