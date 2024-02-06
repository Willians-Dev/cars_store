import pathlib
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QPushButton
from PyQt5 import uic, QtCore
from models.database_model import DatabaseConnection
from models.purchase_model import PurchaseModel
from controllers.purchase_form import PurchaseForm

class PurchaseTable(QMainWindow):
    def __init__(self):
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_purchase.ui", self)
        self._purchase_model = PurchaseModel()
        self.puchaseForm = PurchaseForm()
        self.load_purchase()
        self.addNewPurchaseForm.triggered.connect(lambda: self.create_purchases())
        self.puchaseForm.purchase_saved.connect(self.load_purchase)
        self.quitPurchaseFormButton.triggered.connect(self.close)

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
            #detail_button.clicked.connect(self.edit_customer)
            detail_button.setProperty("row", i)
            #self.costumerTableWidget.setCellWidget(i, 5, edit_button)

        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.purchaseTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def create_purchases(self):
        self.puchaseForm.reset_form()
        self.puchaseForm.show()

    def closeEvent(self, ev) -> None:
        db = DatabaseConnection()
        db.close()
        return super().closeEvent(ev)
