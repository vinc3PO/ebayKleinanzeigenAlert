import re
import sys
from datetime import datetime
from math import trunc

from sqlalchemy.orm import Session

from ebAlert import create_logger
from ebAlert.crud.base import crud_link, get_session
from ebAlert.crud.post import crud_post
from ebAlert.ebayscrapping import ebayclass
from ebAlert.telegram.telegramclass import telegram

log = create_logger(__name__)

try:
    import click
    from click import BaseCommand
except ImportError:
    log.error("Click should be installed\npip install click")


@click.group()
def cli() -> BaseCommand:
    pass


@cli.command(help="Fetch new post and send telegramclass notification.")
def start():
    """
    loop through the urls in the database and send message
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(">> Starting Ebay alert @", current_time)
    with get_session() as db:
        get_all_post(db=db, telegram_message=True)
    print("<< Ebay alert finished")


@cli.command(options_metavar="<options>", help="Add/Show/Remove URL from database.")
@click.option("-r", "--remove_link", 'remove', metavar="<link id>", help="Remove link from database.")
@click.option("-c", "--clear", is_flag=True, help="Clear post database.")
@click.option("-a", "--add_url", 'url', metavar='<URL>', help="Add URL to database and fetch posts.")
@click.option("-i", "--init", is_flag=True, help="Initialise database after clearing.")
@click.option("-s", "--show", is_flag=True, help="Show all urls and corresponding id.")
def links(show, remove, clear, url, init):
    """
    cli related to the links. Add, remove, clear, init and show
    """
    # TODO: Add verification if action worked.
    with get_session() as db:
        if show:
            print(">> List of URL")
            links = crud_link.get_all(db)
            if links:
                for link_model in links:
                    print("{0:<{1}}{2}".format(link_model.id, 8 - len(str(link_model.id)), link_model.link))
            print("<< List of URL")
        elif remove:
            print(">> Removing link")
            if crud_link.remove(db=db, id=remove):
                print("<< Link removed")
            else:
                print("<< No link found")
        elif clear:
            print(">> Clearing item database")
            crud_post.clear_database(db=db)
            print("<< Database cleared")
        elif url:
            print(">> Adding url")
            if crud_link.get_by_key(key_mapping={"link": url}, db=db):
                print("<< Link already exists")
            else:
                crud_link.create({"link": url}, db)
                new_link_id = 0
                ebay_items = ebayclass.EbayItemFactory(url)
                # TODO here link ids for new_link_id missing ...
                crud_post.add_items_to_db(db, ebay_items.item_list, new_link_id)
                print("<< Link and post added to the database")
        elif init:
            print(">> Initializing database")
            get_all_post(db)
            print("<< Database initialized")


def get_all_post(db: Session, telegram_message=False):
    searches = crud_link.get_all(db=db)
    if searches:
        for link_model in searches:
            if link_model.status != 0:
                """
                every search has a status
                0 = search disabled
                1 = search active. update db and send messages
                2 = search silent = update db but do not send messages
                """
                # scrape search pages and add new/changed items to db
                print(f'Searching ID:{link_model.id}: Type \'{link_model.search_type}\', filter \'{link_model.search_string}\', range: {link_model.price_low}€ - {link_model.price_high}€')
                post_factory = ebayclass.EbayItemFactory(link_model)
                message_items = crud_post.add_items_to_db(db=db, items=post_factory.item_list, link_id=link_model.id, simulate=False)
                if link_model.status == 1:
                    # check for items worth sending and send
                    if len(message_items) > 0:
                        filter_message_items(link_model, message_items, telegram_message=telegram_message)
                    else:
                        print('Nothing to report')
                else:
                    # end output
                    print('Silent')


def filter_message_items(link_model, message_items, telegram_message):
    print('Telegram:', end=' ')
    for item in message_items:
        worth_messaging = False
        # current price as integer
        item_price = item.price
        item_price_num = re.findall(r'\d+', re.sub("\.", "", item_price))
        if len(item_price_num) == 0:
            item_price_num = 0
        else:
            item_price_num = int(item_price_num[0])
        # pricerange visual indicator
        pricerange= ""
        if int(link_model.price_low) <= item_price_num <= int(link_model.price_high):
            pricediff = int(link_model.price_high) - int(link_model.price_low)
            pricepos = round((item_price_num - int(link_model.price_low))*10/pricediff)
            for x in range(0, 11):
                if x == pricepos:
                    pricerange += "X"
                else:
                    pricerange += "."
        else:
            pricerange = "......."
        pricerange = " [" + pricerange + "] "
        item.pricerange = f"{link_model.price_low}€{pricerange}{link_model.price_high}€"
        # TODO hardcoded flag here and both over and underrange hints
        # maximal item price to be shown
        price_max = round(int(link_model.price_high) * 1.2)
        if (price_max - link_model.price_high) > 20:
            price_max = link_model.price_high + 20
        # CHECK if message worth sending
        if item_price_num <= 1:
            # price is 0 or 1
            worth_messaging = True
            print('V', end='')
        elif int(link_model.price_low) <= item_price_num <= int(link_model.price_high):
            # price within range
            worth_messaging = True
            print('!', end='')
        elif int(link_model.price_high) < item_price_num <= price_max \
                and "VB" in item_price:
            # price is negotiable and max 20% over watching price max 20€
            item.pricehint = f"(+20%)"
            worth_messaging = True
            print('h', end='')
        elif int(link_model.price_low) * 0.7 <= item_price_num < int(link_model.price_low):
            # price is 30% below watch price
            item.pricehint = f"(-30%)"
            worth_messaging = True
            print('l', end='')
        # send telegram
        if worth_messaging and telegram_message:
            telegram.send_formated_message(item)
    print('')
"""
IDEAS:
prepare vor search only having max price for example
make searches go to individual chat ids
make db much more detailed: product categories + filters prepare URLs and are referenced by serach_type

MAYBE: react to a telegram message marks the item as favored in ebay and sends the seller a text?
"""


if __name__ == "__main__":
    cli(sys.argv[1:])
