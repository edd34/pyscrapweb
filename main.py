from scraper import Scrap
from threads_helpers import thread_consume_page_content, thread_publish_page_content
from urllib.parse import urlparse, urljoin
from functions import recursive_explore
import orm_sqlite
from database import Pattern
import argparse
import uuid

def main(url: str, depth:int)->None:
    result: set[str] = set()

    queue_uuid = str(uuid.uuid4())
    thread1 = thread_publish_page_content(queue_uuid, recursive_explore(url, depth, result))
    thread2 = thread_consume_page_content(queue_uuid)

    thread1.start()
    thread2.start()
    thread2.join()
    thread1.join()
    print("thread2.class_dict_cpt", thread2.class_dict_cpt)
    print("thread2.id_dict_cpt", thread2.id_dict_cpt)

    print("Exit")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog = 'PyScrapAttr',
                    description = "PyScrapAttr is a lightweight python CLI and it's purpose is to scrap recursively a website and extract stats about class and id attributes.")
    parser.add_argument('--url', help="Url of website to scrape.")
    parser.add_argument('--depth', help="Depth of recursivity to stop at.", type=int )

    args = parser.parse_args()
    print(parser)
    print(args.depth)
    
    main(url=args.url, depth=args.depth)