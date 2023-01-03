'''This module contains the main loop of the program and prints'''

import typer
from commands.view import view
from commands.delete import delete
from commands.create import create, target



main_app = typer.Typer(add_completion=True)
# main_app.enable_auto_complete()

# @main_app.callback()
# def commands(ctx: typer.Context):
#     '''This is an API wrapper to DMarket. \n
#     In this version you create, delete and view listings and items'''
#     print(ctx.invoked_subcommand)


main_app.add_typer(view, name="view", help="viewing listings, inventory -all, dm inventory and steam inventory.")
main_app.add_typer(delete, name="delete",help="deleting listings.")
main_app.add_typer(create, name="create",help="creating listings.")



if __name__ == '__main__':
    # target()
    main_app()
