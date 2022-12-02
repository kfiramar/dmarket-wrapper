'''
This module contains the TargetItem class (which is a subclass of BasicItem)
TargetItem represends an Inventory item on DMarket
'''

from items.basic_item import BasicItem
# from commands.view import get_dmarket_items

import inspect
from pathlib import Path
from api_client.api_requests import generic_request
from common.config import LOGGING, MARKET_ITEMS_ENDPOINT
from common.logger import log
from table.tables.dmarket_item_table import DMarketItemTable

func_name = Path(__file__).stem

def get_item_price(title:str) -> list:
    '''Prints all of your inventory'''
    dm_response = generic_request(api_url_path=MARKET_ITEMS_ENDPOINT.format(title, 1, 0, 0), method='GET')
    price = DMarketItemTable.parse_jsons_to_table(dm_response.json()).rows['0'].market_price
    return price


class TargetItem(BasicItem):
    '''TargetItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, title, market_price, exterior, amount, target_id, listing_price):
        self.target_id = target_id
        self.listing_price = listing_price
        self.amount = amount
        self.exterior = exterior
        super().__init__(title, market_price)

    @classmethod
    def parse_json_to_item(cls, json_dict: dict):
        '''parses a JSON into an TargetItem'''
        attributes_dictionary = parse_name_dict_to_dict(json_dict['Attributes'])
        return cls(
                   target_id = json_dict['TargetID'],
                   title=json_dict['Title'],
                   listing_price=json_dict['Price']['Amount'],
                   exterior=attributes_dictionary['exterior'],
                   market_price = get_item_price(json_dict['Title']),
                   amount = json_dict['Amount'])

def parse_jsons_to_items_list(json_items: dict) -> list:
    '''parses json items to TargetItem list'''
    TargetItem_list = []
    for json_item in json_items['Items']:
        TargetItem_list.append(TargetItem.parse_json_to_item(json_dict=json_item))
    return TargetItem_list


def parse_name_dict_to_dict(json_dict: dict) -> dict:
    '''Parses a list of dictionaries from:
                        {key - "Name":"tradeLock", value - "Value":"0"}, ...
                    to: {key:"tradeLock":"0"} '''
    return {attribute['Name']: attribute['Value'] for attribute in json_dict}


