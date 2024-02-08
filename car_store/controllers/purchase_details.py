import pathlib
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5 import uic, QtCore
from models.details_model import DetailsModel

class PurchaseDetails(QMainWindow):
    details_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/purchase_details.ui", self)

        css_path = pathlib.Path(__file__).parent.parent / "views/styles.css"
        with open(css_path, "r") as f:
            self.setStyleSheet(f.read())

        self.details_id = None
        self._details_model = DetailsModel()
        self.load_details()
        self.quitDetailButton.clicked.connect(self.close)

    def load_details(self):
        details_list = self._details_model.get_details()
        self.detailTableWidget.setRowCount(len(details_list))
        for i, purchase in enumerate(details_list):
            id_purchase, date, cliente, producto, categoria , precio_total, *extra = purchase
            self.detailTableWidget.setItem(i, 0, QTableWidgetItem(str(id_purchase)))
            self.detailTableWidget.setItem(i, 1, QTableWidgetItem(str(date)))
            self.detailTableWidget.setItem(i, 2, QTableWidgetItem(str(cliente)))
            self.detailTableWidget.setItem(i, 3, QTableWidgetItem(str(producto)))
            self.detailTableWidget.setItem(i, 4, QTableWidgetItem(str(categoria)))
            self.detailTableWidget.setItem(i, 5, QTableWidgetItem(str(precio_total)))
            self.detailTableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.detailTableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.detailTableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.detailTableWidget.item(i, 3).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.detailTableWidget.item(i, 4).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.detailTableWidget.item(i, 5).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

        self.detailTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  
        self.detailTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  
        self.detailTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.detailTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.detailTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.detailTableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.detailTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def load_details_data(self, customer_id):
        details_data = self._details_model.get_details_by_id(customer_id)
        if details_data:
            self.detailTableWidget.setRowCount(1)  # Configura una sola fila para mostrar los datos
            for i, data in enumerate(details_data):
                item = QTableWidgetItem(str(data))
                self.detailTableWidget.setItem(0, i, item)
        else:
            # Si no se encuentran detalles para el cliente, limpiar la tabla
            self.detailTableWidget.setRowCount(0)
