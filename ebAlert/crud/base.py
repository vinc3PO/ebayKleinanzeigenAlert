from contextlib import contextmanager

import ebAlert.models.sqlmodel
from ebAlert import create_logger
from ebAlert.db.db import Session as Session_DB
from ebAlert.models.sqlmodel import EbayPost, EbayLink
from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import select, delete
from typing import Dict, Any

log = create_logger(__name__)


@contextmanager
def get_session():
    session = Session_DB()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        log.error(e)
    finally:
        session.close()


class CRUBBase:
    def __init__(self, model):
        self.model = model

    def get_all(self, db: Session):
        results = db.execute(select(self.model)).scalars().all()
        return results

    def get_by_key(self, key_mapping: Dict[str, str], db: Session):
        clean_dict = self._get_clean_dict(key_mapping)
        try:
            results = db.execute(select(self.model).filter_by(**clean_dict).limit(1)).first()
            return results
        except Exception as e:
            print(type(e))
            return None

    def create(self, items: Dict[str, Any], db: Session):
        clean_dict = self._get_clean_dict(items)
        item = self.model(**clean_dict)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def remove(self, id: int, db: Session):
        item = db.get(self.model, id)
        if item:
            db.delete(item)
            db.commit()
            return item

    def clear_database(self, db: Session):
        item = db.execute(delete(self.model).where(self.model.id >= 0).execution_options(synchronize_session="fetch"))
        db.commit()
        return item

    def _get_clean_dict(self, obj_in: Dict[str, str]):
        new_object = {}
        for key, value in obj_in.items():
            if key in self.model.__dict__.keys():
                new_object[key] = value
        return new_object


crud_link = CRUBBase(EbayLink)
