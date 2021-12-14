from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ebAlert import create_logger
from ebAlert.core.config import settings

log = create_logger(__name__)


engine = create_engine('sqlite:///{!s}'.format(settings.FILE_LOCATION), echo=False)
Base = declarative_base()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
