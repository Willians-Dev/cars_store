from models.database_model import DatabaseConnection

class CarsModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    # Modelo para obtener los registro de la tabla cars de la base de datos

    def get_cars(self):
        query = "SELECT * FROM car ORDER BY year"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    # Modelo para agregar registros a la tabla cars a la base datos

    def create_cars(self, serial_number, brand, model, transmission, price, year):
        query = """INSERT INTO car (serial_number, brand, model, transmission, price, year) VALUES (%s, %s, %s, %s, %s, %s) 
                   ON CONFLICT (serial_number) 
                   DO UPDATE SET brand = EXCLUDED.brand, model = EXCLUDED.model, transmission = EXCLUDED.transmission, price = EXCLUDED.price, year = EXCLUDED.year
                   RETURNING id_car"""
        try:
            self._cur.execute(query, (serial_number, brand, model, transmission, price, year))
            self._conn.commit()
            print("Registro insertado correctamente.")
        except Exception as e:
            self._conn.rollback()
            print("Error al insertar el registro:", e)
    


    # Modelo para actualizar los registros de la tabla cars
        
    def update_cars(self, id_car, serial_number, brand, model, transmission, price, year):
        query = "UPDATE car SET serial_number = %s, brand = %s, model = %s, transmission = %s, price = %s, year = %s WHERE id_car = %s"
        self._cur.execute(query, (id_car, serial_number, brand, model, transmission, price, year))
        self._conn.commit()

    def get_cars_by_id(self, car_id):
        try:
            query = "SELECT * FROM car WHERE id_car = %s"
            self._cur.execute(query, (car_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener el carro: {str(e)}")
            return None
        
    def delete_cars(self, car_id):
        query = "DELETE FROM car WHERE id_car = %s"
        self._cur.execute(query, (car_id,))
        self._conn.commit()

    # Función para cerrar las conexiones

    def close(self):
        self._cur.close()
        self._conn.close()