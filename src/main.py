'''This module contains the main loop of the program and prints'''
from tabulate import tabulate
import numpy as np
from api_requests import generic_request
from parsing import parse_json_to_items, parse_items_to_rows
from api_requests import write_content

LOGGING = False
INVENTORY_RESPONSE_DM = generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=10000",method='GET')
INVENTORY_RESPONSE_STEAM = generic_request(api_url_path="/marketplace-api/v1/user-inventory?Limit=10000",method='GET')
TOTAL_STEAM = INVENTORY_RESPONSE_STEAM.json()['Total']
TOTAL_DM = INVENTORY_RESPONSE_DM.json()['Total']
TOTAL = str(int(TOTAL_STEAM) + int(TOTAL_DM))

def print_table(rows, total):
    '''Prints tables with headers and total at the end'''
    total_price = 0
    table = [list(vars(rows[0]).keys())]
    columns = len(list(vars(rows[0]).keys()))
    for row in rows:
        table.append(list(vars(row).values()))
        total_price += row.market_price*row.count
    list_test = list(np.full((columns),''))
    list_test[-2] = total
    list_test[-1] = total_price
    table.append(list_test)
    print(tabulate(table))


def cli_loop():
    '''main function - it is a cli loop that uses all the other functions'''
    dm_items = parse_json_to_items(INVENTORY_RESPONSE_DM.json())
    steam_items = parse_json_to_items(INVENTORY_RESPONSE_STEAM.json())
    all_items = dm_items + steam_items
    print("Welcome! this is Kfir's DMarket trading CLI! ")
    client_choice = input('\n What would you like to do?\n 1 - View DMarket inventory \n 2 - View Steam inventory \n 3 - View Total inventory \n 4 - Sell items \n 5 - Buy items \n 6 - Filter inventory for a spesific item \n 9 - To quit \n ')
    while (client_choice != 9):
        if client_choice == '1':
            dm_rows = parse_items_to_rows(dm_items)
            dm_rows.sort(key=lambda x: x.total_price)
            print_table(dm_rows, TOTAL_DM)

        elif client_choice == '2':
            steam_rows = parse_items_to_rows(steam_items)
            steam_rows.sort(key=lambda x: x.total_price)
            print_table(steam_rows, TOTAL_STEAM)

        elif client_choice == '3':
            all_rows = parse_items_to_rows(all_items)
            all_rows.sort(key=lambda x: x.total_price)
            print_table(all_rows, TOTAL)

        elif client_choice == '4':
            print('You choose 4')

        elif client_choice == '5':
            print('You choose 5')

        elif client_choice == '6':
            print('You choose 6')


        elif client_choice == '9':
            exit()

        else:
            print(' Wrong input, try again')

        client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')


if __name__ == '__main__':
    if LOGGING:
        write_content(INVENTORY_RESPONSE_DM.json(), 'GET')
    else:
        cli_loop()
