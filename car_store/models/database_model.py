import psycopg2
from psycopg2 import OperationalError

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Database:
    def __init__(self):
        self._conn = None

    def connect(self):
        if self._conn is None:
            try:
                self._conn = psycopg2.connect(
                    dbname="nombre_basedatos",
                    user="usuario",
                    password="contraseña",
                    host="localhost",
                    port="5432"
                )
                print("Conexión establecida correctamente.")
            except OperationalError as e:
                print(f"Error: {e}")
        return self._conn

    def disconnect(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None
            print("Conexión cerrada.")
