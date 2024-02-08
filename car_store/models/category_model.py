from models.database_model import DatabaseConnection

class CategoryModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    # Modelo para obtner los registro de la tabla categoria

    def get_categories(self):
        query = "SELECT * FROM category ORDER BY category_name"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    # Modelo para insertar datos en la tabla categoria

    def create_categories(self, category_name, description):
        try:
            query = "INSERT INTO category (category_name, description) VALUES (%s, %s)"
            self._cur.execute(query, (category_name, description))
            self._conn.commit()
        except Exception as e:
            print(f"Error al crear la categoria: {e}")

    # Modelo para actualizar los registros de la tabla categoria
        
    def update_categories(self, id_category, category_name, description):
        try:
            query = "UPDATE category SET category_name = %s, description = %s WHERE id_category = %s"
            self._cur.execute(query, (category_name, description, id_category))
            self._conn.commit()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            
    def get_category_by_id(self, category_id):
        try:
            query = "SELECT * FROM category WHERE id_category = %s"
            self._cur.execute(query, (category_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener la categoria: {str(e)}")
            return None
        
    def delete_category(self, category_id):
        try:
            query = "DELETE FROM category WHERE id_category = %s"
            self._cur.execute(query, (category_id,))
            self._conn.commit()
        except Exception as e:
            print(f"Error: {str(e)}")