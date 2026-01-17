from rabbitmq_client import RabbitMQClient

client = RabbitMQClient()
try:
    client.connect()
    print("Подключение успешно!")
    client.close()
except Exception as e:
    print(f"Ошибка подключения: {e}")