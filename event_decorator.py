from rabbitmq_client import RabbitMQClient


rabbitmq = RabbitMQClient()


def send_car_event(event_type: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if result and isinstance(result, dict) and 'id' in result:
                rabbitmq.send_event(event_type, result)
            
            return result
        return wrapper
    return decorator


def send_dealer_event(event_type: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            if result and isinstance(result, dict) and 'id' in result:
                rabbitmq.send_event(event_type, result)
            
            return result
        return wrapper
    return decorator