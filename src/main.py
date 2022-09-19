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
from types import SimpleNamespace
import json


LOGGING = False

balance = float(generic_request(api_url_path="/account/v1/balance", method='GET').json()['usd'])/100
inventory_response_dm = generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=10000",method='GET')
inventory_response_steam = generic_request(api_url_path="/marketplace-api/v1/user-inventory?Limit=10000",method='GET')
total_steam = inventory_response_steam.json()['Total']
total_dm = inventory_response_dm.json()['Total']
total_all = str(int(total_steam) + int(total_dm))


def print_table(rows, total):
    '''Prints tables with headers and total at the end'''
    total_price = 0
    table = []
    headers = list(vars(rows[0]).keys())
    # headers.remove('asset_id')
    columns = len(headers)
    for row in rows:
        # del row.asset_id
        row.market_price = str('     ' + row.market_price)
        table.append(list(vars(row).values()))
        total_price += float(row.market_price)*row.count

    list_test = list(np.full((columns), ''))
    list_test[-2] = total
    list_test[-1] = total_price
    table.append(list_test)
    print(tabulate(table, headers=headers, tablefmt='psql',
                   numalign='center', stralign='left', floatfmt=(".2f", ".2f"), showindex='always'))
    return table


def create_sorted_rows(items):
    rows = parse_items_to_rows(items)
    rows.sort(key=lambda x: x.total_price)
    return rows


def cli_loop():
    '''main function - it is a cli loop that uses all the other functions'''

    dm_items = parse_json_to_items(inventory_response_dm.json())
    steam_items = parse_json_to_items(inventory_response_steam.json())
    all_items = dm_items + steam_items
    dm_rows = create_sorted_rows(dm_items)
    steam_rows = create_sorted_rows(steam_items)
    all_rows = create_sorted_rows(all_items)
    print(f"Welcome! this is Kfir's DMarket trading CLI! Your balance is: {balance}$")
    client_choice = input('\n What would you like to do?\n 1 - View DMarket inventory \n 2 - View Steam inventory \n 3 - View Total inventory \n 4 - Sell items \n 5 - Buy items \n 6 - Filter inventory for a spesific item \n 9 - To quit \n ')
    while client_choice != 9:
        if client_choice == '1':
            print_table(dm_rows.copy(), total_dm)

        elif client_choice == '2':
            print_table(steam_rows.copy(), total_steam)

        elif client_choice == '3':
            print_table(all_rows.copy(), total_all)

        elif client_choice == '4':
            row_number = input('What item would you like to sell? choose index number\n')
            choosen_row = (vars(dm_rows[int(row_number)]))
            asset_id = choosen_row["asset_id"]
            amount = input(f'how many items? You can sell up to {choosen_row["count"]} \n')
            price = input(f'for how much? the default price is: {choosen_row["market_price"]} \n')
            for i in range (int(amount)):
                generic_request_2(api_url_path='/marketplace-api/v1/user-offers/create', method='POST', body=buy_order_body(price, asset_id))
                print(i)
            #response = json.loads(str(data.json()) , object_hook=lambda d: SimpleNamespace(**d))            
        elif client_choice == '5':
            print('You choose 5')

        elif client_choice == '6':
            print('You choose 6')

        elif client_choice == '9':
            sys.exit()

        else:
            print(' Wrong input, try again')

        client_choice = input('\n What would you like to do?\n 1 - View DMarket inventory \n 2 - View Steam inventory \n 3 - View Total inventory \n 4 - Sell items \n 5 - Buy items \n 6 - Filter inventory for a spesific item \n 9 - To quit \n ')

def asset_id_to_row(asset_id, rows):
    for row in rows:
        if (row.asset_id == asset_id):
            return row


def string_to_asset_id(item_name, rows):
    for row in rows:
        if (row.title == item_name):
            return row.asset_id


if __name__ == '__main__':
    if LOGGING:
        # write_content(inventory_response_dm.json(), 'GET')
        print(balance)
    else:
        cli_loop()
