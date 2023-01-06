'''This module contains the BasicItem class which represends a DMarket item'''

from api_client.api_requests import generic_request
from common.config import MARKET_ITEMS_REQUEST


class BasicItem:
    '''This class represends a DMarket item'''

    def __init__(self, title, market_price):
        self.title = title
        self.market_price = market_price

    @classmethod
    def from_json_to_item(cls):
        '''parse json to item'''
        raise NotImplementedError

    def update_item_price(self) -> list:
        '''Prints all of your inventory'''
        dm_response_content = generic_request(url_endpoint=MARKET_ITEMS_REQUEST['ENDPOINT'].format(
            self.title, 1, 0, 0), method=MARKET_ITEMS_REQUEST['METHOD'])
        self.market_price = get_price_from_json(dm_response_content)


def get_price_from_json(json_dict):
    return float(json_dict['objects'][0]['suggestedPrice']['USD'])/100


def parse_jsons_to_items_list(json_items):
    '''parses json items to items'''
    raise NotImplementedError


def parse_name_dict_to_dict(json_dict):
    '''
    Parses a list of dictionaries from:
                        {key - "Name":"tradeLock", value - "Value":"0"}, ...
                    to: {key:"tradeLock":"0"}
    Used only on InventoryItem
    '''
    raise NotImplementedError


def listing_error_parsing(responses: list) -> list:
    '''parse errors from the response -> only on ListingItem'''
    raise NotImplementedError
