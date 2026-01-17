import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

class RabbitMQClient:
    def __init__(self):
        load_dotenv()
   
        print("RABBITMQ_HOST:", os.getenv("RABBITMQ_HOST"))
        print("RABBITMQ_EXCHANGE:", os.getenv("RABBITMQ_EXCHANGE"))
        print("RABBITMQ_QUEUE:", os.getenv("RABBITMQ_QUEUE"))
    
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.user = os.getenv("RABBITMQ_USER", "xrrqd")
        self.password = os.getenv("RABBITMQ_PASS", "zkZ-tk4-pX8-2md")
        self.exchange = os.getenv("RABBITMQ_EXCHANGE", "cars_events_exchange")
        self.queue = os.getenv("RABBITMQ_QUEUE", "cars_events_queue")
        
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=credentials,
            virtual_host='/',
            heartbeat=600,
            blocked_connection_timeout=300
        )
        try:
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
                routing_key=' '
            )
            print("Подключение к RabbitMQ установлено")
        except Exception as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")
            raise

    def send_event(self, event_type: str, car_data: dict):
        try:
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
                    content_type='application/json'
                ),
                mandatory=True
            )
            print(f"Отправлено событие: {event_type} | Данные: {car_data}")

        except pika.exceptions.UnroutableBody:
            print("Сообщение не доставлено: нет подходящего binding")
        except pika.exceptions.AMQPConnectionError:
            print("Соединение с RabbitMQ разорвано. Пытаюсь переподключиться...")
            self.connection = None
            self.send_event(event_type, car_data)
        except Exception as e:
            print(f"Ошибка отправки события: {e}")

    def close(self):
        if self.connection:
            try:
                self.connection.close()
                print("Соединение с RabbitMQ закрыто")
            except Exception as e:
                print(f"Ошибка при закрытии соединения: {e}")
