import psycopg2

class CustomerModel:
    def __init__(self) -> None:
        self._conn = psycopg2.connect("dbname= user= password= host=localhost")
        self._cur = self._conn.cursor()