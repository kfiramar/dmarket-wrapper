'''This module contains the main loop of the program and prints'''
from pathlib import Path
import inspect
import copy
from types import NoneType
import click
from simple_chalk import chalk
from halo import Halo
from api_client.api_requests import request_devider
from common.config import DELETE_LISTING_ENDPOINT, LOGGING, CREATE_LISTINGS_ITEMS, REMOVE_LISTINGS_AMOUNT ,SUCSESSFULLY_DELETED ,UNSUCSESSFULLY_DELETED ,RECIVED_ITEMS ,ZERO_ITEMS, ATTEMPTING_GET_ITEMS, ATTEMPTING_DELETE
from commands.view import get_listings
from table.print import print_table
from api_client.request_body import delete_listing_body
from common.logger import log, merge_dicts

func_name = Path(__file__).stem
items_api_spinner = Halo(text=ATTEMPTING_GET_ITEMS, spinner='dots', animation='bounce', color='green')
create_api_spinner = Halo(text=ATTEMPTING_DELETE, spinner='dots', animation='bounce', color='green')


@click.group()
def delete():
    '''deleting listings,'''


@click.command()
def listing():
    '''Delete a listings on Dmarket'''
    items_api_spinner.start()
    listings_rows = get_listings().rows
    if not isinstance(listings_rows, NoneType):
        items_api_spinner.succeed(text=RECIVED_ITEMS)
        print_table(listings_rows)
        row_number = click.prompt(CREATE_LISTINGS_ITEMS.format(len(listings_rows) - 1))
        choosen_row = (vars(listings_rows[int(row_number)]))
        amount = int(click.prompt(REMOVE_LISTINGS_AMOUNT.format(choosen_row["total_items"])))
        create_api_spinner.start()
        responses = request_devider(
                api_url_path=DELETE_LISTING_ENDPOINT,
                method='DELETE', amount=int(amount),
                body_func=delete_listing_body,
                price=choosen_row['market_price'],
                asset_ids=choosen_row["asset_ids"],
                offer_ids=choosen_row["offer_ids"])
        merged_response = merge_dicts(responses)
        if LOGGING:
            log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
        if merged_response['fail'] is None:
            create_api_spinner.succeed(text=SUCSESSFULLY_DELETED.format(amount, choosen_row['title']))
        else:
            create_api_spinner.fail(text=UNSUCSESSFULLY_DELETED.format(len(merged_response['fail']), amount))
    else:
        items_api_spinner.fail(text=ZERO_ITEMS)


delete.add_command(listing)


if __name__ == '__main__':
    delete()
