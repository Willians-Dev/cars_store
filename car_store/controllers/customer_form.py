import pathlib
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from models.customer_model import CustomersModel
from PyQt5 import uic

class CustomerForm(QMainWindow):
    customer_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self._customers_model = CustomersModel()
        self.customers_id = None
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/customer_form.ui", self) 

        css_path = pathlib.Path(__file__).parent.parent / "views/styles.css"
        with open(css_path, "r") as f:
            self.setStyleSheet(f.read())

        self.saveCostumerButton.clicked.connect(lambda: self.save_customer())
        self.cancelCostumerBotton.clicked.connect(lambda: self.close())
  
    # Método para guardar las categorias a traves del update_categoria
    
    def save_customer(self):
        if self.customers_id:   
             self._customers_model.update_customer(
                self.customers_id,
                self.documentTextLine.text(),
                self.firstNameTextLine.text(),
                self.lastNameTextLine.text(),
                self.emailTextLine.text()
        )
        else:
            self._customers_model.create_customer(
                self.documentTextLine.text(),
                self.firstNameTextLine.text(),
                self.lastNameTextLine.text(),
                self.emailTextLine.text()
            )    
        self.customer_saved.emit()
        self.close()                   # Limpiar los campos después de guardar

    def load_customers_data(self, customer_id):
        self.customers_id = customer_id
        customer_data = self._customers_model.get_customer_by_id(customer_id)
        if customer_data:
            self.documentTextLine.setText(str(customer_data[1]))
            self.firstNameTextLine.setText(customer_data[2])
            self.lastNameTextLine.setText(customer_data[3])
            self.emailTextLine.setText(customer_data[4])

    def reset_form(self):
        self.documentTextLine.setText("")
        self.firstNameTextLine.setText("")
        self.lastNameTextLine.setText("")
        self.emailTextLine.setText("")
        self.customers_id = None