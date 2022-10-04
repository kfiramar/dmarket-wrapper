'''This module contains all the parsing done in the program'''
import json
import pprint
import time
import os
from typing import List
from types import SimpleNamespace
from item import Listing, InventoryItem
from row import InventoryItemRow, ListingRow


SRC_PATH = os.path.dirname(__file__)
JSON_DICTIONARY_FIXER = {"\'": "\"", 'True': '\"True\"', ' False': '\"False\"', 'None': '\"None\"'}


def json_fixer(json_str: str):
    '''changes the everything to the json convention'''
    for key, value in JSON_DICTIONARY_FIXER.items():
        json_str = json_str.replace(key, value)
    return json_str


# Creates a file and loads all the API request result into it
def write_content(content, client_choice):
    '''debugging if you want to know how the recived JSON is built'''
    fixed_json = []
    file_name = time.strftime(f"request-{client_choice}-%Y-%m-%d_%H:%M:%S.json")
    path_to_file = os.path.join(SRC_PATH, f'../logs/{file_name}')
    if isinstance(content, tuple):
        for cont in content:
            fixed_json.append(json.loads(json_fixer(str(cont.json()))))
    else:
        fixed_json = json.loads(json_fixer(str(content)))
    with open(path_to_file, "wb") as file:
        file.write((pprint.pformat(fixed_json).replace("'", '"')).encode("UTF-8"))


def print_content(content):
    '''debugging if you want to know how the recived JSON is built'''
    print(json.loads(json_fixer(str(content))))


def buy_order_body(amount: int, price: float, asset_ids: List):
    '''generate body for buy order'''
    item_order = {"Offers": []}
    for _ in range(amount):
        buy_order = {
                    "AssetID": asset_ids.pop(0),
                    "Price": {
                            "Currency": "USD",
                            "Amount": price
                            }
                }
        item_order['Offers'].append(buy_order)
    return item_order


def listings_body(amount: int, price: float, asset_ids: List, offer_ids: List):
    '''generate body for buy order'''
    item_order = {
         "force": True,
         "objects": []}
    for _ in range(amount):
        listing = {
                    "itemId": asset_ids.pop(0),
                    "offerId": offer_ids.pop(0),
                    "Price": {
                            "Currency": "USD",
                            "Amount": price
                            }
                }
        item_order['objects'].append(listing)
    return item_order


def listing_error_parsing(responses):
    '''parse list if responses to an error list'''
    error_list = []
    for response in responses:
        for listing in response.json()['Result']:
            if listing['Error'] is not None:
                error_list.append({listing['Error']['Message']})
    return error_list


def parse_jsons_to_inventoryitems(jsons: dict):
    '''uses parse_json_to_item to parse all the items from json'''
    inventoryitem_list = []
    for json_item in jsons['Items']:
        inventoryitem_list.append(parse_json_to_inventoryitem(json_dict=json_item))
    return inventoryitem_list


def parse_jsons_to_listings(jsons: dict):
    '''uses parse_json_to_item to parse all the items from json'''
    listing_list = []
    for json_item in jsons['Items']:
        listing_list.append(parse_json_to_listing(json_dict=json_item))
    return listing_list


def parse_json_to_object(json_object: List):
    '''used to parse from json to item'''
    return json.loads(json_object, object_hook=lambda d: SimpleNamespace(**d))


def parse_json_from_attributes(json_dict, attributes_keys):
    '''Parses '''
    simplified_json_dict = {attribute['Name']: attribute['Value'] for attribute in json_dict}
    return {key: value for key, value in simplified_json_dict.items() if key in attributes_keys}


def parse_json_to_inventoryitem(json_dict: dict):
    '''parses a JSON into an item'''
    attributes_dictionary = parse_json_from_attributes(json_dict['Attributes'], ['exterior', 'itemType', 'unlockDate'])
    # items = [{key:item.get(key,next((item["Value"]for item in item["Attributes"]if item["Name"]==key),None))for key in("itemType","exterior","unlockDate","tradeLock","tradeLockDuration","gameId","AssetID","Title","Tradable")}for item in json_dict]
    return InventoryItem(
                         asset_id=json_dict['AssetID'],
                         title=json_dict['Title'],
                         tradable=str(json_dict['Tradable']),
                         market_price=json_dict['MarketPrice']['Amount'],
                         exterior=attributes_dictionary['exterior'],
                         item_type=attributes_dictionary['itemType'],
                         unlock_date=attributes_dictionary['unlockDate'])


def parse_json_to_listing(json_dict: dict):
    '''parses a JSON into an item'''
    return Listing(
                asset_id=json_dict['AssetID'], title=json_dict['Title'], tradable=str(json_dict['Tradable']),
                listing_price=float(json_dict['Offer']['Price']['Amount']), offer_id=json_dict['Offer']['OfferID'])


def merge_dicts(dictionaries: list):
    '''merge a list of dictionary to one'''
    result_dictionary = dictionaries[0].json()
    for dictionary in dictionaries[1:]:
        result_dictionary = combine_2_dict(result_dictionary, dictionary.json())
    return result_dictionary


def combine_2_dict(dict1, dict2):
    '''merge 2 dictionaries'''
    for key, *value in dict1.items():
        for key2, *value2 in dict2.items():
            if key2 == key and value != value2:
                if (isinstance(value, list) and isinstance(value2, list)):
                    dict1[key2].extend(value2[0])
                elif (isinstance(value, int) and isinstance(value2, int)):
                    dict1[key2] += value2[0]
                elif (isinstance(value, str) and isinstance(value2, str)):
                    dict1[key2] += ', ' + value2[0]
    return dict1


def parse_listings_to_listingrows(all_items: List):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title and item.listing_price == row.listing_price and item.tradable == row.tradable:
                row.total_items += 1
                row.total_price += float(item.listing_price)
                row.asset_ids.append(item.asset_id)
                row.offer_ids.append(item.offer_id)
                break
        else:
            rows.append(ListingRow(title=item.title,
                                   asset_ids=[item.asset_id],
                                   listing_price=item.listing_price,
                                   total_items=1,
                                   total_price=item.listing_price,
                                   offer_ids=[item.offer_id],
                                   tradable=item.tradable))
    return rows


def parse_inventoryitems_to_inventoryitemrow(all_items: List):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title and item.market_price == row.market_price and item.tradable == row.tradable:
                row.total_items += 1
                row.total_price += float(item.market_price)
                row.asset_ids.append(item.asset_id)
                row.total_price = float(row.total_price)
                break
        else:
            rows.append(InventoryItemRow(title=item.title,
                                         asset_ids=[item.asset_id],
                                         exterior=item.exterior,
                                         market_price=item.market_price,
                                         total_items=1,
                                         total_price=item.market_price,
                                         tradable=item.tradable))
    return rows
