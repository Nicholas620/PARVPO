import os
import time
import pika
from dotenv import load_dotenv
from .config import QUEUES

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

class RabbitMQClient:
    def __init__(self):
        self.channel = self.connect_to_rabbitmq()

    def connect_to_rabbitmq(self):
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=os.getenv('RABBITMQ_HOST'),
                        port=int(os.getenv('RABBITMQ_PORT'))
                    )
                )
                channel = connection.channel()

                for queue in QUEUES.values():
                    channel.queue_declare(queue=queue)

                print("Connected to RabbitMQ successfully.")
                return channel
            except pika.exceptions.AMQPConnectionError:
                print("RabbitMQ not available yet, retrying...")
                time.sleep(5)
