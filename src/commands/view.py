
'''This module contains the main loop of the program and prints'''
from datetime import datetime
from pathlib import Path
import inspect
from types import NoneType
import typer
from halo import Halo
from api_client.api_requests import (generic_request)
from common.config import (BALANCE_REQUEST, DM_INVENTORY_REQUEST, MARKET_ITEMS_REQUEST, PURCHASE_HISTORY_REQUEST, SPINNER_CONF,
                    STEAM_INVENTORY_REQUEST, SELL_LISTINGS_REQUEST, LOGGING, RECIVED_ITEMS, LISTING_ZERO_ITEMS, BALANCE_TEXT, GETTING_ITEMS, VALID_INVENTORY_ARGUMENTS, VIEW_TARGETS_REQUEST )
from common.logger import log, merge_dicts
from items.target_item import TargetItem
from table.tables.target_item_table import TargetItemTable
from table.tables.listing_table import ListingTable
from table.tables.inventory_item_table import InventoryItemTable
from table.tables.purchese_table import PurcheseTable
from table.tables.dmarket_item_table import DMarketItemTable
from table.print import print_table, print_table_with_date_headers


func_name = Path(__file__).stem
api_spinner = Halo(text=GETTING_ITEMS, spinner=SPINNER_CONF['TYPE'], animation=SPINNER_CONF['ANIMATION'], color=SPINNER_CONF['COLOR'])


view = typer.Typer(rich_markup_mode="markdown")

def validate_inventory_source(source):
    if source not in VALID_INVENTORY_ARGUMENTS:
        raise typer.BadParameter(f"Invalid source: {source}")
    return source

@view.command()
def inventory(inventory_source: str = typer.Option(..., prompt=True, callback=validate_inventory_source, help="choose inventory_source: dm, steamm, all.", rich_help_panel="Customization and Utils")) -> None:
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    print_table(get_inventory(inventory_source))
    api_spinner.succeed(text=RECIVED_ITEMS)


@view.command()
def listings() -> None:
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    current_listings = get_listings()
    if not isinstance(current_listings, NoneType):
        print_table(current_listings.rows)
        api_spinner.succeed(text=RECIVED_ITEMS)
    else:
        api_spinner.fail(text=LISTING_ZERO_ITEMS)

@view.command()
# @app_test.option("--items_name", required = True, type=str, prompt=True, )
def dmarket_items(items_name: str = typer.Option(..., prompt=True, help='item you wish to create target to')) -> None:
    '''Prints all the inventory found on DMarket'''
    api_spinner.start()
    items = get_dmarket_items(title=items_name).rows
    if items:
        print_table(items)
        api_spinner.succeed(text=RECIVED_ITEMS)
    else:
        api_spinner.fail(text=LISTING_ZERO_ITEMS)


@view.command()
# @app_test.option('--merge_by', default='day',type=app_test.Choice(['minute', 'hour', 'day', 'month', 'year']), help='a period of time which you want to merge your purcheses by.')
def purchases(merge_by: str) -> None:
    '''Prints the purchases history'''
    api_spinner.start()
    response_content = generic_request(url_endpoint=PURCHASE_HISTORY_REQUEST['ENDPOINT'], method=PURCHASE_HISTORY_REQUEST['METHOD'])
    purchase_rows = PurcheseTable.parse_jsons_to_table(response_content)
    api_spinner.succeed(text=RECIVED_ITEMS)
    print_table_with_date_headers(purchase_rows.rows, merge_by)
    if LOGGING:
        log(response_content, f"{func_name}_{inspect.stack()[0][3]}")


