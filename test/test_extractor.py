from ebAlert.ebayscrapping.ebayclass import EbayItemFactory, EbayItem
from bs4 import BeautifulSoup


def test_item_extractor():
    with open("./test.html", "r", encoding="UTF-8") as f:
        all_items = [item for item in EbayItemFactory.extract_item_from_page(f.read())]
        assert len(all_items) == 24
        assert all_items[0].attrs["data-adid"] == "2015262426"


def test_ebay_item():
    with open("./test_article.html", "r") as f:
        soup = BeautifulSoup(f.read())
        article = soup.find("article")
        item = EbayItem(article)
        print(item)
        assert item.link == 'https://www.ebay-kleinanzeigen.de/s-anzeige/' \
                            'international-soccer-atari-st-3-5-neu-/2015262426-227-21009'
        assert item.id == 2015262426
        assert item.title == 'INTERNATIONAL SOCCER | ATARI ST | 3,5" | NEU |'
        assert item.price == '48 €'
        assert item.city == '01129 Trachau'
        assert item.distance is None
        assert item.description == "Angebot enthält: 1x ATaris St Spiel in Ovp - " \
                                   "Neu (noch Foliert)  Schaut auch in unsere weiteren..."