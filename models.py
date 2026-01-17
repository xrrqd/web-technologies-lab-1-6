from database import get_db_connection
from schemas import CarCreate, CarUpdate, DealerCreate, DealerUpdate


# лабораторная работа №3
def get_all_cars():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cars")
            return cursor.fetchall()

def get_car_by_id(car_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
            return cursor.fetchone()

def get_all_dealers():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dealers")
            return cursor.fetchall()

def get_dealer_by_id(dealer_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dealers WHERE id = %s", (dealer_id,))
            return cursor.fetchone()   

# лабораторная работа №4
def create_car(car: CarCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO cars (firm, model, year, power, color, price, dealer_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (car.firm, car.model, car.year, car.power, car.color, car.price, car.dealer_id)
            )
            car_id = cursor.fetchone()["id"]
            conn.commit()
            return {**car.model_dump(), "id": car_id}

def update_car(car_id: int, car: CarUpdate):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            fields = []
            values = []
            for key, value in car.model_dump(exclude_unset=True).items():
                fields.append(f"{key} = %s")
                values.append(value)
            if not fields:
                return None

            query = (f"UPDATE cars SET {", ".join(fields)} WHERE id = %s")
            values.append(car_id)

            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                return None
            return get_car_by_id(car_id)

def delete_car(car_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM cars WHERE id = %s", (car_id,))
            conn.commit()
            return cursor.rowcount > 0

def create_dealer(dealer: DealerCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO dealers ("name", "city", "address", "area", "rating")
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (dealer.name, dealer.city, dealer.address, dealer.area, dealer.rating)
            )
            dealer_id = cursor.fetchone()["id"]
            conn.commit()
            return {**dealer.model_dump(), "id": dealer_id}
        

def update_dealer(dealer_id: int, dealer: DealerUpdate):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            fields = []
            values = []
            for key, value in dealer.model_dump(exclude_unset=True).items():
                fields.append(f"'{key}' = %s")
                values.append(value)
            if not fields:
                return None

            query = (f"UPDATE dealers SET {", ".join(fields)} WHERE id = %s")
            values.append(dealer_id)

            cursor.execute(query, values)
            conn.commit()
            if cursor.rowcount == 0:
                return None
            return get_dealer_by_id(dealer_id)

def delete_dealer(dealer_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM dealers WHERE id = %s", (dealer_id,))
            conn.commit()
            return cursor.rowcount > 0