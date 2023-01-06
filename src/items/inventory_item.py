'''
This module contains the InventoryItem class (which is a subclass of BasicItem)
InventoryItem represends an Inventory item on DMarket
'''

from items.basic_item import BasicItem


class InventoryItem(BasicItem):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''

    def __init__(self, asset_id, title, tradable, market_price,
                 item_type, exterior, unlock_date):
        self.tradable = tradable
        self.item_type = item_type
        self.unlock_date = unlock_date
        self.exterior = exterior
        self.asset_id = asset_id
        super().__init__(title, market_price)

    @classmethod
    def parse_json_to_item(cls, json_dict: dict):
        '''parses a JSON into an InventoryItem'''
        attributes_dictionary = parse_name_dict_to_dict(
            json_dict['Attributes'])
        return cls(
            asset_id=json_dict['AssetID'],
            title=json_dict['Title'],
            tradable=str(json_dict['Tradable']),
            market_price=json_dict['MarketPrice']['Amount'],
            exterior=attributes_dictionary['exterior'],
            item_type=attributes_dictionary['itemType'],
            unlock_date=attributes_dictionary['unlockDate'])


def parse_jsons_to_items_list(json_items: dict) -> list:
    '''parses json items to InventoryItem list'''
    inventoryitem_list = []
    for json_item in json_items['Items']:
        inventoryitem_list.append(
            InventoryItem.parse_json_to_item(json_dict=json_item))
    return inventoryitem_list


def parse_name_dict_to_dict(json_dict: dict) -> dict:
    '''Parses a list of dictionaries from:
                        {key - "Name":"tradeLock", value - "Value":"0"}, ...
                    to: {key:"tradeLock":"0"} '''
    return {attribute['Name']: attribute['Value'] for attribute in json_dict}
