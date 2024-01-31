from database_model import Database

class CategoryModel:
    def __init__(self):
        self._db = Database()
        self._conn = self._db.connect()
        self._cur = self._conn.cursor()

    # Modelo para obtner los registro de la tabla categoria

    def get_categories(self):
        query = "SELECT * FROM category ORDER BY category_name"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    # Modelo para insertar datos en la tabla categoria

    def create_categories(self, category_name, description):
        query = "INSERT INTO customers (category_name, description) VALUES (%s, %s)"
        self._cur.execute(query, (category_name, description))
        self._conn.commit()

    # Modelo para actualizar los registros de la tabla categoria
        
    def update_categories(self, id_category, category_name, description):
        query = "UPDATE category SET category_name = %s, description = %s WHERE id_category = %s"
        self._cur.execute(query, (id_category, category_name, description))
        self._conn.commit()
        
    # Función para cerrar las conexiones

    def close(self):
        self._cur.close()
        self._conn.close()
    