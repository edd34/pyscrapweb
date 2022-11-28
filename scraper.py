from bs4 import BeautifulSoup
from bs4.element import ResultSet
import requests
from requests import Response
from urllib.parse import urljoin
from urllib.parse import urlparse
from typing import Optional


class Scrap:
    def __init__(self, url, depth):
        self.url: str = url
        self.depth: int = depth
        self.domain: str = urlparse(url).geturl()
        self.html_content: Optional[str] = None
        self.soup: Optional[BeautifulSoup] = None
        self.links = []
        self._get_html_from_url()

    def _get_html_from_url(self) -> Optional[str]:
        res: Response = requests.get(self.url)
        if not res.ok:
            return None
        self.soup = BeautifulSoup(res.text, "lxml")
        self.html: str = res.text
        return self.html

    def get_link_from_html(self) -> list[str]:
        result: list[str] = []
        if not self.soup:
            return []
        links: ResultSet = self.soup.find_all("a")

        for l in links:
            link = l.get("href")
            if link and "mailto" in link:
                continue
            if link and not str(link).startswith("http"):
                link = urljoin(self.domain, link)

                result.append(link)
        self.links = result
        return result

    def get_attribute(self, name):
        return [tag for tag in self.soup.find_all() if tag.has_attr(name)]

    def get_classes(self, name):
        class_list = []
        for tag in self.soup.find_all():
            if i.has_attr("class"):
                if len(i["class"]) != 0:
                    class_list.append(" ".join(i["class"]))
        return class_list
