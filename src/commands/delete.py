'''This module contains the main loop of the program and prints'''
from pathlib import Path
import inspect
from types import NoneType
import click
from halo import Halo
from api_client.api_requests import request_devider
from api_client.request_body import delete_listing_body
from common.config import DELETE_LISTING_REQUEST, LOGGING, CREATE_LISTINGS_ITEMS, REMOVE_LISTING_AMOUNT ,REMOVE_LISTING_SUCCESSFULLY ,REMOVE_LISTING_UNSUCCESSFULLY ,RECIVED_ITEMS ,LISTING_ZERO_ITEMS, GETTING_ITEMS, ATTEMPTING_DELETE, SPINNER_CONF
from common.logger import log, merge_dicts
from commands.view import get_listings, get_targets
from table.print import print_table

func_name = Path(__file__).stem
items_api_spinner = Halo(text=GETTING_ITEMS, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])
create_api_spinner = Halo(text=ATTEMPTING_DELETE, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])


@click.group()
def delete():
    '''deleting listings,'''


@click.command()
def listing():
    '''Delete a listings on Dmarket'''
    items_api_spinner.start()
    listings_rows = get_listings().rows
    if listings_rows:
        items_api_spinner.succeed(text=RECIVED_ITEMS)
        print_table(listings_rows)
        row_number = click.prompt(CREATE_LISTINGS_ITEMS.format(len(listings_rows) - 1))
        choosen_row = (listings_rows[int(row_number)])
        amount = int(click.prompt(REMOVE_LISTING_AMOUNT.format(choosen_row.amount)))
        create_api_spinner.start()
        responses = request_devider(url_endpoint=DELETE_LISTING_REQUEST['ENDPOINT'], method=DELETE_LISTING_REQUEST['METHOD'], amount=int(amount), price=choosen_row.market_price, row=choosen_row)
        merged_response = merge_dicts(responses)
        if LOGGING:
            log(merged_response, f"{func_name}_{inspect.stack()[0][3]}")
        if merged_response['fail'] is None:
            create_api_spinner.succeed(text=REMOVE_LISTING_SUCCESSFULLY.format(amount, choosen_row.title))
        else:
            create_api_spinner.fail(text=REMOVE_LISTING_UNSUCCESSFULLY.format(error_list=merged_response['fail'], failed_count=len(merged_response['fail']), succeeded_amount= int(amount) - len(merged_response['fail'])))
    else:
        items_api_spinner.fail(text=LISTING_ZERO_ITEMS)


@click.command()
def target():
    '''Delete a listings on Dmarket'''
    items_api_spinner.start()
    listings_rows = get_targets().rows
    if listings_rows:
        items_api_spinner.succeed(text=RECIVED_ITEMS)
        print_table(listings_rows)
        row_number = click.prompt(CREATE_LISTINGS_ITEMS.format(len(listings_rows) - 1))
        choosen_row = (vars(listings_rows[int(row_number)]))
        amount = int(click.prompt(REMOVE_LISTING_AMOUNT.format(choosen_row["amount"])))
        create_api_spinner.start()
        responses = request_devider(url_endpoint=DELETE_LISTING_REQUEST['ENDPOINT'], method=DELETE_LISTING_REQUEST['METHOD'], amount=int(amount), price=choosen_row.market_price, row=choosen_row)
        responses = request_devider(
                url_endpoint=DELETE_LISTING_REQUEST['ENDPOINT'],
                method=DELETE_LISTING_REQUEST['METHOD'], amount=int(amount),
                body_func=delete_listing_body,
                price=choosen_row['market_price'],
                asset_ids=choosen_row["asset_ids"],
                offer_ids=choosen_row["offer_ids"])
        merged_response = merge_dicts(responses)
        if LOGGING:
            log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
        if merged_response['fail'] is None:
            create_api_spinner.succeed(text=REMOVE_LISTING_SUCCESSFULLY.format(amount, choosen_row['title']))
        else:
            create_api_spinner.fail(text=REMOVE_LISTING_UNSUCCESSFULLY.format(len(merged_response['fail']), amount))
    else:
        items_api_spinner.fail(text=LISTING_ZERO_ITEMS)


delete.add_command(listing)


if __name__ == '__main__':
    delete()
