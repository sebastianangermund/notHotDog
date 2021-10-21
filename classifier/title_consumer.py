import pika
import json
import requests

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()
channel.queue_declare(queue='new_task')


def callback(ch, method, properties, body):
    """Takes tasks from RabbitMQ and checks wether the title contains the word
    "hotdog".

    """
    print(" [x] Received %r" % body)
    rawMessage = json.loads(body)
    title = rawMessage['title'].lower()
    api_path = rawMessage['url']
    bol1 = rawMessage['flag']
    bol2 = title.find('hotdog')
    path = 'http://127.0.0.1:8000' + api_path + 'flagged/'
    if (not bol1) and (bol2 < 0):
        print('FLAG!')
        requests.put(path, data={'flagged': 'true'})
    print(" [x] Done ")


channel.basic_consume(
    callback,
    queue='new_task',
)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
