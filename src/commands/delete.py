'''This module contains the main loop of the program and prints'''
from pathlib import Path
import inspect
import copy
from types import NoneType
import click
from simple_chalk import chalk
from halo import Halo
from api_client.api_requests import request_devider
from common.config import DELETE_LISTING_ENDPOINT, LOGGING
from commands.view import get_listings
from table.print import print_table
from api_client.request_body import delete_listing_body
from common.logger import log, merge_dicts

func_name = Path(__file__).stem
items_api_spinner = Halo(text='Attempting to get your items', spinner='dots', animation='bounce', color='green')
create_api_spinner = Halo(text='Attempting to delete items', spinner='dots', animation='bounce', color='green')


@click.group()
def delete():
    '''deleting listings,'''


@click.command()
def listing():
    '''Delete a listings on Dmarket'''
    items_api_spinner.start()
    listings_rows = get_listings().rows
    if not isinstance(listings_rows, NoneType):
        items_api_spinner.succeed(text='Recived your items sucsessfully')
        print_table(copy.deepcopy(listings_rows))
        row_number = click.prompt(chalk.cyan(f'What listings would you like to remove? choose an index number - up to {len(listings_rows) - 1}'))
        choosen_row = (vars(listings_rows[int(row_number)]))
        amount = int(click.prompt(chalk.cyan(f'How many items would you like to delete? You can remove the listing of up to {choosen_row["total_items"]}')))
        create_api_spinner.start()
        responses = request_devider(
                api_url_path=DELETE_LISTING_ENDPOINT,
                method='DELETE', amount=int(amount),
                body_func=delete_listing_body,
                price=choosen_row['market_price'],
                asset_ids=choosen_row["asset_ids"],
                offer_ids=choosen_row["offer_ids"])
        merged_response = merge_dicts(responses)
        if LOGGING == 'True':
            log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
        if merged_response['fail'] is None:
            create_api_spinner.succeed(text=f"SUCCESSFUL - All {amount} items of {choosen_row['title']} were deleted")
        else:
            create_api_spinner.fail(text=f"{len(merged_response['fail'])} items FAILED (and \
            {amount - len(merged_response['fail'])} succseeded) \
            \nERROR: {merged_response['fail']}")
    else:
        items_api_spinner.fail(text="There are ZERO items listed")


delete.add_command(listing)


if __name__ == '__main__':
    delete()
