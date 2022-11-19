'''
This module contains the InventoryItem class (which is a subclass of BasicItem)
InventoryItem represends an Inventory item on DMarket
'''

from items.basic_item import BasicItem

class DMarketItem(BasicItem):
    '''InventoryItem represents a CS:GO item which is in DMarket inventory'''
    def __init__(self, asset_id, title, tradable, market_price,
                 item_type, discount, amount, exterior = ''):
        self.tradable = tradable
        self.item_type = item_type
        self.exterior = exterior
        self.discount = discount
        self.amount = amount
        super().__init__(asset_id, title, market_price)

    @classmethod
    def parse_json_to_item(cls, json_dict: dict):
        '''parses a JSON into an InventoryItem'''
        item = cls(
                   amount = json_dict['amount'],
                   asset_id = str(json_dict['extra']['inGameAssetID']),
                   title = json_dict['title'],
                   market_price = float(json_dict['price']['USD'])/100,
                   tradable = not bool(json_dict['extra']['tradeLockDuration']),
                   item_type = json_dict['extra']['itemType'],
                   discount = json_dict['discount'])
        if 'exterior' in json_dict['extra']:
            item.exterior = json_dict['extra']['exterior']
        return item

def parse_jsons_to_items_list(json_items: dict) -> list:
    '''parses json items to InventoryItem list'''
    inventoryitem_list = []
    for json_item in json_items['objects']:
        inventoryitem_list.append(DMarketItem.parse_json_to_item(json_dict=json_item))
    return inventoryitem_list
