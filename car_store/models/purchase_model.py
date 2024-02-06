from models.database_model import DatabaseConnection

class PurchaseModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    def get_purchase(self):
        query = """SELECT p.id_purchase, p.date, p.city, CONCAT(c.first_name, ' ', c.last_name), p.total_price, p.payment_method 
                FROM purchase p
                INNER JOIN customer c ON p.id_customer02 = c.id_customer
                """
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def create_purchase(self, id_purchase, date, city, total_price, payment_method, id_customer02):
        # Consulta SQL para insertar una nueva compra en la base de datos
        query = """
            INSERT INTO purchase (id_purchase, date, city, total_price, payment_method, id_customer02) 
            VALUES (%s, %s, %s, %s, %s, %s) 
            RETURNING id_purchase;
        """
        try:
            # Ejecutar la consulta SQL con los parámetros proporcionados
            self._cur.execute(query, (id_purchase, date, city, total_price, payment_method, id_customer02))
            # Obtener el ID de la compra recién insertada
            purchase_id = self._cur.fetchone()[0]
            # Confirmar los cambios en la base de datos
            self._conn.commit()
            return purchase_id  # Devolver el ID de la nueva compra insertada
        except Exception as e:
            # Si ocurre algún error, revertir los cambios y mostrar un mensaje de error
            self._conn.rollback()
            print("Error al guardar la compra:", e)
            return None
    
    def get_products_and_categories(self):
        query = """SELECT car.id_car, car.model, category.category_name 
                FROM car 
                INNER JOIN category ON car.id_category01 = category.id_category"""
        self._cur.execute(query)
        return self._cur.fetchall()
        
    def get_purchase_join(self):
        query = """
                SELECT p.id_purchase, c.model, ca.category_name
                FROM purchase p
                INNER JOIN car c ON p.id_purchase = c.id_purchase01
                INNER JOIN category ca ON c.id_category01 = ca.id_category;
                """
        self._cur.execute(query)
        return self._cur.fetchall()