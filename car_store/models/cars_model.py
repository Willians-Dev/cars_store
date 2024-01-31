from models.database_model import Database

class CarsModel:
    def __init__(self):
        self._db = Database()
        self._conn = self._db.connect()
        self._cur = self._conn.cursor()

    # Modelo para obtener los registro de la tabla cars de la base de datos

    def get_cars(self):
        query = "SELECT * FROM cars ORDER BY year"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    # Modelo para agregar registros a la tabla cars a la base datos

    def create_cars(self, serial_number, brand, model, transmision, price, year):
        query = "INSERT INTO cars (serial_number, brand, model, transmision, price, year) VALUES (%s, %s, %s, %s, %s, %s)"
        self._cur.execute(query, (serial_number, brand, model, transmision, price, year))
        self._conn.commit()

    # Modelo para actualizar los registros de la tabla cars
        
    def update_cars(self, id_car, serial_number, brand, model, transmision, price, year):
        query = "UPDATE cars SET serial_number = %s, brand = %s, model = %s, transmision = %s, price = %s, year = %s WHERE id_cars = %s"
        self._cur.execute(query, (id_car, serial_number, brand, model, transmision, price, year))
        self._conn.commit()

    # Función para cerrar las conexiones

    def close(self):
        self._cur.close()
        self._conn.close()