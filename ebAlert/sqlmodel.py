from contextlib import contextmanager
import logging
import os
from ebAlert.ebayclass import getPost

try:
    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
except ImportError:
    print("SQLAlchemy should be installed\npip install sqlalchemy")

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
def getSession():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(e)
    finally:
        session.close()



def postExist(post_id):
    with getSession() as db:
        result = db.query(EbayPost).filter(EbayPost.post_id == post_id).first()
        return bool(result)



def addPost(post_list=None):
    with getSession() as db:
        if post_list is not None:
            for post in post_list:
                newPost = EbayPost()
                newPost.post_id = post.id
                newPost.link = post.link
                newPost.price = post.price
                newPost.title = post.title
                db.add(newPost)



def addLink(link):
    with getSession() as db:
        newLink = EbayLink()
        newLink.link = link
        db.add(newLink)


def getLinks():
    with getSession() as db:
        result = db.query(EbayLink).all()
        links = []
        for row in result:
            links.append(row.__dict__)
        return links

def removeLink(linkId):
    with getSession() as db:
        result = db.query(EbayLink).filter(EbayLink.id==linkId).first()
        db.delete(result)

def clearPostDatabase():
    with getSession() as db:
        result = db.query(EbayPost)
        result.delete()



if __name__ == "__main__":
    list = getPost("https://www.ebay-kleinanzeigen.de/s-weener/preis::250/lenovo/k0l2744r20")
    #addLink(https://www.ebay-kleinanzeigen.de/s-weener/preis::250/thinkpad/k0l2744r20")