'''This module contains the main loop of the program and prints'''
import asyncio
from pathlib import Path
import inspect
import typer

from halo import Halo
from api_client.api_requests import request_devider
from common.config import DELETE_LISTING_REQUEST, LOGGING, CREATE_LISTINGS_ITEMS, REMOVE_LISTING_AMOUNT, REMOVE_LISTING_SUCCESSFULLY, REMOVE_LISTING_UNSUCCESSFULLY, RECIVED_ITEMS, LISTING_ZERO_ITEMS, GETTING_ITEMS, ATTEMPTING_DELETE, SPINNER_CONF
from common.logger import log, merge_dicts
from commands.view import get_listings, get_targets
from table.print import print_table

func_name = Path(__file__).stem
items_api_spinner = Halo(text=GETTING_ITEMS, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])
create_api_spinner = Halo(text=ATTEMPTING_DELETE, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])


delete = typer.Typer()

# # @app_test.group()
# # def delete():
#     '''deleting listings,'''


@delete.command()
def listing():
    '''Delete a listings on Dmarket'''
    items_api_spinner.start()
    listings_rows = get_listings().rows
    if listings_rows:
        items_api_spinner.succeed(text=RECIVED_ITEMS)
        print_table(listings_rows)
        row_number = app_test.prompt(CREATE_LISTINGS_ITEMS.format(len(listings_rows) - 1))
        choosen_row = (listings_rows[int(row_number)])
        amount = int(app_test.prompt(REMOVE_LISTING_AMOUNT.format(choosen_row.amount)))
        create_api_spinner.start()
        responses = asyncio.run(request_devider(url_endpoint=DELETE_LISTING_REQUEST['ENDPOINT'], method=DELETE_LISTING_REQUEST['METHOD'], amount=int(amount), price=choosen_row.market_price, row=choosen_row))
        merged_response = merge_dicts(responses)
        if LOGGING:
            log(merged_response, f"{func_name}_{inspect.stack()[0][3]}")
        if merged_response['fail'] is None:
            create_api_spinner.succeed(text=REMOVE_LISTING_SUCCESSFULLY.format(amount, choosen_row.title))
        else:
            create_api_spinner.fail(text=REMOVE_LISTING_UNSUCCESSFULLY.format(error_list=merged_response['fail'], failed_count=len(merged_response['fail']), succeeded_amount=int(amount) - len(merged_response['fail'])))
    else:
        items_api_spinner.fail(text=LISTING_ZERO_ITEMS)


@delete.command()
def target():
    '''Delete a listings on Dmarket'''
    items_api_spinner.start()
    all_targets = get_targets().rows
    if all_targets:
        items_api_spinner.succeed(text=RECIVED_ITEMS)
        print_table(all_targets)
        row_number = typer.prompt(CREATE_LISTINGS_ITEMS.format(len(all_targets) - 1), type= int)
        choosen_row = all_targets[row_number]
        amount = typer.prompt(REMOVE_LISTING_AMOUNT.format(choosen_row.amount), type=int)
        create_api_spinner.start()
        responses = asyncio.run(request_devider(url_endpoint=DELETE_LISTING_REQUEST['ENDPOINT'], method=DELETE_LISTING_REQUEST['METHOD'], amount=int(amount), price=choosen_row.market_price, row=choosen_row))
        merged_response = merge_dicts(responses)
        if LOGGING:
            log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
        if merged_response['fail'] is None:
            create_api_spinner.succeed(text=REMOVE_LISTING_SUCCESSFULLY.format(amount, choosen_row['title']))
        else:
            create_api_spinner.fail(text=REMOVE_LISTING_UNSUCCESSFULLY.format(len(merged_response['fail']), amount))
    else:
        items_api_spinner.fail(text=LISTING_ZERO_ITEMS)


# delete.add_command(listing)
# delete.add_command(target)


# if __name__ == '__main__':
#     delete()
