'''This module contains the row class which represents a row in a CLI chart'''

from items.InventoryItem import parse_jsons_to_items_list
from table.tables.BasicTable import BasicTable
from table.rows.InventoryItemRow import InventoryItemRow, parse_items_list_to_rows

class InventoryItemTable(BasicTable):
    '''InventoryItemRow represents a certain amount of CS:GO item which is in DMarket inventory'''
    def __init__(self, rows_list: InventoryItemRow):
        super().__init__(rows_list)

    @classmethod
    def parse_jsons_to_table(cls, content: dict) -> list:
        '''This function is used to parse jsons to sorted rows'''
        dm_items = parse_jsons_to_items_list(content)
        dm_rows = parse_items_list_to_rows(dm_items)
        dm_rows.sort(key=lambda row: getattr(row, 'total_price'))
        return cls(dm_rows)
