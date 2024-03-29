import pathlib
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QHeaderView, QMessageBox, QMainWindow
from PyQt5 import uic, QtCore
from models.cars_model import CarsModel
from models.database_model import DatabaseConnection
from controllers.cars_form import CarsForm

class CarsTable(QMainWindow):
    def __init__(self):
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_cars.ui", self)

        css_path = pathlib.Path(__file__).parent.parent / "views/styles.css"
        with open(css_path, "r") as f:
            self.setStyleSheet(f.read())

        self.carsrForm = CarsForm()
        self._cars_model = CarsModel()
        self.load_cars()
        self.newCarFormButton.triggered.connect(lambda: self.create_cars())
        self.carsrForm.cars_saved.connect(self.load_cars)
        self.quitCarsFormButton.triggered.connect(self.close)
        
        # Metodo para cargar la base de datos en el cars_table
    
    def load_cars(self):
        cars_list = self._cars_model.get_cars()
        self.carsTableWidget.setRowCount(len(cars_list))
        for i, cars in enumerate(cars_list):
            id_car, serial_number, brand, model, category_name, transmission, price, year, *extra = cars
            self.carsTableWidget.setItem(i, 0, QTableWidgetItem(str(id_car)))
            self.carsTableWidget.setItem(i, 1, QTableWidgetItem(str(serial_number)))
            self.carsTableWidget.setItem(i, 2, QTableWidgetItem(str(brand)))
            self.carsTableWidget.setItem(i, 3, QTableWidgetItem(str(model)))
            self.carsTableWidget.setItem(i, 4, QTableWidgetItem(str(category_name)))  # Columna de nombre de categoría
            self.carsTableWidget.setItem(i, 5, QTableWidgetItem(str(transmission)))
            self.carsTableWidget.setItem(i, 6, QTableWidgetItem(str(price)))
            self.carsTableWidget.setItem(i, 7, QTableWidgetItem(str(year)))
            self.carsTableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 3).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 4).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 5).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 6).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.carsTableWidget.item(i, 7).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            # Botón para editar los carros
             
            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(self.edit_cars)
            edit_button.setProperty("row", i)
            self.carsTableWidget.setCellWidget(i, 8, edit_button)

            # Botón para Borrar las carros

            delete_button = QPushButton("Borrar")
            delete_button.clicked.connect(self.delete_cars)
            delete_button.setProperty("row", i)
            self.carsTableWidget.setCellWidget(i, 9, delete_button)
        
        # Ajustar automáticamente el tamaño de todas las columnas
        # self.studentsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.carsTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Ajustar a contenido para la primera columna
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Estirar automáticamente para las otras columnas
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.carsTableWidget.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.carsTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def edit_cars(self):
        sender = self.sender()
        row = sender.property("row")
        cars_id = self.carsTableWidget.item(row, 0).text()
        self.carsrForm.load_cars_data(cars_id)
        self.carsrForm.show()

    def create_cars(self):
        self.carsrForm.reset_form()
        self.carsrForm.show()

    # Metodo para la eliminación de los resgistro a travez del cars model
        
    def delete_cars(self):
        sender = self.sender()
        row = sender.property("row")
        cars_id = self.carsTableWidget.item(row, 0).text()
        
        # Mostrar un Mensaje para confirmar la eliminación
        
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(f"¿Está seguro de querer borrar el cliente con ID {cars_id}?")
        msgBox.setWindowTitle("Confirmar eliminación")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        
        if ret == QMessageBox.Yes:
            self._cars_model.delete_cars(cars_id)
            self.load_cars()                               # Volver a cargar la lista de los carros después de eliminar
        
            #Mensaje de confirmación de borrado de registro con éxito

            success_msg = QMessageBox()
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setText("Operación realizada con éxito")
            success_msg.setWindowTitle("Confirmación")
            success_msg.exec_()

    def closeEvent(self, ev) -> None:
        db = DatabaseConnection()
        db.close()
        return super().closeEvent(ev)
