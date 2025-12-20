import psycopg2
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    'host': 'localhost',
    'database': 'Cars',
    'user': 'postgres',
    'password': 'postgres1',
    'port': '5432'
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)