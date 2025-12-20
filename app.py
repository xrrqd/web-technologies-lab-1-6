import json
import psycopg2
from psycopg2.extras import execute_batch

# подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    database="Cars",
    user="postgres",
    password="postgres1"
)
cursor = conn.cursor()

# чтение json-файла
with open('cars.json', 'r', encoding='utf-8') as file:
    cars = json.load(file)

# sql-запрос для вставки данных
insert_query = """
INSERT INTO cars (firm, model, year, power, color, price)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# массовая вставка данных
execute_batch(cursor, insert_query, [
    (car['firm'], car['model'], car['year'], car['power'], car['color'], car['price'])
    for car in cars
])

# сохранение изменений
conn.commit()
cursor.close()
conn.close()

print("Данные успешно загружены в базу данных Cars!")
