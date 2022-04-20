import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from ebAlert.crud.base import crud_link
from ebAlert.crud.post import crud_post
from ebAlert.models.sqlmodel import Base, EbayLink, EbayPost


@pytest.fixture
def db():
    engine = create_engine('sqlite://', echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    db = Session()
    for i in range(1, 5):
        link = EbayLink(
            id=i,
            link=f'link_{i}'
        )
        post = EbayPost(
            id=i,
            post_id=i * 1000
        )
        db.add(link)
        db.add(post)
        db.commit()
    yield db
    db.close()


def test_crud_base_get_all(db):
    result = crud_link.get_all(db=db)
    assert len(result) == 4


def test_crud_base_get_by_key(db):
    # test correct
    result_ok = crud_link.get_by_key(key_mapping={"link": "link_3"}, db=db)
    assert result_ok.id == 3
    # test link doesn't exists
    result_2 = crud_link.get_by_key(key_mapping={"link": "link_23"}, db=db)
    assert result_2 is None
    # test wrong wrong keyword
    result_3 = crud_link.get_by_key(key_mapping={"lind": "link_3"}, db=db)
    assert result_3 is None


def test_crud_base_create(db):
    # test correct
    result = crud_link.create(items={"link": "link_8"}, db=db)
    assert result.id == 5
    # test wrong keyword
    result_2 = crud_link.create(items={"links": "link_8"}, db=db)
    assert result_2 is None


def test_crud_base_remove(db):
    # test exists
    result = crud_link.remove(id=1, db=db)
    assert result is True
    assert db.get(EbayLink, 1) is None
    # test doesn't exists
    result_2 = crud_link.remove(id=32, db=db)
    assert result_2 is None


def test_crud_base_clear_database(db):
    result = crud_link.clear_database(db=db)
    assert result is None
    assert db.get(EbayLink, 1) is None
    assert db.execute(select(EbayLink)).scalars().all() == []


def test_crud_post_add_list_items(db):
    items = [type('test', (), {"id": i})() for i in range(1, 5)]
    result = crud_post.add_items_to_db(items=items, db=db)
    assert len(result) == 4
    assert len(db.execute(select(EbayPost)).scalars().all()) == 8


if __name__ == "__main__":
    pass
