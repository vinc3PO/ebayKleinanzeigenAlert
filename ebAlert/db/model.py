from contextlib import contextmanager
import os
from ebAlert import create_logger
import datetime

log = create_logger(__name__)

try:
    from sqlalchemy import create_engine, func
    from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship, joinedload
except ImportError:
    log.error("SQLAlchemy should be installed\npip install sqlalchemy")

FILELOCATION = os.path.join(os.path.expanduser("~"), "ebayklein.db")
engine = create_engine('sqlite:///{!s}'.format(FILELOCATION), echo=False)
Base = declarative_base()


class TelegramBot(Base):
    __tablename__ = "telegram_bot"

    id = Column(Integer, primary_key=True)
    token = Column(String)
    chat_id = Column(Integer)
    comment = Column(String)

    link = relationship("EbayLink")


class EbayLink(Base):
    __tablename__ = "ebay_link"

    id = Column(Integer, primary_key=True)
    link = Column(String)
    bot_id = Column(Integer, ForeignKey(TelegramBot.id))

    bot = relationship("TelegramBot")


class EbayPost(Base):
    __tablename__ = "ebay_post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    post_id = Column(Integer)
    link = Column(String)
    date = Column(DateTime, default=func.now())
    search_id = Column(Integer, ForeignKey(EbayLink.id))

    search = relationship("EbayLink")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

