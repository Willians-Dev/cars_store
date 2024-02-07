import pathlib
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QCheckBox
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
        self.load_customers()
        self.update_current_datetime()
        self.load_purchase_form()
        self.SaveCompraButton.clicked.connect(self.save_purchase)
        self.CancelCompraButton.clicked.connect(self.close)

        for i in range(self.purchaseTableWidget.rowCount()):
            checkbox_item = self.purchaseTableWidget.cellWidget(i, 0)
            if isinstance(checkbox_item, QCheckBox):
                checkbox_item.stateChanged.connect(self.update_total_price)

    def load_customers(self):
        customers = self._customer_model.get_customers()  # Método para obtener el cliente del customer_model
        self.customerPurchaseComboBox.clear()
        for id_customer, _ , first_name, last_name, _ in customers:
            self.customerPurchaseComboBox.addItem(f"{first_name} {last_name}", userData=id_customer)  # Agregar solo el firstname y lastname al combo box, pero almacenar el id_customer como userData
        # Método para guardar los customers a traves del update_custoemrs
            
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
            id_purchase, model, category_name, price = order
            checkbox = QCheckBox()  # Crear un checkbox
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")  # Establecer el estilo para centrar el checkbox
            self.purchaseTableWidget.setCellWidget(i, 0, checkbox)  # Agregar el checkbox a la celda
            self.purchaseTableWidget.setItem(i, 1, QTableWidgetItem(str(id_purchase)))
            self.purchaseTableWidget.setItem(i, 2, QTableWidgetItem(str(model)))
            self.purchaseTableWidget.setItem(i, 3, QTableWidgetItem(str(category_name)))
            self.purchaseTableWidget.setItem(i, 4, QTableWidgetItem(str(price)))

        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Ajustar a contenido para la primera columna
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Estirar automáticamente para las otras columnas
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.purchaseTableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.purchaseTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Ocultar la columna de numeración
        self.purchaseTableWidget.verticalHeader().setVisible(False)

    def update_total_price(self):
        # Lógica para calcular el precio total basado en los QCheckBox
        total_price = 0
        for i in range(self.purchaseTableWidget.rowCount()):
            checkbox_item = self.purchaseTableWidget.cellWidget(i, 0)
            if isinstance(checkbox_item, QCheckBox) and checkbox_item.isChecked():
                # Verificar si hay un QTableWidgetItem en la celda de la columna 4
                item = self.purchaseTableWidget.item(i, 4)
                if item is not None:
                    # Si hay un QTableWidgetItem, obtener su texto y convertirlo a float
                    price_text = item.text()
                    price = float(price_text)
                    total_price += price

        # Actualizar la etiqueta de precio total
        self.priceTotalLabel.setText(f"{total_price:.2f}")

    def save_purchase(self):
        id_customer = self.customerPurchaseComboBox.currentData()   # Obtener el id del cliente seleccionado del combobox
        date = self.CompraDateTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")   # Obtener la fecha y hora actual
        total_price = float(self.priceTotalLabel.text())    # Obtener el precio total de la etiqueta
        
        # Obtener el id_purchase de la fila seleccionada en la tabla de compras
        selected_row = self.purchaseTableWidget.currentRow()
        id_purchase_item = self.purchaseTableWidget.item(selected_row, 1)
        
        if id_purchase_item is not None:
            id_purchase = int(id_purchase_item.text())  # Sumar 1 al id_purchase obtenido
            self._purchase_model.save_purchase(id_customer, date, total_price, id_purchase)   # Guardar la compra
            self.purchase_saved.emit()   # Emitir señal de que la compra ha sido guardada 
            self.close()   # Cerrar la ventana
        else:
            # Manejar el caso en que no se seleccionó ninguna fila o no se encontró el id_purchase
            print("No se seleccionó ninguna fila o el id_purchase no está disponible")


    def reset_form(self):
            self._purchase_id = None