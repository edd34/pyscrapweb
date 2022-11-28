import threading
import pika
import requests
from requests import Response
from functions import extract_link_class_id, count_occurence
from typing import List, Iterator
from database import PatternSchema, Pattern
from json import dumps, loads
import datetime
import orm_sqlite
from add_wrapper import Add

class thread_publish_page_content(threading.Thread):
    """
    
    """
    def __init__(self, queue_uuid:str, links: Iterator[str]):
        threading.Thread.__init__(self)
        self.links: Iterator[str] = links
        self.queue_uuid = queue_uuid

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_uuid)
        for link in self.links:
            req: Response = requests.get(link)
            if req.ok:
                channel.basic_publish(
                    exchange="",
                    routing_key=self.queue_uuid,
                    body=dumps({"content": req.text, "link": link, "command":"ok"}),
                )
        channel.basic_publish(exchange="", routing_key=self.queue_uuid, body=dumps({"command":"close"}))
        connection.close()


class thread_consume_page_content(threading.Thread):
    def __init__(self, queue_uuid):
        threading.Thread.__init__(self)
        self.queue_uuid = queue_uuid
        self.id_dict_cpt = None
        self.class_dict_cpt = None

        # helper function to execute the threads

    def run(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_uuid)
        class_dict_cpt = {}
        id_dict_cpt = {}

        def callback(ch, method, properties, body):
            db = orm_sqlite.Database("database.db")
            Pattern.objects.backend = db
            body = loads(body)
            print(body["command"])
            if body["command"] == "close":
                channel.close()
                return 0
            link = body.get("link")
            print(" [x] received %r " % link)
            content = body.get("content")
            _class_list, _, _id_tag_list = extract_link_class_id(content)
            dict_cpt_class = count_occurence(_class_list)
            dict_cpt_id = count_occurence(_id_tag_list)
            timestamp = datetime.datetime.now()
            for elem in dict_cpt_class:
                p = Pattern({
                    "url":link,
                    "timestamp":str(timestamp),
                    "entity_type":"class",
                    "entity_name":elem,
                    "entity_count":dict_cpt_class[elem],
                })
                p.save()
                if elem not in class_dict_cpt.keys():
                    class_dict_cpt[elem] = 0
                class_dict_cpt[elem] = Add(class_dict_cpt[elem], 1)
            for elem in dict_cpt_id:
                p = Pattern({
                    "url":link,
                    "timestamp":str(timestamp),
                    "entity_type":"id",
                    "entity_name":elem,
                    "entity_count":dict_cpt_id[elem],
                })
                p.save()
                if elem not in id_dict_cpt.keys():
                    id_dict_cpt[elem] = 0
                id_dict_cpt[elem] = Add(id_dict_cpt[elem], 1)

            self.id_dict_cpt = id_dict_cpt
            self.class_dict_cpt = class_dict_cpt

        channel.basic_consume(
            queue=self.queue_uuid, on_message_callback=callback, auto_ack=True
        )

        print(" [*] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
        print("end")
