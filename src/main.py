'''This module contains the main loop of the program and prints'''

import typer
from commands.view import view
from commands.delete import delete
from commands.create import create

# @click.group()
# def commands():
#     '''This is an API wrapper to DMarket. \n
#     In this version you create, delete and view listings and items'''


main_app = typer.Typer(add_completion=True)

main_app.add_typer(view, name="view", help="viewing listings, inventory -all, dm inventory and steam inventory.")
main_app.add_typer(delete, name="delete",help="deleting listings.")
main_app.add_typer(create, name="create",help="creating listings.")
# commands.add_command(view)
# commands.add_command(delete)
# commands.add_command(create)

if __name__ == '__main__':
    # commands()
    main_app()
