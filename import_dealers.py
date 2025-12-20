import json
import psycopg2
import random
from psycopg2.extras import execute_batch


DB_CONFIG = {
    'host': 'localhost',
    'database': 'Cars',
    'user': 'postgres',
    'password': 'postgres1',
    'port': '5432'
}

def load_dealers(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def insert_dealers(conn, dealers):
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO dealers (Name, City, Address, Area, Rating)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """
    execute_batch(cursor, insert_query, [
        (d['Name'], d['City'], d['Address'], d['Area'], d['Rating'])
        for d in dealers
    ])
    conn.commit()
    cursor.close()
    print(f"Добавлено {len(dealers)} дилеров.")


def get_all_car_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM cars WHERE dealer_id IS NULL")
    car_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return car_ids


def assign_cars_to_dealers(conn, dealer_ids, car_ids):
    cursor = conn.cursor()
    
    # перемешиваем автомобили для случайного распределения
    random.shuffle(car_ids)
    
    assignments = []  # список (dealer_id, car_id)
    car_index = 0
    
    for dealer_id in dealer_ids:
        # каждому дилеру даём от 1 до 5 автомобилей (или сколько осталось)
        num_cars = random.randint(1, 5)
        for _ in range(num_cars):
            if car_index < len(car_ids):
                car_id = car_ids[car_index]
                assignments.append((dealer_id, car_id))
                car_index += 1
            else:
                break  # все автомобили распределены
    
    # обновляем поле dealer_id в таблице cars
    update_query = """
    UPDATE cars
    SET dealer_id = %s
    WHERE id = %s
    """
    execute_batch(cursor, update_query, assignments)
    conn.commit()
    cursor.close()
    print(f"Назначено {len(assignments)} автомобилей дилерам.")


def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Подключение к БД успешно.")
        
        # загрузка дилеров из json
        dealers = load_dealers('dealers.json')
        insert_dealers(conn, dealers)
        
        # получение id дилеров
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dealers")
        dealer_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        # получение свободных автомобилей (без дилера)
        car_ids = get_all_car_ids(conn)
        # распределение автомобилей по дилерам
        assign_cars_to_dealers(conn, dealer_ids, car_ids)
        
        conn.close()
        print("Все операции выполнены успешно!")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
