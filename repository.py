from models import (
    get_all_cars, get_car_by_id, create_car, update_car, delete_car,
    get_all_dealers, get_dealer_by_id, create_dealer, update_dealer, delete_dealer
)
from schemas import CarCreate, CarUpdate, DealerCreate, DealerUpdate


class CarRepository:
    @staticmethod
    def get_all():
        return get_all_cars()

    @staticmethod
    def get_by_id(car_id: int):
        return get_car_by_id(car_id)

    @staticmethod
    def create(car: CarCreate):
        return create_car(car)

    @staticmethod
    def update(car_id: int, car: CarUpdate):
        return update_car(car_id, car)

    @staticmethod
    def delete(car_id: int):
        return delete_car(car_id)


class DealerRepository:
    @staticmethod
    def get_all():
        return get_all_dealers()

    @staticmethod
    def get_by_id(dealer_id: int):
        return get_dealer_by_id(dealer_id)

    @staticmethod
    def create(dealer: DealerCreate):
        return create_dealer(dealer)

    @staticmethod
    def update(dealer_id: int, dealer: DealerUpdate):
        return update_dealer(dealer_id, dealer)

    @staticmethod
    def delete(dealer_id: int):
        return delete_dealer(dealer_id)