from typing import List

from sqlalchemy.orm import Session

from ebAlert.crud.base import CRUBBase
from ebAlert.ebayscrapping.ebayclass import EbayItem
from ebAlert.models.sqlmodel import EbayPost


class CRUDPost(CRUBBase):

    def add_items_to_db(self, items: List[EbayItem], db: Session, update=False):
        add_items = []
        for item in items:
            db_result = self.get_by_key({"post_id": str(item.id)}, db)
            if not db_result:
                self.create({"post_id": str(item.id), "price": item.price}, db=db)
                add_items.append(item)
            else:
                old_price = str(getattr(db_result, "price"))
                if not old_price:
                    # was there no price before, then write it
                    self.update({"post_id": str(item.id), "price": item.price}, db=db)
                elif old_price != item.price:
                    # was there a different price before, update it and inform
                    self.update({"post_id": str(item.id), "price": item.price}, db=db)
                    item.new_price = "NEW: " + old_price + "  -->  " + item.price
                    add_items.append(item)
        return add_items


crud_post = CRUDPost(EbayPost)
