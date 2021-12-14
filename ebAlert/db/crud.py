from contextlib import contextmanager

from ebAlert import create_logger
from ebAlert.db.db import Session
from ebAlert.models.sqlmodel import EbayPost, EbayLink

log = create_logger(__name__)


@contextmanager
def get_session():
    session = Session()
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
        result = db.query(EbayPost).filter(EbayPost.post_id == post_id).first()
        return bool(result)


def add_post(post_list=None):
    with get_session() as db:
        if post_list is not None:
            for post in post_list:
                new_post = EbayPost()
                new_post.post_id = post.id
                new_post.link = post.link
                new_post.price = post.price
                new_post.title = post.title
                db.add(new_post)


def add_link(link):
    with get_session() as db:
        new_link = EbayLink()
        new_link.link = link
        db.add(new_link)


def get_links():
    """
    get link from the database
    :return: [(id, link)]
    """
    with get_session() as db:
        result = db.query(EbayLink).all()
        links = []
        for row in result:
            links.append((row.id, row.link))
        return links


def remove_link(link_id):
    with get_session() as db:
        result = db.query(EbayLink).filter(EbayLink.id == link_id).first()
        db.delete(result)


def clear_post_database():
    with get_session() as db:
        result = db.query(EbayPost)
        result.delete()
