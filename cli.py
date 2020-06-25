import app.ebklalert
import click

@click.group()
def cli():
    pass


@cli.command(help="Fetch new post and send Telegram notification.")
def start():
    app.ebklalert.alert()

@cli.command(options_metavar="<options>", help="Add/Show/Remove URL from database.")
@click.option("-r","--remove_link",'remove',metavar="<link id>", help="Remove link from database.")
@click.option("-c", "--clear", is_flag=True, help="Clear post database.")
@click.option("-a", "--add_url", 'add', metavar='<URL>', help="Add URL to database and fetch posts.")
@click.option("-i", "--init", is_flag=True, help="Initialise database after clearing.")
@click.option("-s", "--show", is_flag=True,help="Show all urls and corresponding id.")
def links(show, remove, clear, add, init):
    app.ebklalert.links(show, remove, clear, add, init)



if __name__ == "__main__":
    cli(['--help'])
