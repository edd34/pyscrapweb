from bs4 import BeautifulSoup
from scraper import Scrap
from urllib.parse import urljoin
from typing import Iterator
from add_wrapper import Add

def recursive_explore(url: str, depth: int, result: set[str]) -> Iterator[str]:
    if depth == 0:
        return None
    i_scrap = Scrap(url, depth)
    links = i_scrap.get_link_from_html()

    for link in links:
        link = urljoin(i_scrap.domain, link)
        if link in result:
            continue
        yield link
        result.add(link)
        recursive_explore(link, depth - 1, result)


def extract_link_class_id(content_html: str) -> tuple[list[str], list[str], list[str]]:
    soup = BeautifulSoup(content_html, "lxml")
    link_list: list[str] = []
    class_list: list[str] = []
    id_tag_list: list[str] = []
    for tag in soup.find_all():
        if tag.name == "a":
            link_list.append(tag.get("href"))
        if tag.has_attr("id"):
            id_tag_list.append(tag["id"])
        if tag.has_attr("class"):
            if len(tag["class"]) != 0:
                class_list += (" ".join(tag["class"])).split()
    return class_list, link_list, id_tag_list

def _count_occurence(elem, list_elem):
    cpt = 0
    for i in list_elem:
        if i == elem:
            cpt = Add(cpt, 1)
    return cpt

def count_occurence(list_elem: list[str])->dict[str, int]:
    keys = set(list_elem)
    result = {}
    for key in keys:
        result[key] = _count_occurence(key, list_elem)
    return result
