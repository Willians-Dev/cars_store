from models.database_model import DatabaseConnection

class PurchaseModel:
    def __init__(self):
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    def get_purchase(self):
        query = """
                SELECT p.id_purchase, c.model, ca.category_name
                FROM purchase p
                INNER JOIN car c ON p.id_purchase = c.id_purchase01
                INNER JOIN category ca ON c.id_category01 = ca.id_category;
                """
        self._cur.execute(query)
        return self._cur.fetchall()