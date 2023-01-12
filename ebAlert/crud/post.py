from typing import List

from sqlalchemy.orm import Session

from ebAlert.crud.base import CRUBBase
from ebAlert.ebayscrapping.ebayclass import EbayItem
from ebAlert.models.sqlmodel import EbayPost


class CRUDPost(CRUBBase):

    def add_items_to_db(self, items: List[EbayItem], db: Session, link_id: int, simulate=False) -> List[EbayItem]:
        new_items = []
        print("Working:", end=' ')
        for item in items:
            db_result = self.get_by_key({"post_id": str(item.id)}, db)
            if not db_result:
                # new article
                print("C", end='')
                if not simulate:
                    self.create({"post_id": str(item.id), "price": item.price, "link_id": link_id}, db=db)
                new_items.append(item)
            else:
                # transition to saving link id in offers
                if str(getattr(db_result, "link_id")) == "":
                    print("c", end='')
                    if not simulate:
                        self.update({"post_id": str(item.id), "link_id": link_id}, db=db)
                    item.old_price = old_price
                    new_items.append(item)
                # there was a different price before, update it and inform
                old_price = str(getattr(db_result, "price"))
                if old_price != item.price:
                    print("C", end='')
                    if not simulate:
                        self.update({"post_id": str(item.id), "price": item.price}, db=db)
                    item.old_price = old_price
                    new_items.append(item)
        print(" ... OK")
        return new_items


crud_post = CRUDPost(EbayPost)
