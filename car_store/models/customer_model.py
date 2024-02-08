from PyQt5.QtWidgets import QMessageBox
from models.database_model import DatabaseConnection

class CustomersModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    # Modelo para obtener los clientes desde la base de datos

    def get_customers(self):
        try:
            query = "SELECT * FROM customer ORDER BY last_name"
            self._cur.execute(query)
            return self._cur.fetchall()
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            return None
    
    def create_customer(self, document, first_name, last_name, email):
        try:
            # Verificar la longitud del documento
            if len(document) != 10:
                raise ValueError("El documento debe tener 10 dígitos")
            
            query = "INSERT INTO customer (document, first_name, last_name, email) VALUES (%s, %s, %s, %s)"
            self._cur.execute(query, (document, first_name, last_name, email))
            self._conn.commit()
        except ValueError as ve:
            # Mostrar un QMessageBox con el mensaje de error
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Warning)
            error_box.setWindowTitle("Error")
            error_box.setText(str(ve))
            error_box.exec_()
        except Exception as e:
            print(f"Error al crear el cliente: {e}")

    def update_customer(self, id_customer, document, first_name, last_name, email):
        try:
            query = "UPDATE customer SET document = %s, first_name = %s, last_name = %s, email = %s WHERE id_customer = %s"
            self._cur.execute(query, (document, first_name, last_name, email, id_customer))
            self._conn.commit()
        except Exception as e:
            print(f"Error al actualizar el cliente: {e}")

    def get_customer_by_id(self, customer_id):
        try:
            query = "SELECT * FROM customer WHERE id_customer = %s"
            self._cur.execute(query, (customer_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener el cliente por id: {e}")
            return None
        
    def delete_customer(self, customer_id):
        try:
            query = "DELETE FROM customer WHERE id_customer = %s"
            self._cur.execute(query, (customer_id,))
            self._conn.commit()
        except Exception as e:
            print(f"Error al eliminar el cliente: {e}")