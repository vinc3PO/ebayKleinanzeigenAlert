from contextlib import contextmanager
import os
from . import create_logger
from typing import List

log = create_logger(__name__)

try:
    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
except ImportError:
    log.error("SQLAlchemy should be installed\npip install sqlalchemy")

FILELOCATION = os.path.join(os.path.expanduser("~"), "ebayklein.db")
engine = create_engine('sqlite:///{!s}'.format(FILELOCATION), echo=False)
Base = declarative_base()


class EbayPost(Base):
    __tablename__ = "ebay_post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    post_id = Column(Integer)
    link = Column(String)


class EbayLink(Base):
    __tablename__ = "ebay_link"

    id = Column(Integer, primary_key=True)
    link = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

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
                newPost = EbayPost()
                newPost.post_id = post.id
                newPost.link = post.link
                newPost.price = post.price
                newPost.title = post.title
                db.add(newPost)


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


def remove_link(linkId):
    with get_session() as db:
        result = db.query(EbayLink).filter(EbayLink.id == linkId).first()
        db.delete(result)


def clear_post_database():
    with get_session() as db:
        result = db.query(EbayPost)
        result.delete()

