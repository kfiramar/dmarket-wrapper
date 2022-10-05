'''module that loads all the variables in to the app'''
import click
from .view_commands.View import view_commands


@click.group()
def commands():
    pass


commands.add_command(view_commands)
