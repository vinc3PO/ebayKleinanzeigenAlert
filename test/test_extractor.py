from bs4 import BeautifulSoup

from ebAlert.ebayscrapping.ebayclass import EbayItemFactory, EbayItem


def test_item_extractor():
    with open("./test.html", "r", encoding="UTF-8") as f:
        all_items = [item for item in EbayItemFactory.extract_item_from_page(f.read())]
        assert len(all_items) == 27
        assert all_items[0].attrs["data-adid"] == "2469197759"


def test_ebay_item():
    with open("./test_article.html", "r") as f:
        soup = BeautifulSoup(f.read())
        article = soup.find("article")
        item = EbayItem(article)
        print(item)
        assert item.link == 'https://www.kleinanzeigen.de/s-anzeige/suche-alte-spiele-nintendo-gameboy-sega-playstation-c64-amiga-pc/2469197759-227-8256'
        assert item.id == 2469197759
        assert item.title == 'Suche alte Spiele:Nintendo-GameBoy-Sega-Playstation-C64-Amiga-PC'
        assert item.price == '1.234 € VB'
        assert item.city == '69207 Sandhausen'
        assert item.distance is None
        assert item.description == "Guten Tag,  ich suche alte Videospiele von Nintendo-Game" \
                                   " Boy-Sega-Playstation & PC / Atari..."


if __name__ == "__main__":
    pass
