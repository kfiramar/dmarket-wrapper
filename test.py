'''shit'''
import click


@click.group()
def mycommands():
    pass

@click.command()
@click.option("--name", prompt="enter your name", help="banana")
def blaa(name):
    '''test'''
    # name = click.prompt('Please enter a valid str', type=str)
    click.echo(f"hellm {name}")
    
    
    
@click.command('blaaa')
@click.option("--name", prompt="enter your name", help="banana")
def blaaa(name):
    '''test'''
    # name = click.prompt('Please enter a valid str', type=str)
    click.echo(f"hellm {name}")


mycommands.add_command(blaa)
mycommands.add_command(blaaa)

if __name__ == "__main__":
    mycommands()
