import pathlib
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QHeaderView
from models.purchase_model import PurchaseModel
from models.customer_model import CustomersModel

class PurchaseTable(QMainWindow):
    def __init__(self):
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_purchase.ui", self)
        self._purchase_model = PurchaseModel()
        self._customer_model = CustomersModel()
        # Conectar botones a funciones
        #self.saveCompraButton.clicked.connect(self.save_compra)
        #self.cancelCompraButton.clicked.connect(lambda: self.close())
        self.load_purchase()
        self.load_customers()

    def load_customers(self):
        customers = self._customer_model.get_customers()  # Método para obtener los clientes del modelo
        self.customerPurchaseComboBox.clear()
        for id_customer, _ , first_name, last_name, _ in customers:
            self.customerPurchaseComboBox.addItem(f"{first_name} {last_name}", userData=id_customer) # Agregar solo el category_name al combo box, pero almacenar el id_category como userData

    def load_purchase(self):
        purchase_list = self._purchase_model.get_purchase()
        self.purchaseTableWidget.setRowCount(len(purchase_list))
        for i, purchase in enumerate(purchase_list):
            id_purchase, model, name_category = purchase
            self.purchaseTableWidget.setItem(i, 0, QTableWidgetItem(str(id_purchase)))
            self.purchaseTableWidget.setItem(i, 1, QTableWidgetItem(str(model)))
            self.purchaseTableWidget.setItem(i, 2, QTableWidgetItem(str(name_category)))
            self.purchaseTableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.purchaseTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
   