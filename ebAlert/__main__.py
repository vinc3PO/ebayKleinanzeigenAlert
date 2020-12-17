from . import ebayclass as ebay
from . import sqlmodel as sql
from . import telegramclass as telegram
import sys
from random import randint
from time import sleep
from . import createLogger

log = createLogger(__name__)

try:
    import click
except ImportError:
    log.error("Click should be installed\npip install click")


@click.group()
def cli():
    pass


@cli.command(help="Fetch new post and send Telegram notification.")
def start():
    """
    loop through the urls in the database and send message
    """
    if sql.getLinks():
        links = [rows["link"] for rows in sql.getLinks()]
        if links:
            for link in links:
                sleep(randint(0, 10))
                addPost(link, True)
    print("Success")


@cli.command(options_metavar="<options>", help="Add/Show/Remove URL from database.")
@click.option("-r","--remove_link",'remove',metavar="<link id>", help="Remove link from database.")
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
        if sql.getLinks():
            links = [(rows["id"], rows["link"])for rows in sql.getLinks()]
            print("id     link")
            if links:
                for id, link in links:
                    print("{0:<{1}}{2}".format(id, 8 - len(str(id)) ,link))
    elif remove:
        sql.removeLink(remove)
        print("Link removed")
    elif clear:
        sql.clearPostDatabase()
        print("Post database cleared")
    elif add:
        sql.addLink(add)
        addPost(add)
        print("Link and post added to the database")
    elif init:
        if sql.getLinks():
            links = [rows["link"] for rows in sql.getLinks()]
            if links:
                for link in links:
                    addPost(link)
            print("database initialised")


def addPost(link, toSend=False):
    """
    Function to fetch ebay posts, check the database and send telegram if new
    :param link: string
    :param toSend: boolean
    :return: None
    """
    posts = ebay.getPost(link)
    for post in posts:
        if not sql.postExist(post.id):
            sql.addPost([post])
            if toSend:
                telegram.sendMessage("{}\n\n{} ({})\n\n{}".format(post.title, post.price, post.city, post.link))


if __name__ == "__main__":
    cli(sys.argv[1:])
