'''This module contains the main loop of the program and prints'''

from pathlib import Path
import inspect
import click
from halo import Halo
from api_client.api_requests import request_devider
from api_client.request_body import create_listing_body, create_target_body
from common.config import ATTEMPTING_GET_ITEMS, BUY_ORDER_ENDPOINT, CREATE_LISTINGS_AMOUNT, CREATE_LISTINGS_PRICE, CREATE_TARGET_ENDPOINT, LOGGING, CREATE_LISTINGS_ITEMS, SUCCESSFULLY_CREATED, UNSUCSESSFULLY_CREATED, INVENTORY_ZERO_ITEMS
from common.logger import log, merge_dicts
from items.listing_item import listing_error_parsing
from commands.view import get_dmarket_items, get_inventory
from table.print import print_table

func_name = Path(__file__).stem
items_api_spinner = Halo(text=ATTEMPTING_GET_ITEMS, spinner='dots', animation='bounce', color='green')
create_api_spinner = Halo(text='Attempting to create', spinner='dots', animation='bounce', color='green')


@click.group()
def create():
    '''creating listings'''


@click.command()
def listing():
    '''Creates listing on Dmarket'''
    target_item = get_inventory(inventory_source='dm')
    if target_item:
        print_table(target_item)
        row_number = click.prompt(CREATE_LISTINGS_ITEMS.format(len(target_item) - 1))
        choosen_row = (vars(target_item[int(row_number)]))
        amount = click.prompt(CREATE_LISTINGS_AMOUNT.format(choosen_row["amount"]))
        price = click.prompt(CREATE_LISTINGS_PRICE.format(choosen_row["market_price"]))
        create_api_spinner.start()
        responses = request_devider(api_url_path=BUY_ORDER_ENDPOINT, method='POST', amount=int(amount), body_func=create_listing_body, price=price, asset_ids=choosen_row["asset_ids"])
        error_list = listing_error_parsing(responses)
        if len(error_list) == 0:
            create_api_spinner.succeed(text=SUCCESSFULLY_CREATED.format(amount, choosen_row['title']))
        else:
            create_api_spinner.fail(text=UNSUCSESSFULLY_CREATED.format(error_list, amount))
        if LOGGING:
            log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
    else:
        create_api_spinner.fail(text=INVENTORY_ZERO_ITEMS)



@click.command()
@click.option("--items_name", required = True, type=str, prompt=True, help='item you wish to create target to')
def target(items_name: str):
    '''Creates target on Dmarket'''
    target_item = get_dmarket_items(items_name, items = 1).rows[0]
    if target_item:
        price = click.prompt(f'For how much do you want to sell: {target_item.title}\nCurrent lowest offer is: {target_item.market_price}$')
        amount = click.prompt('How many of this item would you liek to purchase?', type=int)
        create_api_spinner.start()
        responses = request_devider(api_url_path=CREATE_TARGET_ENDPOINT, method='POST', amount=amount, body_func=create_target_body, price=price, title=target_item.title)
        merged_response = merge_dicts(responses)
        if LOGGING:
            log(merged_response, f"{func_name}_{inspect.stack()[0][3]}")
        if 'result' in merged_response:
            create_api_spinner.succeed(text=SUCCESSFULLY_CREATED.format(amount, target_item.title))
        else:
            create_api_spinner.fail(text=UNSUCSESSFULLY_CREATED.format(merged_response['Message'], amount))
    else:
        create_api_spinner.fail(text=INVENTORY_ZERO_ITEMS)


create.add_command(listing)
create.add_command(target)


if __name__ == '__main__':
    create()
