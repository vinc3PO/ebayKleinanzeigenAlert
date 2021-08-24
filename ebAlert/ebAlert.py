from ebAlert.ebayscrapping import ebayclass
from ebAlert.db import dbutils, schema
from ebAlert.telegram import telegramclass
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
    if not dbutils.get_telegram_bot():
        raise telegramclass.TelegramBotError

    links = dbutils.get_links()
    if links:
        for link in links:
            print("Processing link - id: {} - link: {} ".format(link.id, link.link))
            sleep(randint(0, 10))
            add_post(link.link, link.bot, True)
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
        links = dbutils.get_links()
        if links:
            print("id     link (bot_id)")
            for link in links:
                print("{0:<{1}}{3} ({2})".format(link.id, 8 - len(str(link.id)), link.bot.id, link.link))
    elif remove:
        dbutils.remove_link(remove)
        print("Link removed")
    elif clear:
        dbutils.clear_post_database()
        print("Post database cleared")
    elif add:
        bots = dbutils.get_telegram_bot()
        if bots:
            if len(bots) > 1:
                print("id     description <token>")
                for bot in bots:
                    print("{0:<{1}}{2} <{3}>".format(bot.id,
                                                     8 - len(str(id)),
                                                     bot.comment,
                                                     bot.token))
                bot_id = input("Bot id? ")
            else:
                bot_id = bots[0].id
        else:
            raise telegramclass.TelegramBotError
        dbutils.add_link(add, bot_id)
        add_post(add)
        print("Link and post added to the database")
    elif init:
        links = dbutils.get_links()
        if links:
            for link in links:
                add_post(link.link)
            print("database initialised")
    else:
        print("Help available with ebAlert links --help")


@cli.command(options_metavar="<options>", help="Add/Show/Remove telegram bot from database.")
@click.option("-r","--remove_bot", 'remove', metavar="<bot id>", help="Remove bot from database.")
@click.option("-a", "--add_bot", is_flag=True, help="Add bot to database.")
@click.option("-s", "--show", is_flag=True, help="Show all bot token, chat_id and comment.")
def telegram(show, add_bot,  remove):
    """
    cli related to the links. Add, remove, clear, init and show
    """
    #TODO: Add verification if action worked.
    if show:
        bots = dbutils.get_telegram_bot()
        if bots:
            print("id     description <chat_id : token>")
            for bot in bots:
                print("{0:<{1}}{2} <{3} : {4}>".format(bot.id, 8 - len(str(id)), bot.comment, bot.chat_id, bot.token))
    elif remove:
        dbutils.remove_telegram_bot(remove)
        print("Bot removed")
    elif add_bot:
        # token, chat_id, comment = add
        token = input("Telegram token: ")
        chat_id = input("Telegram chat ID: ")
        comment = input("Telegram bot description: ")
        dbutils.add_telegram_bot(token, chat_id, comment)
        print("Telegram bot added added to the database")
    else:
        print('Help available with ebAlert telegram --help')


def add_post(link, bot=None, toSend=False):
    """
    Function to fetch ebayclass posts, check the database and send telegramclass if new
    :param link: string, bot [token, chat_id]
    :param toSend: boolean
    :return: None
    """
    posts = ebayclass.get_post(link)
    for post in posts:
        if not dbutils.post_exist(post.id):
            dbutils.add_post([post])
            if toSend:
                try:
                    telegramclass.send_message("{}\n\n{} ({})\n\n{}".format(post.title,
                                                                            post.price,
                                                                            post.city,
                                                                            post.link),
                                                bot)
                except Exception as e:
                    log.error(f"Error while sending message for url ({post.link}) with the following error: {e}")


if __name__ == "__main__":
    cli(sys.argv[1:])
