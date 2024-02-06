import pathlib
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from PyQt5 import uic
from models.customer_model import CustomersModel
from models.purchase_model import PurchaseModel

class PurchaseForm(QMainWindow):
    purchase_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/purchase_form.ui", self)
        self._purchase_id = None
        self._customer_model = CustomersModel()
        self._purchase_model = PurchaseModel()   
        self.load_categories()
        self.update_current_datetime()
        self.load_purchase_form()
        

    def load_categories(self):
        customers = self._customer_model.get_customers()  # Método para obtener el cliente del customer_model
        self.customerPurchaseComboBox.clear()
        for id_customer, _ , first_name, last_name, _ in customers:
            self.customerPurchaseComboBox.addItem(f"{first_name} {last_name}", userData=id_customer)  # Agregar solo el category_name al combo box, pero almacenar el id_category como userData
        # Método para guardar las categorias a traves del update_categoria
            
    def update_current_datetime(self):
        # Obtener la fecha y hora actual del sistema
        current_datetime = QDateTime.currentDateTime()
        # Establecer la fecha y hora actual en el QDateTimeEdit
        self.CompraDateTime.setDateTime(current_datetime)
        # Almacenar la fecha y hora actual en una variable
        self.current_datetime = current_datetime

    def load_purchase_form(self):
        order_list = self._purchase_model.get_purchase_join()
        self.purchaseTableWidget.setRowCount(len(order_list))
        for i, order in enumerate(order_list):
            id_purchase, model, category_name = order
            self.purchaseTableWidget.setItem(i, 0, QTableWidgetItem(str(id_purchase)))
            self.purchaseTableWidget.setItem(i, 1, QTableWidgetItem(str(model)))
            self.purchaseTableWidget.setItem(i, 2, QTableWidgetItem(str(category_name)))
        
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Ajustar a contenido para la primera columna
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Estirar automáticamente para las otras columnas
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.purchaseTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def create_order(self):
        order_list = self._purchase_model.create_purchase()
        self.purchaseTableWidget.setRowCount(len(order_list))
        for i, order in enumerate(order_list):
            id_purchase, model, category_name = order
            self.purchaseTableWidget.setItem(i, 0, QTableWidgetItem(str(id_purchase)))
            self.purchaseTableWidget.setItem(i, 1, QTableWidgetItem(str(model)))
            self.purchaseTableWidget.setItem(i, 2, QTableWidgetItem(str(category_name)))
            
    def reset_form(self):
        self._purchase_id = None
        
    
