'''This module contains all the parsing done in the program'''
from item import Item
from row import Row


def parse_json_to_items(json_list):
    '''uses parse_json_to_item to parse all the items from json'''
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
      trade_lock=['tradeLock'], market_price=json['Offer']['Price']['Amount'])

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
            return item


def parse_items_to_rows(all_items):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title:
                row.count += 1
                break
        else:
            rows.append(Row(title=item.title, exterior = item.exterior, market_price = item.market_price, count = 1))
    return rows