try:
    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
except ImportError:
    print("SQLAlchemy should be installed\npip install sqlalchemy")
import sys
import os

from ebAlert.ebayclass import getPost
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


def postExist(post_id):
    session = Session()
    try:
        result = session.query(EbayPost).filter(EbayPost.post_id == post_id).first()
        if result is not None:
            return True
        else:
            return False
    except:
        print(sys.exc_info())
        return False


def addPost(post_list=None):
    session = Session()
    if post_list is not None:
        for post in post_list:
            try:
                newPost = EbayPost()
                newPost.post_id = post.id
                newPost.link = post.link
                newPost.price = post.price
                newPost.title = post.title
                session.add(newPost)
                session.commit()
                return True
            except:
                return False


def addLink(link):
    session = Session()
    try:
        newLink = EbayLink()
        newLink.link = link
        session.add(newLink)
        session.commit()
        return True
    except:
        return False


def getLinks():
    session = Session()
    try:
        result = session.query(EbayLink).all()
        links = []
        for row in result:
            links.append(row.__dict__)
        return links
    except:
        print(sys.exc_info())
        return []

def removeLink(linkId):
    session = Session()
    try:
        result = session.query(EbayLink).filter(EbayLink.id==linkId).first()
        session.delete(result)
        session.commit()
        return True
    except:
        print(sys.exc_info())
        return False

def clearPostDatabase():
    session = Session()
    try:
        result = session.query(EbayPost)
        result.delete()
        session.commit()
        return True
    except:
        print(sys.exc_info())
        return False


if __name__ == "__main__":
    list = getPost("https://www.ebay-kleinanzeigen.de/s-weener/preis::250/lenovo/k0l2744r20")
    #addLink("https://www.ebay-kleinanzeigen.de/s-weener/preis::250/thinkpad/k0l2744r20")