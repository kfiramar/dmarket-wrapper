'''This module contains all the parsing done in the program'''
import json
import pprint
import time
import os
from typing import List
from types import SimpleNamespace
from item import Item
from row import Row


SRC_PATH= os.path.dirname(__file__)
JSON_DICTIONARY_FIXER = {"\'": "\"" ,'True': '\"True\"',' False': '\"False\"','None':'\"None\"'}

def json_fixer(json: dict):
    '''changes the everything to the json convention'''
    for key, value in JSON_DICTIONARY_FIXER.items():
        json = json.replace(key, value)
    return json

# Creates a file and loads all the API request result into it
def write_content(content):
    '''debugging if you want to know how the recived JSON is built'''
    file_name = time.strftime("request_%Y-%m-%d_%H:%M:%S.json")
    path_to_file = os.path.join(SRC_PATH, f'../logs/{file_name}')
    fixed_json = json.loads(json_fixer(str(content.json())))
    with open(path_to_file,"wb") as file:  
        file.write((pprint.pformat(fixed_json).replace("'", '"')).encode("UTF-8"))



def buy_order_body(amount : int, price : float, asset_ids : List):
    '''generate body for buy order'''
    item_order = {"Offers": []}
    for i in range(amount):
        curr_order = {
                    "AssetID": asset_ids.pop(0),
                    "Price": {
                            "Currency": "USD",
                            "Amount": price
                            }
                }
        item_order['Offers'].append(curr_order)
    return item_order

def parse_json_to_items(json_list : dict):
    '''uses parse_json_to_item to parse all the items from json'''
    items_list = []
    for json_item in json_list['Items']:
        items_list.append(parse_json_to_item(json=json_item))
    return items_list


def parse_json_to_object(json_object : List):
    '''used to parse from json to item'''
    return json.loads(json_object, object_hook=lambda d: SimpleNamespace(**d))



def parse_json_to_item(json: dict):
    '''parses a JSON into an item'''
    unlock_date = exterior = itemtype = False
    if json['Offer']['OfferID'] == '':
        item = Item(
        asset_id=json['AssetID'], title=json['Title'], tradable=json['Tradable'], market_price=json['MarketPrice']['Amount'])
        for attribute in json['Attributes']:

            if attribute['Name'] == 'exterior':
                item.exterior = attribute['Value']
                exterior = True

            elif attribute['Name'] == 'itemType':
                item.itemType = attribute['Value']
                itemtype = True

            elif attribute['Name'] == 'unlockDate':
                item.unlock_date = attribute['Value']
                unlock_date = True

            if (exterior and itemtype and unlock_date):
                return item

    return Item(
        asset_id=json['AssetID'], title=json['Title'], tradable=json['Tradable'], market_price=float(json['Offer']['Price']['Amount']))


def parse_items_to_rows(all_items : List):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title and item.market_price == row.market_price:
                row.count += 1
                row.total_price += float(row.market_price)
                row.asset_ids.append(item.asset_id)
                break
        else:
            rows.append(Row(title=item.title,asset_ids=item.asset_id, exterior=item.exterior,
                            market_price=item.market_price,
                            count=1, total_price=item.market_price))
    return rows
