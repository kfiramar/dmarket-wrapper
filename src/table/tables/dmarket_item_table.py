'''This module contains the row class which represents a row in a CLI chart'''

from items.dmrket_item import parse_jsons_to_items_list
from common.formatting import format_floats_to_usd 
from table.tables.basic_table import BasicTable
from table.rows.dmarket_item_row import parse_items_list_to_rows

class DMarketItemTable(BasicTable):
    '''InventoryItemTable represents a table (which is a list of InventoryItemRows)'''

    @classmethod
    def parse_jsons_to_table(cls, content: dict) -> list:
        '''This function is used to parse jsons to a table'''
        dm_items = parse_jsons_to_items_list(content)
        dm_rows = parse_items_list_to_rows(dm_items)
        dm_rows.sort(key=lambda row: getattr(row, 'discount'), reverse=True)
        return cls(dm_rows)