# @click.command()
# @click.option('--date', required=True, prompt=True, help='Date from which you want to see your purchase history (%d/%m/%Y).')
@view.command()
def purchases_from(date: str) -> None:
    '''Prints the purchases history'''
    date = datetime.strptime(date, '%d/%m/%Y')
    api_spinner.start()
    response_content = generic_request(url_endpoint=PURCHASE_HISTORY_REQUEST['ENDPOINT'], method=PURCHASE_HISTORY_REQUEST['METHOD'])
    purchase_rows = PurcheseTable.parse_jsons_to_purchese_table_from_date(response_content, date)
    api_spinner.succeed(text=RECIVED_ITEMS)
    print_table(purchase_rows.rows)
    if LOGGING:
        log(response_content, f"{func_name}_{inspect.stack()[0][3]}")


def get_inventory(inventory_source: str) -> list:
    '''Prints all of your inventory'''
    returned_rows, responses = [], []
    if inventory_source in ('dm', 'all'):
        dm_response_content = generic_request(url_endpoint=DM_INVENTORY_REQUEST['ENDPOINT'], method=DM_INVENTORY_REQUEST['METHOD'])
        dm_rows = InventoryItemTable.parse_jsons_to_table(dm_response_content)
        returned_rows.extend(dm_rows.rows)
        responses.append(dm_response_content)
    if inventory_source in ('steam', 'all'):
        steam_response_content = generic_request(url_endpoint=STEAM_INVENTORY_REQUEST['ENDPOINT'], method=STEAM_INVENTORY_REQUEST['METHOD'])
        steam_rows = InventoryItemTable.parse_jsons_to_table(steam_response_content)
        returned_rows.extend(steam_rows.rows)
        responses.append(steam_response_content)
    if LOGGING:
        log(merge_dicts(responses), f"{func_name}_{inspect.stack()[0][3]}")
    return returned_rows


def get_dmarket_items(title:str, items:int = 100, min_price: int = 0, max_price: int = 0) -> list:
    '''Prints all of your inventory'''
    dm_response_content = generic_request(url_endpoint=MARKET_ITEMS_REQUEST['ENDPOINT'].format(title, items, min_price, max_price), method=MARKET_ITEMS_REQUEST['METHOD'])
    if LOGGING:
        log(dm_response_content, f"{func_name}_{inspect.stack()[0][3]}")
    dm_rows = DMarketItemTable.parse_jsons_to_table(dm_response_content)
    return dm_rows


def get_listings() -> None:
    '''Prints all the listings on Dmarket'''
    response_content = generic_request(url_endpoint=SELL_LISTINGS_REQUEST['ENDPOINT'], method=SELL_LISTINGS_REQUEST['METHOD'])
    if LOGGING:
        log(response_content, f"{func_name}_{inspect.stack()[0][3]}")
    return ListingTable.parse_jsons_to_table(response_content)


def get_targets() -> None:
    '''Prints all the listings on Dmarket'''
    response_content = generic_request(url_endpoint=VIEW_TARGETS_REQUEST['ENDPOINT'], method=VIEW_TARGETS_REQUEST['METHOD'])
    if LOGGING:
        log(response_content, f"{func_name}_{inspect.stack()[0][3]}")
    return TargetItemTable.parse_jsons_to_table(response_content)

@view.command()
def targets():
    """test"""
    api_spinner.start()
    current_targets = get_targets()
    if not isinstance(current_targets, NoneType):
        print_table(current_targets.rows)
        api_spinner.succeed(text=RECIVED_ITEMS)
    else:
        api_spinner.fail(text=LISTING_ZERO_ITEMS)



@view.command()
def balance() -> None:
    '''View your current Dmarket balance'''
    response_content = generic_request(url_endpoint=BALANCE_REQUEST['ENDPOINT'], method=BALANCE_REQUEST['METHOD'])
    typer.echo(BALANCE_TEXT.format(str(float(response_content['usd'])/100)))
    if LOGGING:
        log(response_content, f"{func_name}_{inspect.stack()[0][3]}")


# view.add_command(dmarket_items)
# view.add_command(targets)
# view.add_command(inventory)
# view.add_command(listings)
# view.add_command(balance)
# view.add_command(purchases)
# view.add_command(purchases_from)


# if __name__ == '__main__':
#     view()
