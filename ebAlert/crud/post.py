from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.util import NoneType

from ebAlert.crud.base import CRUBBase
from ebAlert.ebayscrapping.ebayclass import EbayItem
from ebAlert.models.sqlmodel import EbayPost


class CRUDPost(CRUBBase):

    def add_items_to_db(self, items: List[EbayItem], db: Session, link_id: int, simulate=False) -> List[EbayItem]:
        new_items = []
        print(f'Updating DB on {str(len(items))} items:', end=' ')
        for item in items:
            db_result = self.get_by_key({"post_id": str(item.id)}, db)
            if not db_result:
                # new article
                print("C", end='')
                if not simulate:
                    self.create({"post_id": str(item.id), "price": item.price, "link_id": link_id, "title": item.title}, db=db)
                new_items.append(item)
            else:
                # transition to saving link id in offers
                if type(getattr(db_result, "link_id")) is NoneType:
                    print("u", end='')
                    if not simulate:
                        self.update({"identifier": "post_id", "post_id": item.id, "link_id": link_id}, db=db)
                # there was a different price before, update it and inform
                old_price = str(getattr(db_result, "price"))
                if old_price != item.price:
                    #print(f'U-{item.id}({old_price}->{item.price}) ', end='')
                    print(f'U', end='')
                    if not simulate:
                        self.update({"identifier": "post_id", "post_id": item.id, "price": item.price}, db=db)
                    item.old_price = old_price
                    new_items.append(item)
        print('')
        return new_items


crud_post = CRUDPost(EbayPost)
