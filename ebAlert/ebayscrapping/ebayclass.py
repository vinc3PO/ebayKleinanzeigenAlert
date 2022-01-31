import requests
from bs4 import BeautifulSoup

from ebAlert import create_logger

log = create_logger(__name__)

URL_BASE = "https://www.ebay-kleinanzeigen.de"


class EbayItem:
    """Class ebay item"""
    distance = "??"
    city = "??"
    price = "??"
    description = "??"

    def __init__(self, contents):
        self.contents = [con for con in contents if con != "\n"][0]
        self.link = URL_BASE + self.contents.a.get('href')
        self.title = contents.find("a", {"class": "ellipsis"}).text if contents.find("a", {"class": "ellipsis"}) else ""
        for div in self.contents.findAll("p"):
            if div.attrs.get("class"):
                if "price" in div.attrs["class"][0]:
                    self.price = div.text.strip()
                elif "description" in div.attrs["class"][0]:
                    self.description = div.text.replace("\n", " ")
        self.id = self.contents.get('data-adid')
        self.get_details()

    def __repr__(self):
        return '{}; {}; {}'.format(self.title, self.city, self.distance)

    def get_details(self):
        details_list = self.contents.find_all("div", {'class': "aditem-main--top--left"})
        if details_list and details_list[0] and details_list[0].text:
            details = self.contents.find_all("div", {'class': "aditem-main--top--left"})[0].text.split("\n")
            details = [det.strip() for det in details if det.strip() != ""]
            if len(details) > 1:
                self.distance = details[1]
                self.city = details[0]
            else:
                self.city = details[0]


def get_post(link):
    session = requests.Session()
    custom_header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}
    response = session.get('{}'.format(link),
                           headers=custom_header)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
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

