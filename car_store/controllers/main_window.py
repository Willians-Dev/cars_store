from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton
from PyQt5 import uic
import pathlib
from controllers.category_table import CategoryTable
from controllers.customer_table import CustomersTable
from controllers.cars_table import CarsTable

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_window.ui", self)

        self._category_table = CategoryTable() 
        self._customer_table = CustomersTable()
        self._cars_table = CarsTable()

        self.category_main_button = self.findChild(QPushButton, "categoryMainButton")
        self.category_main_button.clicked.connect(self.open_categoryTable)

        self.product_main_button = self.findChild(QPushButton, "carsMainButton")
        self.product_main_button.clicked.connect(self.open_cars_window)

        self.customer_main_button = self.findChild(QPushButton, "customerMainButton")
        self.customer_main_button.clicked.connect(self.open_customers_window)

        self.purchase_main_button = self.findChild(QPushButton, "purchaseMainButton")
        self.purchase_main_button.clicked.connect(self.open_purchases_window)

    def open_categoryTable(self):
        self._category_table.show()

    def open_cars_window(self):
        self._cars_table.show()

    def open_customers_window(self):
        self._customer_table.show()

    def open_purchases_window(self):
        print("Abrir ventana de compras")