from models.database_model import DatabaseConnection

class CustomersModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    # Modelo para obtener los clientes desde la base de datos

    def get_customers(self):
        query = "SELECT * FROM customer ORDER BY last_name"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    # Modelo para agregar registros a la tabla clientes a la base datos

    def create_customers(self, document, first_name, last_name, email):
        query = "INSERT INTO customer (document, first_name, last_name, email) VALUES (%s, %s, %s, %s)"
        self._cur.execute(query, (int(document), first_name, last_name, email))
        self._conn.commit()

    # Modelo para actualizar los registros de la tabla clientes
        
    def update_customers(self, id_customer, document, first_name, last_name, email):
        try:
            query = "UPDATE customer SET document = %s, first_name = %s, last_name = %s, email = %s WHERE id_customer = %s"
            self._cur.execute(query, (document, first_name, last_name, email, id_customer))
            self._conn.commit()
        except Exception as e:
            print(f"Error al actualizar la categoria: {str(e)}")
            return None

    def get_customers_by_id(self, customer_id):
        try:
            query = "SELECT * FROM customer WHERE id_customer = %s"
            self._cur.execute(query, (customer_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener el cliente: {str(e)}")
            return None
        
    def delete_customer(self, customer_id):
        try:
            query = "DELETE FROM customer WHERE id_customer = %s"
            self._cur.execute(query, (customer_id,))
            self._conn.commit()
        except Exception as e:
            print(f"Error: {str(e)}")