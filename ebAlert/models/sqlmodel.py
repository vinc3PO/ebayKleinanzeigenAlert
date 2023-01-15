from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from ebAlert import create_logger
from ebAlert.db.db import Base, engine

log = create_logger(__name__)


class EbayPost(Base):
    __tablename__ = "ebay_post"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    post_id = Column(Integer)
    link_id = Column(Integer)
    date = Column(DateTime(timezone=True), server_default=func.now())


class EbayLink(Base):
    __tablename__ = "ebay_link"

    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    search_type = Column(String)
    search_string = Column(String)
    price_low = Column(Integer)
    price_high = Column(Integer)
    zipcodes = Column(String)


Base.metadata.create_all(engine)
