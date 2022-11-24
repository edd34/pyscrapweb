from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.parse import urlparse

class Scrap:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth
        self.domain = urlparse(url).geturl()
        self.html_content = None
        self.soup = None
        self.links = []
        self._get_html_from_url()

    def _get_html_from_url(self):
        res = requests.get(self.url)
        if not res.ok:
            return None
        self.soup = BeautifulSoup(res.text, 'lxml')
        self.html = res.text
        return self.html

    def get_link_from_html(self):
        result = []
        if not self.soup:
            return []
        links = self.soup.find_all('a')

        for l in links:
            link = l.get('href')
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
            if i.has_attr( "class" ):
                if len( i['class'] ) != 0:
                    class_list.append(" ".join( i['class']))
        return class_list