'''This module contains the row class which represents a row in a CLI chart'''

from common.formatting import format_floats_to_usd


class BasicTable:
    '''This class represents a row in a CLI chart'''

    def __init__(self, rows_list):
        self.rows = rows_list

    @classmethod
    def parse_jsons_to_table(cls, content) -> list:
        '''This function is used to parse jsons to a table'''
        raise NotImplementedError

    @classmethod
    def parse_jsons_to_purchese_table_from_date(cls, content: dict, date: str) -> list:
        '''
        This function is used to parse jsons to a table
        but only including purchases from the stated date
        Used only on PurchaseTable
        '''
        raise NotImplementedError

    def get_last_row(self, headers):
        '''creates last row (the totals) of a table'''
        last_row = ['']*len(headers)
        last_row[0] = "TOTAL:"
        last_row[headers.index("amount")] = self.sum_items_attributes("amount")
        last_row[headers.index("total_price")] = self.sum_items_attributes(
            "total_price")
        last_row = format_floats_to_usd(last_row)
        return last_row

    def sum_items_attributes(self, attribute):
        return sum(getattr(row, attribute) for row in self.rows)
