from typing import Generator

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from random import randint
from time import sleep

from ebAlert import create_logger
from ebAlert.core.config import settings

log = create_logger(__name__)


class EbayItem:
    """Class ebay item"""
    def __init__(self, contents: Tag):
        self.contents = contents
        self.old_price = ""
        self.pricehint = ""
        self.pricerange = ""
        self.distance = ""

    @property
    def link(self) -> str:
        if self.contents.a.get('href'):
            return settings.URL_BASE + self.contents.a.get('href')
        else:
            return "No url found."

    @property
    def shipping(self) -> str:
        if self.distance == "":
            return self._find_text_in_class("aditem-main--middle--price-shipping--shipping") or "No Shipping"
        else:
            return self.distance

    @property
    def title(self) -> str:
        return self._find_text_in_class("ellipsis") or "No Title"

    @property
    def price(self) -> str:
        return self._find_text_in_class("aditem-main--middle--price-shipping--price") or "No Price"

    @property
    def print_price(self) -> str:
        print_price = self.price
        if self.old_price != "":
            print_price = "NEW:" + self.old_price + " --> " + print_price
        if self.pricehint != "":
            print_price += " " + self.pricehint
        print_price += "\n" + self.pricerange
        return print_price

    @property
    def description(self) -> str:
        description = self._find_text_in_class("aditem-main--middle--description")
        if description:
            return description.replace("\n", " ")
        else:
            return "No Description"

    @property
    def id(self) -> int:
        return int(self.contents.get('data-adid')) or 0

    @property
    def location(self):
        return self._find_text_in_class("aditem-main--top--left") or "No location"

    def __repr__(self):
        return '{}; {}; {}'.format(self.title, self.city, self.price)

    def _find_text_in_class(self, class_name: str):
        found = self.contents.find(attrs={"class": f"{class_name}"})
        if found:
            return found.text.strip()


class EbayItemFactory:
    def __init__(self, link_model):
        self.item_list = []
        npage_max = settings.MAX_PAGESTOSCRAPE
        npage_found = 1
        npage = 1
        while 0 < npage <= npage_max:
            web_page_soup = self.get_webpage(self.generate_url(link_model, npage))
            if web_page_soup:
                articles = self.extract_item_from_page(web_page_soup)
                self.item_list += [EbayItem(article) for article in articles]
                npage_found = len(web_page_soup.find(attrs={"class": "pagination-pages"}).find_all())
                if npage < npage_found and npage <= npage_max:
                    npage += 1
                    sleep(randint(0, 30) / 10)
                else:
                    npage = 0
            else:
                npage = 0

    @staticmethod
    def generate_url(link_model, npage=1) -> str:
        # generate url from DB using URL placeholders: {NPAGE} {SEARCH_TERM}
        current_page = ""
        if npage > 1:
            current_page = "seite:" + str(npage) + "/"
        search_term = ""
        if link_model.search_string != "":
            search_term = link_model.search_string.replace(" ", "-") + "/"
        # currently price is not considered in getting the results, articles are filtered later
        url = settings.URL_BASE
        url += getattr(settings, "URL_TYPE_"+link_model.search_type).format(SEARCH_TERM=search_term, NPAGE=current_page)
        print(url)
        return url

    @staticmethod
    def get_webpage(url: str) -> BeautifulSoup:
        custom_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
        }
        response = requests.get(url, headers=custom_header)
        if response and response.status_code == 200:
            cleaned_response = response.text.replace("&#8203", "")
            soup = BeautifulSoup(cleaned_response, "html.parser")
            return soup
        else:
            print(f"<< webpage fetching error for url: {url}")

    @staticmethod
    def extract_item_from_page(soup:BeautifulSoup) -> Generator:
        result = soup.find(attrs={"id": "srchrslt-adtable"})
        if result:
            for item in result.find_all(attrs={"class": "ad-listitem lazyload-item"}):
                if item.article:
                    yield item.article