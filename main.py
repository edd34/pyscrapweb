from scraper import Scrap
from threads_helpers import thread_consume_page_content, thread_publish_page_content
from urllib.parse import urlparse, urljoin

from functions import recursive_explore

depth = 1
url = "https://www.eddineomar.fr/"
result : set[str] = set()
recursive_explore(url, depth, result)
print(result)
print(len(result))

thread1 = thread_publish_page_content(result)
thread2 = thread_consume_page_content()

thread1.start()
thread2.start()
thread2.join()
thread1.join()

print("Exit")



# print(class_list)
# print(len(link_list), len(class_list), len(id_tag_list))