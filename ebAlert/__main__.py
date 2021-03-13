from ebAlert import ebayclass
from ebAlert import sqlmodel
from ebAlert import telegramclass
import sys
from random import randint
from time import sleep
from ebAlert import create_logger

log = create_logger(__name__)

try:
    import click
except ImportError:
    log.error("Click should be installed\npip install click")


@click.group()
def cli():
    pass


@cli.command(help="Fetch new post and send telegramclass notification.")
def start():
    """
    loop through the urls in the database and send message
    """
    links = sqlmodel.get_links()
    if links:
        for id, link in links:
            print("Processing link - id: {} - link: {} ".format(id, link))
            sleep(randint(0, 10))
            add_post(link, True)
    print("Finished")


@cli.command(options_metavar="<options>", help="Add/Show/Remove URL from database.")
@click.option("-r","--remove_link", 'remove',metavar="<link id>", help="Remove link from database.")
@click.option("-c", "--clear", is_flag=True, help="Clear post database.")
@click.option("-a", "--add_url", 'add', metavar='<URL>', help="Add URL to database and fetch posts.")
@click.option("-i", "--init", is_flag=True, help="Initialise database after clearing.")
@click.option("-s", "--show", is_flag=True,help="Show all urls and corresponding id.")
def links(show, remove, clear, add, init):
    """
    cli related to the links. Add, remove, clear, init and show
    """
    #TODO: Add verification if action worked.
    if show:
        links = sqlmodel.get_links()
        if links:
            for id, link in links:
                print("{0:<{1}}{2}".format(id, 8 - len(str(id)) ,link))
    elif remove:
        sqlmodel.remove_link(remove)
        print("Link removed")
    elif clear:
        sqlmodel.clear_post_database()
        print("Post database cleared")
    elif add:
        sqlmodel.add_link(add)
        add_post(add)
        print("Link and post added to the database")
    elif init:
        links = sqlmodel.get_links()
        if links:
            for id, link in links:
                add_post(link)
            print("database initialised")


def add_post(link, toSend=False):
    """
    Function to fetch ebayclass posts, check the database and send telegramclass if new
    :param link: string
    :param toSend: boolean
    :return: None
    """
    posts = ebayclass.get_post(link)
    for post in posts:
        if not sqlmodel.post_exist(post.id):
            sqlmodel.add_post([post])
            if toSend:
                telegramclass.send_message("{}\n\n{} ({})\n\n{}".format(post.title, post.price, post.city, post.link))


if __name__ == "__main__":
    cli(sys.argv[1:])
