'''This module contains all the parsing done in the program'''
import json
from item import Item
from row import Row


# def string_to_asset_id(item_name):
#     for 

def buy_order_body(amount, price, asset_id):
    '''lksjdhflasj'''
    item_order = {"Offers": [
                {
                    "AssetID": asset_id,
                    "Price": {
                            "Currency": "USD",
                            "Amount": price
                            }
                }
            ]}
    for i in range(amount-1):
        item_order['Offers'].append(item_order['Offers'][0])
    return json.dumps(item_order)


def parse_json_to_items(json_list, items_list=None):
    '''uses parse_json_to_item to parse all the items from json'''
    if items_list is None:
        items_list = []
    for json in json_list['Items']:
        items_list.append(parse_json_to_item(json=json))
    return items_list


def parse_json_to_item(json):
    '''parses a JSON into an item'''
    exterior = False
    itemtype = False
    tradelock = False
    unlock_date = False

    item = Item(
      asset_id=json['AssetID'], title=json['Title'], tradable=json['Tradable'],
      trade_lock=['tradeLock'], market_price=json['MarketPrice']['Amount'])

    for attribute in json['Attributes']:

        if attribute['Name'] == 'exterior':
            item.exterior = attribute['Value']
            exterior = True

        elif attribute['Name'] == 'tradeLock':
            item.tradeLock = attribute['Value']
            tradelock = True

        elif attribute['Name'] == 'itemType':
            item.itemType = attribute['Value']
            itemtype = True

        elif attribute['Name'] == 'unlockDate':
            item.unlock_date = attribute['Value']
            unlock_date = True

        if (exterior and itemtype and tradelock and unlock_date):
            break
    return item


def parse_items_to_rows(all_items):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title:
                row.count += 1
                row.total_price += float(row.market_price)
                break
        else:
            rows.append(Row(title=item.title,asset_id=item.asset_id, exterior=item.exterior,
                            market_price=str(item.market_price),
                            count=1, total_price=item.market_price))
    return rows
