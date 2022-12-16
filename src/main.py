'''This module contains the main loop of the program and prints'''

import click
from commands.view import view
from commands.delete import delete
from commands.create import create

@click.group()
def commands():
    '''This is an API wrapper to DMarket. \n
    In this version you create, delete and view listings and items'''


commands.add_command(view)
commands.add_command(delete)
commands.add_command(create)

if __name__ == '__main__':
    commands()
