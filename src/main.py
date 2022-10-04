'''This module contains the main loop of the program and prints'''
from typing import List
import sys
import copy
from tabulate import tabulate
import numpy as np
from api_requests import (generic_request, request_devider_buy_order, request_devider_listing)
from config import (BUY_ORDER_ENDPOINT, BALANCE_ENDPOINT, INVENTORY_ENDPOINT,
                    SELL_LISTINGS_ENDPOINT, DELETE_LISTING_ENDPOINT, LOGGING)
from parsing import (listing_error_parsing, parse_jsons_to_listings,
                     parse_jsons_to_inventoryitems, parse_listings_to_listingrows,
                     buy_order_body, write_content, listings_body, merge_dicts,
                     parse_inventoryitems_to_inventoryitemrow)
from item import (InventoryItem, Listing)
from row import (InventoryItemRow, ListingRow)


def print_table(rows: List):
    '''Prints tables with headers and total at the end'''
    total_price = 0
    total_items = 0
    is_listing = isinstance(rows[0], ListingRow)
    is_inventory_item_row = isinstance(rows[0], InventoryItemRow)
    table = []
    for row in rows:
        # delattr(row, 'asset_ids')
        if is_listing:
            # delattr(row, 'offer_ids')
            total_price += float(row.listing_price)*row.total_items
        elif is_inventory_item_row:
            total_price += float(row.market_price)*row.total_items
        table.append(row.get_list())
        total_items += row.total_items
    headers = rows[0].get_keys()
    last_row = list(np.full((len(headers)), ''))
    last_row[headers.index("total_items")] = total_items
    last_row[headers.index("total_price")] = total_price
    last_row[0] = "TOTAL:"
    table.append(last_row)
    print(tabulate(table, headers=headers, tablefmt='psql',
                   numalign='center', stralign='center',
                   floatfmt=".2f", showindex='always'))


def input_from_user():
    '''Ask the client for an action'''
    print("\n  The options are: \
           \n  1 - View DMarket inventory \
           \n  2 - View Steam inventory\
           \n  3 - View Total inventory \
           \n  4 - Sell items \
           \n  5 - View sell listings \
           \n  6 - Delete sell listings \
           \n  7 - Buy items \
           \n  8 - Filter inventory for a spesific item \
           \n -1 - To quit \n")
    balance = float(generic_request(api_url_path=BALANCE_ENDPOINT, method='GET').json()['usd'])/100
    print(f"what are you willing to do with your {balance}$")
    return input('  ')


def cli_loop():
    '''main function - it is a cli loop that uses all the other functions'''
    print("Welcome! this is Kfir's DMarket trading CLI!")
    client_choice = input_from_user()
    while True:
        if client_choice == '1':
            response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
            items = parse_jsons_to_inventoryitems(response.json())
            dm_rows = parse_inventoryitems_to_inventoryitemrow(items)
            dm_rows.sort(key=lambda x: getattr(x, 'total_price'))
            print_table(copy.deepcopy(dm_rows))

        elif client_choice == '2':
            response = generic_request(api_url_path=INVENTORY_ENDPOINT, method='GET')
            items = parse_jsons_to_inventoryitems(response.json())
            steam_rows = parse_inventoryitems_to_inventoryitemrow(items)
            steam_rows.sort(key=lambda x: getattr(x, 'total_price'))
            print_table(copy.deepcopy(steam_rows))

        elif client_choice == '3':
            dm_response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
            dm_items = parse_jsons_to_inventoryitems(response.json())
            dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
            dm_rows.sort(key=lambda x: getattr(x, 'total_price'))
            steam_response = generic_request(api_url_path=INVENTORY_ENDPOINT, method='GET')
            steam_items = parse_jsons_to_inventoryitems(response.json())
            steam_rows = parse_inventoryitems_to_inventoryitemrow(steam_items)
            steam_rows.sort(key=lambda x: getattr(x, 'total_price'))
            responses = (steam_response, dm_response)
            print_table(copy.deepcopy(dm_rows + steam_rows))

        elif client_choice == '4':
            dm_response = generic_request(api_url_path=f"{INVENTORY_ENDPOINT}&BasicFilters.InMarket=true", method='GET')
            dm_items = parse_jsons_to_inventoryitems(dm_response.json())
            dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
            dm_rows.sort(key=lambda x: getattr(x, 'total_price'))
            print_table(copy.deepcopy(dm_rows))
            row_number = input(f'What item would you like to sell? choose index number - up to {len(dm_rows) - 1}\n')
            choosen_row = (vars(dm_rows[int(row_number)]))
            amount = int(input(f'how many items? You can sell up to {choosen_row["total_items"]} \n'))
            price = input(f'for how much? the current market price is: {choosen_row["market_price"]}$ \n')
            responses = request_devider_buy_order(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=amount, body_func=buy_order_body, price=price, asset_ids=choosen_row["asset_ids"])
            error_list = listing_error_parsing(responses)
            print(f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were listed" if len(error_list) == 0 else f"{len(error_list)} items FAILED (and {amount - len(error_list)} succseeded) \nERROR: {error_list}")

        elif client_choice == '5':
            response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
            if response.json()['Total'] != '0':
                listings = parse_jsons_to_listings(response.json())
                listings_rows = parse_listings_to_listingrows(listings)
                listings_rows.sort(key=lambda x: getattr(x, 'total_price'))
                print_table(copy.deepcopy(listings_rows))
            else:
                print('There are ZERO items listed')

        elif client_choice == '6':
            listings_response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
            if listings_response.json()['Total'] != '0':
                listings = parse_jsons_to_listings(response.json())
                listings_rows = parse_listings_to_listingrows(listings)
                listings_rows.sort(key=lambda x: getattr(x, 'total_price'))
                print_table(copy.deepcopy(listings_rows))
                row_number = input(f'What listings would you like to remove? choose an index number - up to {len(listings_rows) - 1} \n')
                choosen_row = (vars(listings_rows[int(row_number)]))
                amount = int(input(f'How many items would you like to delete? You can remove the listing of up to {choosen_row["total_items"]} \n'))

                responses = request_devider_listing(api_url_path=DELETE_LISTING_ENDPOINT,
                                                    method='DELETE', amount=amount,
                                                    body_func=listings_body,
                                                    price=choosen_row['market_price'],
                                                    asset_ids=choosen_row["asset_ids"],
                                                    offer_ids=choosen_row["offer_ids"])

                merged_response = merge_dicts(responses)

                print(f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were deleted"
                      if merged_response['fail'] is None else
                      f"{len(merged_response['fail'])} items FAILED (and \
                      {amount - len(merged_response['fail'])} succseeded) \
                      \nERROR: {merged_response['fail']}")

            else:
                print('There are ZERO items listed')

        elif client_choice == '7':
            print('You choose 7')

        elif client_choice == '8':
            print('You choose 8')

        elif client_choice == '-1':
            sys.exit()

        else:
            print(' Wrong input, try again')

        if LOGGING == 'True' and len(client_choice) == 1 and ord(client_choice) in range(48, 57):
            if client_choice in ('4', '6'):
                write_content(merge_dicts(responses), client_choice)
            elif client_choice == '3':
                write_content(responses, client_choice)
            else:
                write_content(response.json(), client_choice)

        client_choice = input_from_user()


if __name__ == '__main__':
    cli_loop()
