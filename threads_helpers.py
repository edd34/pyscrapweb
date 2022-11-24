import threading
import pika
import requests
from functions import extract_link_class_id

class thread_publish_page_content(threading.Thread):
    def __init__(self, links):
        threading.Thread.__init__(self)
        self.links = links
    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='html_content')
        for link in self.links:
            req = requests.get(link)
            if req.ok:
                channel.basic_publish(exchange='', routing_key='html_content', body=req.text)
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
            # print(" [x] Received %r" % body)
            a, b, c = extract_link_class_id(body)
            print(len(a), len(b), len(c))

        channel.basic_consume(queue='html_content', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
        print("end")