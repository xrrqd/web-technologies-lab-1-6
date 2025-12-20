import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RabbitMQClient:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST")
        self.port = int(os.getenv("RABBITMQ_PORT"))
        self.user = os.getenv("RABBITMQ_USER")
        self.password = os.getenv("RABBITMQ_PASS")
        self.exchange = os.getenv("RABBITMQ_EXCHANGE")
        self.queue = os.getenv("RABBITMQ_QUEUE")
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type='direct',
            durable=True
        )
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_bind(
            queue=self.queue,
            exchange=self.exchange,
            routing_key=''
        )

    def send_event(self, event_type: str, car_data: dict):
        if not self.connection or not self.channel:
            self.connect()

        message = {
            "eventType": event_type,
            "car": car_data
        }
        
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key='',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        print(f"[x] Отправлено событие: {event_type}")

    def close(self):
        if self.connection:
            self.connection.close()