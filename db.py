import mysql.connector.pooling
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="api_pool",
        pool_size=5,
        **db_config
    )
    print("Pool de conexiones creado exitosamente.")

except mysql.connector.Error as err:
    print(f" Error al crear el pool de conexiones: {err}")
    exit()

def get_db_connection():
    """Obtiene una conexión del pool."""
    try:
        conn = connection_pool.get_connection()
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        print(f" Error al obtener conexión del pool: {err}")
        return None