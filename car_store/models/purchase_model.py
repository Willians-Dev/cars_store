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
    
    def get_purchase_join(self):
        query = """
                SELECT p.id_purchase, c.model, ca.category_name, c.price
                FROM purchase p
                INNER JOIN car c ON p.id_purchase = c.id_purchase01
                INNER JOIN category ca ON c.id_category01 = ca.id_category;
                """
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def save_purchase(self, id_customer, date, total_price, id_purchase):
        # Realizar el query para insertar los datos en la tabla "purchase"
        query_purchase = "INSERT INTO purchase (id_customer02, date, total_price) VALUES (%s, %s, %s)"
        self._cur.execute(query_purchase, (id_customer, date, total_price))
        self._conn.commit()
        
        # Obtener el id_purchase recién insertado
        #id_purchase_inserted = self._cur.lastrowid

        # Realizar el query para insertar los datos en la tabla "car" usando el id_purchase pasado como argumento
        query_car = "INSERT INTO car (id_purchase01) VALUES (%s)"
        self._cur.execute(query_car, (id_purchase,))
        self._conn.commit()

