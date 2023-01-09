import re
import sys

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
    print(">> Starting Ebay alert")
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
                ebay_items = ebayclass.EbayItemFactory(url)
                crud_post.add_items_to_db(db, ebay_items.item_list)
                print("<< Link and post added to the database")
        elif init:
            print(">> Initializing database")
            get_all_post(db)
            print("<< Database initialized")


def get_all_post(db: Session, telegram_message=False):
    searches = crud_link.get_all(db=db)
    if searches:
        for link_model in searches:
            # scrape search pages and add new/changed items to db
            print(f'Processing link ID:{link_model.id} --- searching {link_model.search_type}, search term \'{link_model.search_string}\', display price range: {link_model.price_low} - {link_model.price_high}')
            post_factory = ebayclass.EbayItemFactory(link_model)
            message_items = crud_post.add_items_to_db(db=db, items=post_factory.item_list, simulate=True)
            # filter which new/changed items are to be sent by Telegram
            if telegram_message:
                for item in message_items:
                    price = re.findall(r'\d+', item.price)
                    item_price = item.price
                    worth_messaging = False
                    if len(price) > 0:
                        price = int(price[0])
                        # price value added
                        if price == 1:
                            worth_messaging = True
                        elif int(link_model.price_low) <= price <= int(link_model.price_high):
                            worth_messaging = True
                        elif int(link_model.price_high) < price <= round(int(link_model.price_high)*1.1) \
                                and "VB" in item_price:
                            # price is negotiable and max 10% over watching price
                            item.pricehint = f"(+10% from {link_model.price_high}€)"
                            worth_messaging = True
                        elif int(link_model.price_low)*0.7 > price:
                            # price is 30% below watch price
                            item.pricehint = f"(-30% from {link_model.price_low}€)"
                            worth_messaging = True
                    else:
                        # no price offered
                        worth_messaging = True
                    if worth_messaging:
                        telegram.send_formated_message(item)


if __name__ == "__main__":
    cli(sys.argv[1:])
