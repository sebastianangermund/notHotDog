from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pika
import json
import requests
import numpy as np

from requests.auth import HTTPBasicAuth
from classifier import init_classification

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.queue_declare(queue='new_task')


def callback(ch, method, properties, body):
    """Recieves data from RabbitMQ, redirects photo data to function

    "init_classification" to get classified. If the calssifier got
    less than 0.95 on hotdogs it answers the Django site with "flagged=true".

    """
    raw_message = json.loads(body)
    print(" [x] Received %r" % raw_message['url'])
    is_flagged = raw_message['flag']
    photo_data = np.array(raw_message['photo'])

    depicts_hotdog = init_classification(photo_data)

    if (not is_flagged) and (not depicts_hotdog):
        print('FLAG!')
        api_path = raw_message['url']
        path = 'http://127.0.0.1:8000' + api_path + 'flagged/'

        requests.put(
            path,
            {'flagged': 'true'},
            auth=('agge', '123Hejsan'),
        )
    print(" [x] Done ")


channel.basic_consume(
    callback,
    queue='new_task',
)
print(' [*] Waiting for messages. To exit press CTRL+C:')
channel.start_consuming()
channel.queue_delete(queue='new_task')
connection.close()
