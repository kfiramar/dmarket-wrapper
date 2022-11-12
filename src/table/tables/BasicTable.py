'''This module contains the row class which represents a row in a CLI chart'''

from table.rows.BasicRow import BasicRow

class BasicTable:
    '''This class represents a row in a CLI chart'''
    def __init__(self, rows_list: BasicRow):
        self.rows = rows_list

    @classmethod
    def parse_jsons_to_table(cls, content) -> list:
        raise NotImplementedError

    @classmethod
    def parse_jsons_to_purchese_table_from_date(cls, content: dict, date: str) -> list:
        raise NotImplementedError
    