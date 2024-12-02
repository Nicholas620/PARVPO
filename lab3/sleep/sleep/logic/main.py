import os
from dotenv import load_dotenv
from clients.rabbitmq_client import RabbitMQClient
from clients.postgres_client import get_session
from processors import (
    process_user_registration,
    process_user_login,
    process_add_sleep,
    process_sleep_info,
)
from clients.config import QUEUES

def main():
    load_dotenv()

    rabbitmq_client = RabbitMQClient()
    session = get_session()

    channel = rabbitmq_client.channel

    def callback(ch, method, properties, body):
        try:
            if method.routing_key == QUEUES["user_registration"]:
                process_user_registration(body, session)
            elif method.routing_key == QUEUES["user_login"]:
                process_user_login(body, session, ch, properties)
            elif method.routing_key == QUEUES["add_user_sleep"]:
                process_add_sleep(body, session, ch, properties)
            elif method.routing_key == QUEUES["sleep_info"]:
                process_sleep_info(body, session, ch, properties)
        finally:
            session.close()

    channel.basic_consume(queue=QUEUES["user_registration"], on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=QUEUES["user_login"], on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=QUEUES["add_user_sleep"], on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=QUEUES["sleep_info"], on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
