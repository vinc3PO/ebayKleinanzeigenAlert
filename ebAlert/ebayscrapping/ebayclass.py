import requests
from bs4 import BeautifulSoup

from ebAlert import create_logger

log = create_logger(__name__)

URL_BASE = "https://www.ebay-kleinanzeigen.de"


class EbayItem:
    """Class ebay item"""
    def __init__(self, contents):
        self.contents = [con for con in contents if con != "\n"][0]

    @property
    def link(self) -> str:
        if self.contents.a.get('href'):
            return URL_BASE + self.contents.a.get('href')
        else:
            return "No url found."

    @property
    def title(self) -> str:
        if self.contents.find("a", {"class": "ellipsis"}):
            return self.contents.find("a", {"class": "ellipsis"}).text
        else:
            return "No title found."

    @property
    def price(self) -> str:
        return self.extract_price_detail("price")

    @property
    def description(self) -> str:
        return self.extract_price_detail("description")

    @property
    def id(self) -> int:
        return int(self.contents.get('data-adid')) or 0

    @property
    def city(self):
        return self.extract_city_distance("city")

    @property
    def distance(self):
        return self.extract_city_distance("distance")

    def __repr__(self):
        return '{}; {}; {}'.format(self.title, self.city, self.distance)

    def extract_price_detail(self, key):
        for div in self.contents.findAll("p"):
            if div.attrs.get("class"):
                if key in div.attrs["class"][0]:
                    return div.text.strip().replace("\n", " ")
        return f"No {key} found."

    def extract_city_distance(self, key):
        try:
            details_list = self.contents.find_all("div", {'class': "aditem-main--top--left"})
            if details_list and details_list[0].text:
                details = self.contents.find_all("div", {'class': "aditem-main--top--left"})[0].text.split("\n")
                details = [det.strip() for det in details if det.strip() != ""]
                if key == "city":
                    return details[0]
                elif key == "distance":
                    return details[1]
        except Exception:
            return f"No {key} found." if key == "city" else None


def get_post(link):
    session = requests.Session()
    custom_header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}
    response = session.get('{}'.format(link),
                           headers=custom_header)
    if response.status_code == 200:
        clean_response = response.text.replace("&#8203", "")  # this character breaks the beautiful soup parsing.
        soup = BeautifulSoup(clean_response, "html.parser")
        result = soup.find(attrs={"id": "srchrslt-adtable"})
        if result:
            articles = result.find_all(attrs={"class": "ad-listitem lazyload-item"})
            items = []
            for item in articles:
                try:
                    items.append = EbayItem(item)
                except Exception as e:
                    log.debug(e)
                    pass
            items = [EbayItem(item) for item in articles]
            return items

