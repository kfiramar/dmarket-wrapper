'''This module contains the main loop of the program and prints'''
import inspect
import click
import copy
from api_requests import (generic_request, request_devider_buy_order)
from config import (BUY_ORDER_ENDPOINT, DM_INVENTORY_ENDPOINT, LOGGING)
from parsing import (listing_error_parsing,
                     parse_jsons_to_inventoryitems,
                     buy_order_body, write_content, merge_dicts,
                     parse_inventoryitems_to_inventoryitemrow)
from print import print_table


@click.group()
def create():
    '''creating listings,'''

@click.command()
def listing():
    '''Creates listing on Dmarket'''
    dm_response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
    dm_items = parse_jsons_to_inventoryitems(dm_response.json())
    dm_rows = parse_inventoryitems_to_inventoryitemrow(dm_items)
    dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
    print_table(copy.deepcopy(dm_rows))
    row_number = click.prompt(f'What item would you like to sell? choose index number - up to {len(dm_rows) - 1}\n', type=str)
    choosen_row = (vars(dm_rows[int(row_number)]))
    amount = click.prompt(f'how many items? You can sell up to {choosen_row["total_items"]} \n', type=int)
    price = click.prompt(f'for how much? the current market price is: {choosen_row["market_price"]}$ \n', type=float)
    responses = request_devider_buy_order(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=amount, body_func=buy_order_body, price=price, asset_ids=choosen_row["asset_ids"])
    error_list = listing_error_parsing(responses)
    print(f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were listed" if len(error_list) == 0 else f"{len(error_list)} items FAILED (and {amount - len(error_list)} succseeded) \nERROR: {error_list}")
    if LOGGING == 'True': 
        write_content(merge_dicts(responses), inspect.stack()[0][3])


create.add_command(listing)


if __name__ == '__main__':
    create()
