import re
from typing import Generator

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from ebAlert import create_logger
from ebAlert.core.config import settings

log = create_logger(__name__)


class EbayItem:
    """Class ebay item"""
    def __init__(self, contents: Tag):
        self.contents = contents
        self._city = None
        self._distance = None
        self._extract_city_distance()

    @property
    def link(self) -> str:
        if self.contents.a.get('href'):
            return settings.URL_BASE + self.contents.a.get('href')
        else:
            return "No url found."

    @property
    def title(self) -> str:
        return self._find_text_in_class("ellipsis") or "No Title"

    @property
    def price(self) -> str:
        return self._find_text_in_class("aditem-main--middle--price-shipping--price") or "No Price"

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
    def city(self):
        return self._city or "No city"

    @property
    def distance(self):
        return self._distance

    def __repr__(self):
        return '{}; {}; {}'.format(self.title, self.city, self.distance)

    def _find_text_in_class(self, class_name: str):
        found = self.contents.find(attrs={"class": f"{class_name}"})
        if found:
            return found.text.strip()

    def _extract_city_distance(self):
        details_list = self._find_text_in_class("aditem-main--top--left")
        if details_list:
            split_detail = details_list.split("\n")
            if len(split_detail) == 1:
                self._city = split_detail[0]
            else:
                split_detail = [detail.strip() for detail in split_detail]
                self._city = split_detail[0]
                self._distance = split_detail[1]


class EbayItemFactory:
    def __init__(self, link):
        self.link = link
        web_pages = self.get_webpage()
        if web_pages:
            articles = self.extract_item_from_page(self.get_webpage())
            self.item_list = [EbayItem(article) for article in articles]
        else:
            self.item_list = []

    def get_webpage(self) -> str:
        custom_header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
        }
        response = requests.get(self.link, headers=custom_header)
        if response and response.status_code == 200:
            return response.text
        else:
            print(f"<< webpage fetching error for url: {self.link}")

    @staticmethod
    def extract_item_from_page(text: str) -> Generator:
        cleaned_response = text.replace("&#8203", "")
        soup = BeautifulSoup(cleaned_response, "html.parser")
        result = soup.find(attrs={"id": "srchrslt-adtable"})
        if result:
            for item in result.find_all(attrs={"class": re.compile("ad-listitem.*")}):
                if item.article:
                    yield item.article
