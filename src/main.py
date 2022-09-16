'''This module contains is the main module of the function, it contains all of the parsing and the main loop of the program'''
from tabulate import tabulate
import numpy as np
from api_requests import generic_request
from parsing import parse_json_to_items, parse_json_to_item, parse_items_to_rows

INVENTORY_RESPONSE = generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=10000",method='GET')
TOTAL = INVENTORY_RESPONSE.json()['Total']


def print_table(rows):
    '''Prints tables with headers and total at the end'''
    table = [list(vars(rows[0]).keys())]
    columns = len(list(vars(rows[0]).keys()))
    for row in rows:
        table.append(list(vars(row).values()))
    list_test = list(np.full((columns),''))
    list_test[-1] = TOTAL
    table.append(list_test)
    print(tabulate(table))


def cli_loop():
    '''main function - it is a cli loop that uses all the other functions'''
    all_items = parse_json_to_items(INVENTORY_RESPONSE.json())
    print("Welcome! this is Kfir's DMarket trading CLI! ")
    client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')
    while(client_choice != 9):
        if client_choice == '1':
            rows = parse_items_to_rows(all_items)
            print_table(rows)

        elif client_choice == '2':
            print('You choose 2')

        elif client_choice == '3':
            print('You choose 3')

        elif client_choice == '4':
            print('You choose 4')

        elif client_choice == '9':
            exit()

        else:
            print(' Wrong input, try again')

        client_choice = input('\n What would you like to do?\n 1 - View inventory \n 2 - Sell items \n 3 - Buy items \n 4 - Filter inventory for a spesific item \n 9 - To quit \n ')


if __name__ == '__main__':
    cli_loop()
