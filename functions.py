from bs4 import BeautifulSoup
from scraper import Scrap
from urllib.parse import urljoin

def recursive_explore(url, depth, result):
    if depth == 0:
        return
    i_scrap = Scrap(url, depth)
    links = i_scrap.get_link_from_html()
    if not links:
        return
    for link in links:
        link = urljoin(i_scrap.domain, link)
        result.add(link)
        recursive_explore(link, depth-1, result)

def extract_link_class_id(content_html):
    soup = BeautifulSoup(content_html, 'lxml')
    link_list = []
    class_list = []
    id_tag_list = []
    for tag in soup.find_all():
        if tag.name == 'a':
            link_list.append(tag.get("href"))
        if tag.has_attr('id'):
            id_tag_list.append(tag)
        if tag.has_attr( "class" ):
            if len(tag['class']) != 0:
                class_list += (" ".join(tag['class'])).split()
    return class_list, link_list, id_tag_list
