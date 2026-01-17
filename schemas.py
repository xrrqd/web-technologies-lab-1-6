from pydantic import BaseModel
from typing import Optional


class Car(BaseModel): # лр №3
    id: int
    firm: str
    model: str
    year: int
    power: int
    color: str
    price: float
    dealer_id: Optional[int] = None

class CarCreate(BaseModel): # лр №4
    firm: str
    model: str
    year: int
    power: int
    color: str
    price: float
    dealer_id: Optional[int] = None

class CarUpdate(BaseModel): # лр №4
    firm: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    power: Optional[int] = None
    color: Optional[str] = None
    price: Optional[float] = None
    dealer_id: Optional[int] = None

class Dealer(BaseModel): # лр №3
    id: int
    name: str
    city: str
    address: str
    area: str
    rating: float

class DealerCreate(BaseModel): # лр №4
    name: str
    city: str
    address: str
    area: str
    rating: float

class DealerUpdate(BaseModel): # лр №4
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    area: Optional[str] = None
    rating: Optional[float] = None