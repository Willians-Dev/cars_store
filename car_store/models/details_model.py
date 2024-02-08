from models.database_model import DatabaseConnection

class DetailsModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    def get_details(self):
        query = """SELECT p.id_purchase, p.date, CONCAT(cu.first_name, ' ', cu.last_name), car.model, ca.category_name, car.price 
                FROM purchase p
                INNER JOIN customer cu ON p.id_customer02 = cu.id_customer
                INNER JOIN car ON cu.id_customer = car.id_customer01
                INNER JOIN category ca ON car.id_category01 = ca.id_category
                """
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def get_details_by_id(self, customer_id):
        try:
            query = """SELECT p.id_purchase, p.date, CONCAT(c.first_name, ' ', c.last_name), model, category_name, p.total_price
                    FROM purchase p
                    INNER JOIN customer c ON p.id_customer02 = c.id_customer
                    INNER JOIN car ON c.id_customer = car.id_customer01
                    INNER JOIN category cat ON car.id_category01 = cat.id_category
                    WHERE id_customer = %s"""
            self._cur.execute(query, (customer_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener el cliente por id: {e}")
            return None