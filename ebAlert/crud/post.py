from typing import List

from sqlalchemy.orm import Session

from ebAlert.crud.base import CRUBBase
from ebAlert.ebayscrapping.ebayclass import EbayItem
from ebAlert.models.sqlmodel import EbayPost


class CRUDPost(CRUBBase):

    def add_items_to_db(self, items: List[EbayItem], db: Session):
        add_items = []
        for item in items:
            if not self.get_by_key({"post_id": str(item.id)}, db):
                self.create({"post_id": item.id}, db=db)
                add_items.append(item)
        return add_items


crud_post = CRUDPost(EbayPost)
