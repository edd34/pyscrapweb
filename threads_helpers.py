import threading
import pika
import requests
from requests import Response
from functions import extract_link_class_id
from typing import List

class thread_publish_page_content(threading.Thread):
    def __init__(self, links: set[str]):
        threading.Thread.__init__(self)
        self.links : set[str] = links
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='html_content')
        for link in self.links:
            req : Response = requests.get(link)
            if req.ok:
                channel.basic_publish(exchange='', routing_key='html_content', body=req.text)
        channel.basic_publish(exchange='', routing_key='html_content', body="close")
        connection.close()

class thread_consume_page_content(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # helper function to execute the threads
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='html_content')

        def callback(ch, method, properties, body):
            print(" [x] received")
            # print(" [x] Received %r" % body)
            class_list, link_list, id_tag_list = extract_link_class_id(body)
            # print(class_list, link_list, id_tag_list)
            print(len(class_list), len(link_list), len(id_tag_list))
            if body == b"close":
                channel.close()
                return

        channel.basic_consume(queue='html_content', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        print("end")