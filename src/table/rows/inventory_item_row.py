'''
This module contains the InventoryItemRow class (which is a subclass of BasicItem).
InventoryItemRow is based on InventoryItem,
Each row groups all the identical items into the same row.
'''

import typing

from items.inventory_item import InventoryItem
# from table.rows.inventory_item_row import InventoryItemRow
from table.rows.basic_row import BasicRow


class InventoryItemRow(BasicRow):
    '''
    InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory.
    
    Parameters:
    - title (str): Title of the item.
    - asset_ids (list[str]): List of asset IDs belonging to this item.
    - amount (int): Number of items in this row.
    - total_price (float): Total price of all items in this row.
    - exterior (str): Exterior quality of the items in this row.
    - tradable (bool): Whether the items in this row are tradable or not.
    - market_price (float): Market price of the items in this row.
    '''

    def __init__(self, title: str, asset_ids: list[str], amount: int,
                 total_price: float, exterior: str, tradable: bool, market_price: float):

        super().__init__(title, amount, market_price)
        self.asset_ids = asset_ids
        self.total_price = total_price
        self.exterior = exterior
        self.tradable = tradable

    @classmethod
    def item_to_row(cls, item: InventoryItem):
        '''creates a new InventoryItemRow from an InventoryItem'''
        return cls(title=item.title,
                   asset_ids=[item.asset_id],
                   exterior=item.exterior,
                   market_price=item.market_price,
                   amount=1,
                   total_price=item.market_price,
                   tradable=item.tradable)

    def add_to_row(self, item: InventoryItem):
        '''adds an InventoryItem to an existing InventoryItemRow'''
        self.amount += 1
        self.total_price += float(item.market_price)
        self.asset_ids.append(item.asset_id)

    def similar_to_item(self, item: InventoryItem) -> bool:
        '''returns whether an InventoryItem has the same relevant attributes as the InventoryItemRow'''
        return item.title == self.title and item.market_price == self.market_price

    def change_state_body(self, amount: int, price: float) -> dict:
        '''generate body to create a listing'''
        asset_ids = self.asset_ids
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


def parse_items_list_to_rows(all_items: typing.List[InventoryItem]) -> typing.List[InventoryItemRow]:
    '''parses items from list(Items) to list(Rows)'''
    rows = []
    for item in all_items:
        for row in rows:
            if row.similar_to_item(item):
                row.add_to_row(item)
                break
        else:
            rows.append(InventoryItemRow.item_to_row(item))
    return rows
