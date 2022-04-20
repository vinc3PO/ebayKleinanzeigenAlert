from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ebAlert import create_logger
from ebAlert.core.config import settings

log = create_logger(__name__)


engine = create_engine(f'sqlite:///{settings.FILE_LOCATION}', echo=False, future=True)
Base = declarative_base()

Session = sessionmaker(bind=engine, future=True)
