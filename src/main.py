'''This module contains the main loop of the program and prints'''
from typing import List
import sys
import copy
import json
import requests
from tabulate import tabulate
import numpy as np
from config import BUY_ORDER_ENDPOINT, BALANCE_ENDPOINT, INVENTORY_ENDPOINT, SELL_LISTINGS_ENDPOINT,DELETE_LISTING_ENDPOINT, LOGGING
from api_requests import generic_request,generic_request_w_body
from parsing import listing_error_parsing, parse_json_to_items, parse_items_to_rows, \
     buy_order_body, write_content, print_content, listings_body , json_fixer, \
     listing_error_parsing


def print_table(rows: List):
    '''Prints tables with headers and total at the end'''
    total_price = 0
    total_items = 0
    table = []
    for row in rows:
        delattr(row,'asset_ids')
        delattr(row,'offer_ids')
        table.append(list(vars(row).values()))
        total_price += float(row.market_price)*row.count
        total_items += row.count
    headers = list(vars(rows[0]).keys())
    last_row = list(np.full((len(headers)), ''))
    last_row[-2:-1] = total_items,total_price
    last_row[0] = "TOTAL:"
    table.append(last_row)
    print(tabulate(table, headers=headers, tablefmt='psql',
                   numalign='center', stralign='center', floatfmt=(".2f", ".2f"), showindex='always'))

def sort_rows(items: List, parse_by : str):
    '''sort rows by a paramater'''
    rows = parse_items_to_rows(items)
    rows.sort(key=lambda x: x.__getattribute__(parse_by))
    return rows



def cli_loop():
    '''main function - it is a cli loop that uses all the other functions'''
    balance = float(generic_request(api_url_path=BALANCE_ENDPOINT, method='GET').json()['usd'])/100
    print(f"Welcome! this is Kfir's DMarket trading CLI! Your balance is: {balance}$")
    print('\n What would you like to do?\n  1 - View DMarket inventory \n  2 - View Steam inventory\
         \n  3 - View Total inventory \n  4 - Sell items \n  5 - View sell listings \n  6 - Delete sell listings \
         \n  7 - Buy items \n  8 - Filter inventory for a spesific item \n -1 - To quit \n ')
    client_choice = input()
    while True:
        response = requests.models.Response()
        if client_choice == '1':
            response = generic_request(api_url_path= f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true",method='GET')
            dm_rows = sort_rows(parse_json_to_items(response.json()),parse_by= 'total_price')
            print_table(copy.deepcopy(dm_rows))

        elif client_choice == '2':
            response = generic_request(api_url_path= INVENTORY_ENDPOINT, method='GET')
            steam_rows = sort_rows(parse_json_to_items(response.json()),parse_by= 'total_price')
            print_table(copy.deepcopy(steam_rows))

        elif client_choice == '3':
            response_dm = generic_request(api_url_path= f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true",method='GET')
            dm_rows = sort_rows(parse_json_to_items(response_dm.json()),parse_by= 'total_price')
            response_steam = generic_request(api_url_path= INVENTORY_ENDPOINT, method='GET')
            steam_rows = sort_rows(parse_json_to_items(response_steam.json()),parse_by= 'total_price')
            response = response_steam, response_dm
            print_table(copy.deepcopy(dm_rows + steam_rows))

        elif client_choice == '4':
            response_dm = generic_request(api_url_path= f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true",method='GET')
            dm_rows = sort_rows(parse_json_to_items(response_dm.json()),parse_by= 'total_price')
            print_table(copy.deepcopy(dm_rows))
            row_number = input('What item would you like to sell? choose index number\n')
            choosen_row = (vars(dm_rows[int(row_number)]))
            amount = int(input(f'how many items? You can sell up to {choosen_row["count"]} \n'))
            price = input(f'for how much? the current market price is: {choosen_row["market_price"]}$ \n')
            response = ((generic_request_w_body(api_url_path= BUY_ORDER_ENDPOINT, method='POST', body=buy_order_body(amount, price, choosen_row["asset_ids"]))))
            error_list = listing_error_parsing(response)
            print(f"SUCCESSFUL - {amount} items of {choosen_row['title']} were listed" if len(error_list) == 0 else f" FAILED listing error {error_list}")
        
        elif client_choice == '5':
            response = generic_request(api_url_path= SELL_LISTINGS_ENDPOINT,method='GET')
            listings_rows = sort_rows(parse_json_to_items(response.json(),),parse_by= 'total_price')
            print_table(copy.deepcopy(listings_rows))


        elif client_choice == '6':
            listings_response = generic_request(api_url_path= SELL_LISTINGS_ENDPOINT,method='GET')
            listings_rows = sort_rows(parse_json_to_items(listings_response.json(),),parse_by= 'total_price')
            print_table(copy.deepcopy(listings_rows))
            row_number = input('What listings would you like to delete? choose an index number\n')
            choosen_row = (vars(listings_rows[int(row_number)]))
            amount = int(input(f'how many items would you like to delete? You can sell up to {choosen_row["count"]} \n'))
            response = ((generic_request_w_body(api_url_path= DELETE_LISTING_ENDPOINT, method='DELETE', body=listings_body(amount, choosen_row['market_price'], choosen_row["asset_ids"], choosen_row["offer_ids"]))))
            response_dict = json.loads(json_fixer(str(response.json())))
            print(f"SUCCESSFUL - {amount} items of {choosen_row['title']} were listed"  \
            if response_dict['fail'] == 'None' else f'FAILED - with error:{response_dict["fail"]}')

        elif client_choice == '7':
            print('You choose 7')

        elif client_choice == '8':
            print('You choose 8')

        elif client_choice == '-1':
            sys.exit()

        else:
            print(' Wrong input, try again')

        print('\n What else would you like to do?\n  1 - View DMarket inventory \n  2 - View Steam inventory\
         \n  3 - View Total inventory \n  4 - Sell items \n  5 - View sell listings \n  6 - Delete sell listings \
         \n  7 - Buy items \n  8 - Filter inventory for a spesific item \n -1 - To quit \n ')
        if LOGGING == 'True' and client_choice in range(0, 10) :
            write_content(response.json(), client_choice)
        client_choice = input()

if __name__ == '__main__':
    cli_loop()
