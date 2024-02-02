import pathlib
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHeaderView, QMessageBox, QMainWindow
from PyQt5 import uic, QtCore
from models.customer_model import CustomersModel
from controllers.customer_form import CustomerForm
from models.database_model import DatabaseConnection

class CustomersTable(QMainWindow):
    def __init__(self):
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_costumer.ui", self)
        self.customerForm = CustomerForm()
        self._customer_model = CustomersModel()
        self.load_customer()

        self.addNewCustomerForm.triggered.connect(lambda: self.create_customer())
        self.customerForm.customer_saved.connect(self.load_customer) 
  
    def load_customer(self):
        customer_list = self._customer_model.get_customers()
        self.costumerTableWidget.setRowCount(len(customer_list))
        for i, customer in enumerate(customer_list):
            id_customer, document, first_name, last_name, email = customer
            self.costumerTableWidget.setItem(i, 0, QTableWidgetItem(str(id_customer)))
            self.costumerTableWidget.setItem(i, 1, QTableWidgetItem(str(document)))
            self.costumerTableWidget.setItem(i, 2, QTableWidgetItem(str(first_name)))
            self.costumerTableWidget.setItem(i, 3, QTableWidgetItem(str(last_name)))
            self.costumerTableWidget.setItem(i, 4, QTableWidgetItem(str(email)))
            self.costumerTableWidget.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.costumerTableWidget.item(i, 1).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.costumerTableWidget.item(i, 2).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.costumerTableWidget.item(i, 3).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.costumerTableWidget.item(i, 4).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            # Botón para editar los clientes
             
            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(self.edit_customer)
            edit_button.setProperty("row", i)
            self.costumerTableWidget.setCellWidget(i, 5, edit_button)

            # Botón para Borrar las categoreias

            delete_button = QPushButton("Borrar")
            delete_button.clicked.connect(self.delete_customer)
            delete_button.setProperty("row", i)
            self.costumerTableWidget.setCellWidget(i, 6, delete_button)
    
        # Ajustar automáticamente el tamaño de todas las columnas
        # self.studentsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.costumerTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Ajustar a contenido para la primera columna
        self.costumerTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Estirar automáticamente para las otras columnas
        self.costumerTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.costumerTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.costumerTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.costumerTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def edit_customer(self):
        sender = self.sender()
        row = sender.property("row")
        customer_id = self.costumerTableWidget.item(row, 0).text()
        self.customerForm.load_customers_data(customer_id)
        self.customerForm.show()

    # Metodo para la eliminación de los resgistro a travez del category model
        
    def create_customer(self):
        self.customerForm.reset_form()
        self.customerForm.show()

    def delete_customer(self):
        sender = self.sender()
        row = sender.property("row")
        customer_id = self.costumerTableWidget.item(row, 0).text()
        
        # Mostrar un Mensaje para confirmar la eliminación
        
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(f"¿Está seguro de querer borrar el cliente con ID {customer_id}?")
        msgBox.setWindowTitle("Confirmar eliminación")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        
        if ret == QMessageBox.Yes:
            self._customer_model.delete_customer(customer_id)
            self.load_customer()                               # Volver a cargar la lista de las categorias después de eliminar
        
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
