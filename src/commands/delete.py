'''This module contains the main loop of the program and prints'''


import inspect
import copy
import click
from api_requests import (generic_request, request_devider_listing)
from config import (SELL_LISTINGS_ENDPOINT, DELETE_LISTING_ENDPOINT, LOGGING)
from parsing import (parse_jsons_to_listings,
                     parse_listings_to_listingrows,
                     write_content, merge_dicts)
from print import print_table
from request_body import listings_body


@click.group()
def delete():
    '''deleting listings,'''


@click.command()
def listing():
    '''Delete a listings on Dmarket'''
    listings_response = generic_request(api_url_path=SELL_LISTINGS_ENDPOINT, method='GET')
    if listings_response.json()['Total'] != '0':
        listings = parse_jsons_to_listings(listings_response.json())
        listings_rows = parse_listings_to_listingrows(listings)
        listings_rows.sort(key=lambda row: getattr(row, 'total_price'))
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
    if LOGGING == 'True':
        write_content(merge_dicts(responses), inspect.stack()[0][3])


delete.add_command(listing)


if __name__ == '__main__':
    delete()
