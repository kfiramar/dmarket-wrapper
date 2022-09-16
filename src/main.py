'''This module contains is the main module of the function, it contains all of the parsing and the main loop of the program'''
from tabulate import tabulate
import numpy as np
from item import Item
from row import Row
from api_requests import generic_request

INVENTORY_RESPONSE = generic_request(api_url_path="/marketplace-api/v1/user-inventory?BasicFilters.InMarket=true&Limit=10000",method='GET')
TOTAL = INVENTORY_RESPONSE.json()['Total']


def parse_json_to_items(json_list):
    '''uses parse_json_to_item to parse all the items from json'''
    items_list = []
    for json in json_list['Items']:
        items_list.append(parse_json_to_item(json=json))
    return items_list


def parse_json_to_item(json):
    '''parses a JSON into an item'''
    exterior = False
    itemtype = False
    tradelock = False
    unlock_date = False

    item = Item(
      asset_id=json['AssetID'],title=json['Title'],tradable=json['Tradable'],
      trade_lock=['tradeLock'],market_price=json['Offer']['Price']['Amount'])

    for attribute in json['Attributes']:

        if attribute['Name'] == 'exterior':
            item.exterior = attribute['Value']
            exterior = True

        elif attribute['Name'] == 'tradeLock':
            item.tradeLock = attribute['Value']
            tradelock = True

        elif attribute['Name'] == 'itemType':
            item.itemType = attribute['Value']
            itemtype = True

        elif attribute['Name'] == 'unlockDate':
            item.unlock_date = attribute['Value']
            unlock_date = True

        if (exterior and itemtype and tradelock and unlock_date):
            return item


def parse_items_to_rows(all_items):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title:
                row.count += 1
                break
        else:
            rows.append(Row(title=item.title, exterior = item.exterior, market_price = item.market_price, count = 1))
    return rows


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
