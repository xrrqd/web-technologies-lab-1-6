
from rabbitmq_client import RabbitMQClient

client = RabbitMQClient()

client.send_event(
    event_type="TEST",
    car_data={"id": 999, "model": "Test Model"}
)

client.close()