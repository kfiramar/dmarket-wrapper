'''This module contains the main loop of the program and prints'''

from pathlib import Path
import inspect
import copy
import click
from simple_chalk import chalk
from halo import Halo
from api_client.api_requests import generic_request, request_devider_buy_order
from common.config import BUY_ORDER_ENDPOINT, DM_INVENTORY_ENDPOINT, LOGGING
from common.parsing import (listing_error_parsing,
                     parse_jsons_to_inventoryitems,
                     parse_inventoryitems_to_inventoryitemrow,
                     parse_jsons_to_rows)
from table.print import print_table
from api_client.request_body import buy_order_body
from common.logger import log, merge_dicts

func_name = Path(__file__).stem
items_api_spinner = Halo(text='Attempting to get items', spinner='dots', animation='bounce', color='green')
create_api_spinner = Halo(text='Attempting to create', spinner='dots', animation='bounce', color='green')


@click.group()
def create():
    '''creating listings'''


@click.command()
def listing():
    '''Creates listing on Dmarket'''
    items_api_spinner.start()
    dm_response = generic_request(api_url_path=f"{DM_INVENTORY_ENDPOINT}", method='GET')
    dm_rows = parse_jsons_to_rows(dm_response.json(), parse_jsons_to_inventoryitems,
                                  parse_inventoryitems_to_inventoryitemrow, 'total_price')
    items_api_spinner.succeed(text='Sucssesfully recived your items')
    print_table(copy.deepcopy(dm_rows))
    row_number = click.prompt(chalk.cyan(f'What item would you like to sell? choose index number - up to {len(dm_rows) - 1}'))
    choosen_row = (vars(dm_rows[int(row_number)]))
    amount = click.prompt(chalk.cyan(f'how many items? You can sell up to {choosen_row["total_items"]}'))
    price = click.prompt(chalk.cyan(f'for how much? the current market price is: {choosen_row["market_price"]}$'))
    create_api_spinner.start()
    responses = request_devider_buy_order(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=int(amount), body_func=buy_order_body, price=price, asset_ids=choosen_row["asset_ids"])
    error_list = listing_error_parsing(responses)
    if len(error_list) == 0:
        create_api_spinner.succeed(text=f"SUCCESSFUL - {amount} items of {choosen_row['title']} were listed")
    else:
        create_api_spinner.fail(text=f"{len(error_list)} items FAILED (and {amount - len(error_list)} succseeded) \nERROR: {error_list}")
    if LOGGING == 'True':
        log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")


create.add_command(listing)


if __name__ == '__main__':
    create()
