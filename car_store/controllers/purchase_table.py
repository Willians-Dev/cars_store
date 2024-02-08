import pathlib
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QPushButton
from PyQt5 import uic, QtCore
from models.database_model import DatabaseConnection
from models.purchase_model import PurchaseModel
from controllers.purchase_form import PurchaseForm
from controllers.purchase_details import PurchaseDetails

class PurchaseTable(QMainWindow):
    def __init__(self):
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_purchase.ui", self)

        css_path = pathlib.Path(__file__).parent.parent / "views/styles.css"
        with open(css_path, "r") as f:
            self.setStyleSheet(f.read())

        self._purchase_model = PurchaseModel()
        self.puchaseForm = PurchaseForm()
        self.purchaseDetails = PurchaseDetails()
        self.load_purchase()
        self.addNewPurchaseForm.triggered.connect(lambda: self.create_purchases())
        self.puchaseForm.purchase_saved.connect(self.load_purchase)
        self.quitPurchaseFormButton.triggered.connect(self.close)
        self.purchaseForm = PurchaseForm()
        self.purchaseForm.purchase_saved.connect(self.update_purchase_table)

    def load_purchase(self):
        
        purchase_list = self._purchase_model.get_purchase()
        self.purchaseTableWidget.setRowCount(len(purchase_list))
        for i, purchase in enumerate(purchase_list):
            id_purchase, date, city, name_customer ,total_price, payment_method, *extra = purchase
            self.purchaseTableWidget.setItem(i, 0, QTableWidgetItem(str(id_purchase)))
            self.purchaseTableWidget.setItem(i, 1, QTableWidgetItem(str(date)))
            self.purchaseTableWidget.setItem(i, 2, QTableWidgetItem(str(city)))
            self.purchaseTableWidget.setItem(i, 3, QTableWidgetItem(str(name_customer)))
            self.purchaseTableWidget.setItem(i, 4, QTableWidgetItem(str(total_price)))
            self.purchaseTableWidget.setItem(i, 5, QTableWidgetItem(str(payment_method)))
            self.purchaseTableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 3).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 4).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.purchaseTableWidget.item(i, 5).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            # Botón para editar los clientes
             
            detail_button = QPushButton("Detalles")
            detail_button.clicked.connect(self.show_details)
            detail_button.setProperty("row", i)
            self.purchaseTableWidget.setCellWidget(i, 6, detail_button)

        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.purchaseTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    #def show_details(self):
    #    sender = self.sender()
    #    row = sender.property("row")
    #    # No es necesario pasar purchase_id como argumento
    #    # purchase_id = self.purchaseTableWidget.item(row, 0).text()
    #    self.purchaseDetails.load_details()  # No se pasa ningún argumento
    #    self.purchaseDetails.show()
                
    def create_purchases(self):
        self.puchaseForm.reset_form()
        self.puchaseForm.show()
    
    def update_purchase_table(self):
        # Puedes llamar al método que obtiene las compras y actualiza la tabla
        self.load_purchase()

    def closeEvent(self, ev) -> None:
        db = DatabaseConnection()
        db.close()
        return super().closeEvent(ev)
    
    def show_details(self):
        sender = self.sender()
        row = sender.property("row")
        customer_id = self.purchaseTableWidget.item(row, 0).text()
        self.purchaseDetails.load_details_data(customer_id)
        self.purchaseDetails.show()
