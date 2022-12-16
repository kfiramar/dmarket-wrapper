'''This module contains the main loop of the program and prints'''

import asyncio
from pathlib import Path
import inspect
import click
from halo import Halo
from api_client.api_requests import request_devider
from common.config import ATTEMPTING_CREATE_ITEMS, CREATE_TARGET_AMOUNT, CREATE_TARGET_PRICE, GETTING_ITEMS, BUY_ORDER_REQUEST, CREATE_LISTINGS_AMOUNT, CREATE_LISTINGS_PRICE, CREATE_TARGET_REQUEST, LOGGING, CREATE_LISTINGS_ITEMS, SPINNER_CONF, SUCCESSFULLY_CREATED, UNSUCSESSFULLY_CREATED, INVENTORY_ZERO_ITEMS, NO_ITEM
from common.logger import log, merge_dicts
from items.listing_item import listing_error_parsing
from commands.view import get_dmarket_items, get_inventory
from table.print import print_table

func_name = Path(__file__).stem
items_api_spinner = Halo(text=GETTING_ITEMS, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])
create_api_spinner = Halo(text=ATTEMPTING_CREATE_ITEMS, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])


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
        choosen_row = target_item[int(row_number)]
        amount = click.prompt(CREATE_LISTINGS_AMOUNT.format(choosen_row.amount))
        price = click.prompt(CREATE_LISTINGS_PRICE.format(choosen_row.market_price))
        create_api_spinner.start()
        responses = asyncio.run(request_devider(url_endpoint=BUY_ORDER_REQUEST['ENDPOINT'], method=BUY_ORDER_REQUEST['METHOD'], amount=int(amount), price=price, row=choosen_row))
        error_list = listing_error_parsing(responses)
        if len(error_list) == 0:
            create_api_spinner.succeed(text=SUCCESSFULLY_CREATED.format(amount, choosen_row.title))
        else:
            create_api_spinner.fail(text=UNSUCSESSFULLY_CREATED.format(error_list=error_list, failed_count=len(error_list), succeeded_amount=int(amount) - len(error_list)))
        if LOGGING:
            log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
    else:
        create_api_spinner.fail(text=INVENTORY_ZERO_ITEMS)



@click.command()
@click.option("--item_name", required=True, type=str, prompt=True, help='item you wish to create target to')
def target(item_name: str):
    '''Creates target on Dmarket'''
    target_item = get_dmarket_items(item_name, items=1).rows
    while not target_item:
        item_name = click.prompt(NO_ITEM.format(item_name=item_name))
        target_item = get_dmarket_items(item_name, items=1).rows
    target_item = target_item[0]
    price = click.prompt(CREATE_TARGET_PRICE.format(item_title=target_item.title, item_price = target_item.market_price), type=float)
    amount = click.prompt(CREATE_TARGET_AMOUNT.format(item_title=target_item.title), type=int)
    create_api_spinner.start()
    responses = asyncio.run(request_devider(url_endpoint=CREATE_TARGET_REQUEST['ENDPOINT'], method=CREATE_TARGET_REQUEST['METHOD'], amount=amount, price=price, row=target_item))
    merged_response = merge_dicts(responses)
    if LOGGING:
        log(merged_response, f"{func_name}_{inspect.stack()[0][3]}")
    if 'Result' in merged_response:
        create_api_spinner.succeed(text=SUCCESSFULLY_CREATED.format(amount, target_item.title))
    else:
        create_api_spinner.fail(text=UNSUCSESSFULLY_CREATED.format(merged_response['Message'], amount))



create.add_command(listing)
create.add_command(target)


if __name__ == '__main__':
    create()
