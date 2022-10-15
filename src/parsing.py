'''This module contains all the parsing done in the program'''
from datetime import datetime
from item import Listing, InventoryItem, Purchase
from row import InventoryItemRow, ListingRow, PurcheseRow
TIME_TABLE = {'minute': -3, 'hour': -6, 'day': -9, 'month': -12, 'year': -15}

def parse_jsons_to_rows(json_object, json_to_items_func, items_to_rows_func, sort_by):
    '''This function is used to parse jsons to sorted rows'''
    dm_items = json_to_items_func(jsons=json_object)
    dm_rows = items_to_rows_func(dm_items)
    dm_rows.sort(key=lambda row: getattr(row, sort_by))
    return dm_rows


def parse_jsons_to_purcheserows(json_object, json_to_items_func, items_to_rows_func, sort_by, param):
    '''This function is used to parse jsons to sorted rows'''
    dm_items = json_to_items_func(jsons=json_object)
    dm_rows = items_to_rows_func(dm_items, param)
    dm_rows.sort(key=lambda row: getattr(row, sort_by))
    return dm_rows


def parse_jsons_to_listings(jsons: dict):
    '''uses parse_json_to_item to parse all the items from json'''
    listing_list = []
    for json_item in jsons['Items']:
        listing_list.append(parse_json_to_listing(json_dict=json_item))
    return listing_list


def parse_jsons_to_purchases(jsons: dict):
    '''uses parse_json_to_item to parse all the items from json'''
    listing_list = []
    for json_item in jsons['Trades']:
        listing_list.append(parse_json_to_purchase(json_dict=json_item))
    return listing_list


def parse_json_to_purchase(json_dict: dict):
    '''parses a JSON into a Purchase item'''
    return Purchase(
                asset_id=json_dict['AssetID'],
                title=json_dict['Title'],
                offer_id=json_dict['OfferID'],
                sold_price=float(json_dict['Price']['Amount']),
                offer_closed_at=epoch_time_convertor(json_dict['OfferClosedAt']),
                offer_created_at=epoch_time_convertor(json_dict['OfferCreatedAt']))


def epoch_time_convertor(epoch_time):
    '''afsdf'''
    if epoch_time == '-62135596800':
        return '0001-01-01 00:00:01'
    return datetime.fromtimestamp(int(epoch_time)).strftime('%Y-%m-%d %H:%M:%S')


def parse_purchases_to_purcheserows_merge(all_items: list, merge_by):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if item.title == row.title and item.sold_price == row.sold_price and item.offer_closed_at[:TIME_TABLE[merge_by]] == row.offer_closed_at[:TIME_TABLE[merge_by]]:
                row.total_items += 1
                row.total_price += float(item.sold_price)
                row.asset_ids.append(item.asset_id)
                row.offer_ids.append(item.offer_id)
                break
        else:
            rows.append(PurcheseRow(title=item.title,
                                    asset_ids=[item.asset_id],
                                    sold_price=item.sold_price,
                                    offer_closed_at=item.offer_closed_at,
                                    offer_created_at=item.offer_created_at,
                                    total_items=1,
                                    total_price=item.sold_price,
                                    offer_ids=[item.offer_id]
                                    ))
    return rows


def parse_purchases_to_purcheserows_by_date(all_items: list, date):
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        item_date = datetime.strptime(item.offer_closed_at, '%Y-%m-%d %H:%M:%S')
        if (item_date >= date):
            for row in rows:
                if item.title == row.title and item.sold_price == row.sold_price:
                    row.total_items += 1
                    row.total_price += float(item.sold_price)
                    row.asset_ids.append(item.asset_id)
                    row.offer_ids.append(item.offer_id)
                    break
            else:
                rows.append(PurcheseRow(title=item.title,
                                        asset_ids=[item.asset_id],
                                        sold_price=item.sold_price,
                                        offer_closed_at=item.offer_closed_at,
                                        offer_created_at=item.offer_created_at,
                                        total_items=1,
                                        total_price=item.sold_price,
                                        offer_ids=[item.offer_id]
                                        ))
    return rows


def parse_json_to_listing(json_dict: dict):
    '''parses a JSON into an item'''
    return Listing(
                   asset_id=json_dict['AssetID'],
                   title=json_dict['Title'],
                   tradable=str(json_dict['Tradable']),
                   listing_price=float(json_dict['Offer']['Price']['Amount']),
                   offer_id=json_dict['Offer']['OfferID'])


def parse_listings_to_listingrows(all_items: list):
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


def parse_jsons_to_inventoryitems(jsons: dict):
    '''uses parse_json_to_item to parse all the items from json'''
    inventoryitem_list = []
    for json_item in jsons['Items']:
        inventoryitem_list.append(parse_json_to_inventoryitem(json_dict=json_item))
    return inventoryitem_list


def parse_json_to_inventoryitem(json_dict: dict):
    '''parses a JSON into an item'''
    attributes_dictionary = parse_json_to_attributes(json_dict['Attributes'])
    return InventoryItem(
                         asset_id=json_dict['AssetID'],
                         title=json_dict['Title'],
                         tradable=str(json_dict['Tradable']),
                         market_price=json_dict['MarketPrice']['Amount'],
                         exterior=attributes_dictionary['exterior'],
                         item_type=attributes_dictionary['itemType'],
                         unlock_date=attributes_dictionary['unlockDate'])


def parse_json_to_attributes(json_dict):
    '''Parses a list of dictionaries from:
                        {key - "Name":"tradeLock", value - "Value":"0"}, ...
                    to: {key:"tradeLock":"0"} '''
    return {attribute['Name']: attribute['Value'] for attribute in json_dict}


def parse_inventoryitems_to_inventoryitemrow(all_items: list):
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


def listing_error_parsing(responses):
    '''parse list if responses to an error list'''
    error_list = []
    for response in responses:
        for listing in response.json()['Result']:
            if listing['Error'] is not None:
                error_list.append({listing['Error']['Message']})
    return error_list


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
                if (isinstance(dict1[key], list) and
                        isinstance(dict2[key2], list)):
                    dict1[key2].extend(value2[0])

                elif (isinstance(dict1[key], int) and
                        isinstance(dict2[key2], int)):
                    dict1[key2] += value2[0]

                elif (isinstance(dict1[key], str) and
                        isinstance(dict2[key2], str)):
                    dict1[key2] += ', ' + value2[0]
    return dict1
