from fastapi import FastAPI, HTTPException, status
from models import (
    get_all_cars, get_car_by_id, create_car, update_car, delete_car,
    get_all_dealers, get_dealer_by_id, create_dealer, update_dealer, delete_dealer
)
from repository import CarRepository, DealerRepository
from event_decorator import send_car_event, send_dealer_event
from schemas import Car, CarCreate, CarUpdate, Dealer, DealerCreate, DealerUpdate


app = FastAPI(title="Car Dealers API", version="3.1")


# контроллер для автомобилей

# лабораторная работа №3
@app.get("/api/cars", response_model=list[Car])
def get_cars():
    cars = get_all_cars()
    if not cars:
        raise HTTPException(status_code=404, detail="Автомобили не найдены")
    return cars

@app.get("/api/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    car = get_car_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail=(f"Автомобиль с id {car_id} не найдена"))
    return car

# лабораторная работа №4
@app.post("/api/cars", response_model=Car, status_code=status.HTTP_201_CREATED)
def create_new_car(car: CarCreate):
    try:
        new_car = create_car(car)
        return new_car
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/cars/{car_id}", response_model=Car)
def update_existing_car(car_id: int, car: CarUpdate):
    updated_car = update_car(car_id, car)
    if not updated_car:
        raise HTTPException(status_code=404, detail=(f"Автомобиль с id {car_id} не найден либо данные не обновлены"))
    return updated_car

@app.delete("/api/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_car(car_id: int):
    if not delete_car(car_id):
        raise HTTPException(status_code=404, detail=(f"Автомобиль с id {car_id} не найден"))
    return


# лабораторная работа №5
@app.get("/api/cars", response_model=list[Car])
def get_cars():
    cars = CarRepository.get_all()
    if not cars:
        raise HTTPException(status_code=404, detail="Автомобили не найдены")
    return cars

@app.get("/api/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    car = CarRepository.get_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail=f"Автомобиль с id {car_id} не найден")
    return car

@app.post("/api/cars", response_model=Car, status_code=status.HTTP_201_CREATED)
@send_car_event("CREATE")
def create_new_car(car: CarCreate):
    try:
        new_car = CarRepository.create(car)
        return new_car
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/cars/{car_id}", response_model=Car)
@send_car_event("UPDATE")
def update_existing_car(car_id: int, car: CarUpdate):
    updated_car = CarRepository.update(car_id, car)
    if not updated_car:
        raise HTTPException(
            status_code=404,
            detail=f"Автомобиль с id {car_id} не найден либо данные не обновлены"
        )
    return updated_car

@app.delete("/api/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
@send_car_event("DELETE")
def delete_existing_car(car_id: int):
    if not CarRepository.delete(car_id):
        raise HTTPException(status_code=404, detail=f"Автомобиль с id {car_id} не найден")
    return


#контроллер для дилеров

# лабораторная работа №3
@app.get("/api/dealers", response_model=list[Dealer])
def get_dealers():
    dealers = get_all_dealers()
    if not dealers:
        raise HTTPException(status_code=404, detail="Дилеры не найдены")
    return dealers

@app.get("/api/dealers/{dealer_id}", response_model=Dealer)
def get_dealer(dealer_id: int):
    dealer = get_dealer_by_id(dealer_id)
    if not dealer:
        raise HTTPException(status_code=404, detail=(f"Дилер с id {dealer_id} не найден"))
    return dealer

# лабораторная работа №4
@app.post("/api/dealers", response_model=Dealer, status_code=status.HTTP_201_CREATED)
def create_new_dealer(dealer: DealerCreate):
    try:
        new_dealer = create_dealer(dealer)
        return new_dealer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/dealers/{dealer_id}", response_model=Dealer)
def update_existing_dealer(dealer_id: int, dealer: DealerUpdate):
    updated_dealer = update_dealer(dealer_id, dealer)
    if not updated_dealer:
        raise HTTPException(
            status_code=404,
            detail=f"Дилер с id {dealer_id} не найден либо данные не обновлены"
        )
    return updated_dealer

@app.delete("/api/dealers/{dealer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_dealer(dealer_id: int):
    if not delete_dealer(dealer_id):
        raise HTTPException(
            status_code=404,
            detail=f"Дилер с id {dealer_id} не найден"
        )
    return
    
# лабораторная работа №5
@app.get("/api/dealers", response_model=list[Dealer])
def get_dealers():
    dealers = DealerRepository.get_all()
    if not dealers:
        raise HTTPException(status_code=404, detail="Дилеры не найдены")
    return dealers

@app.get("/api/dealers/{dealer_id}", response_model=Dealer)
def get_dealer(dealer_id: int):
    dealer = DealerRepository.get_by_id(dealer_id)
    if not dealer:
        raise HTTPException(status_code=404, detail=f"Дилер с id {dealer_id} не найден")
    return dealer

@app.post("/api/dealers", response_model=Dealer, status_code=status.HTTP_201_CREATED)
@send_dealer_event("CREATE")
def create_new_dealer(dealer: DealerCreate):
    try:
        new_dealer = DealerRepository.create(dealer)
        return new_dealer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/dealers/{dealer_id}", response_model=Dealer)
@send_dealer_event("UPDATE")
def update_existing_dealer(dealer_id: int, dealer: DealerUpdate):
    updated_dealer = DealerRepository.update(dealer_id, dealer)
    if not updated_dealer:
        raise HTTPException(
            status_code=404,
            detail=f"Дилер с id {dealer_id} не найден либо данные не обновлены"
        )
    return updated_dealer


@app.delete("/api/dealers/{dealer_id}", status_code=status.HTTP_204_NO_CONTENT)
@send_dealer_event("DELETE")
def delete_existing_dealer(dealer_id: int):
    if not DealerRepository.delete(dealer_id):
        raise HTTPException(status_code=404, detail=f"Дилер с id {dealer_id} не найден")
    return