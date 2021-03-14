from contextlib import contextmanager
import os
from ebAlert import create_logger
from ebAlert.db import model, schema

log = create_logger(__name__)

try:
    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship, joinedload
except ImportError:
    log.error("SQLAlchemy should be installed\npip install sqlalchemy")


@contextmanager
def get_session():
    session = model.Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        log.error(e)
    finally:
        session.close()


def post_exist(post_id):
    with get_session() as db:
        result = db.query(model.EbayPost).filter(model.EbayPost.post_id == post_id).first()
        return bool(result)


def add_post(post_list=None):
    with get_session() as db:
        if post_list is not None:
            for post in post_list:
                new_post = model.EbayPost()
                new_post.post_id = post.id
                new_post.link = post.link
                new_post.price = post.price
                new_post.title = post.title
                db.add(new_post)


def add_link(link, bot_id):
    with get_session() as db:
        new_link = model.EbayLink()
        new_link.link = link
        new_link.bot_id = bot_id
        db.add(new_link)


def get_links():
    """
    get link from the database
    :return: [(id, link)]
    """
    with get_session() as db:
        result = db.query(model.EbayLink).options(joinedload(model.EbayLink.bot)).all()
        links = []
        for link in result:
            links.append(schema.Link.from_orm(link))
        return links


def remove_link(link_id):
    with get_session() as db:
        result = db.query(model.EbayLink).filter(model.EbayLink.id == link_id).first()
        db.delete(result)


def clear_post_database():
    with get_session() as db:
        result = db.query(model.EbayPost)
        result.delete()


def get_telegram_bot():
    with get_session() as db:
        result = db.query(model.TelegramBot).all()
        bots = []
        for bot in result:
            bots.append(schema.Bot.from_orm(bot))
        return bots


def add_telegram_bot(token, chat_id, comment):
    with get_session() as db:
        bot = model.TelegramBot(token=token, chat_id=chat_id, comment=comment)
        db.add(bot)


def remove_telegram_bot(bot_id):
    with get_session() as db:
        result = db.query(model.TelegramBot).filter_by(id=bot_id).first()
        db.delete(result)