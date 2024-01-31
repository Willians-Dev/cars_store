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
        self._customers_id = None
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/customer_form.ui", self)     
        self.saveCostumerButton.clicked.connect(lambda: self.save_customer())
        self.cancelCostumerBotton.clicked.connect(lambda: self.close())
        self.clear_form_fields() 

    # Metodo para limpiar los campos al abrir el customer_form
             
    def clear_form_fields(self):
        self.firstNameTextLine.setText("")
        self.lastNameTextLine.setText("")
        self.documentTextLine.setText("")
        self.emailTextLine.setText("")
    
    # Método para guardar las categorias a traves del update_categoria
    
    def save_customer(self):
        if self._customers_id:   
            self._customers_model.update_customers(
                self.id_customer,
                self.firstNameTextLine.text(),
                self.lastNameTextLine.text(),
                self.documentTextLine.text(),
                self.emailTextLine.text(),
            )
        else:
            self._customers_model.create_customers(
                self.firstNameTextLine.text(),
                self.lastNameTextLine.text(),
                self.documentTextLine.text(),
                self.emailTextLine.text(),
            )    
        self.customer_saved.emit()
        self.clear_form_fields()                     # Limpiar los campos después de guardar

    def load_customers_data(self, customer_id):
        self.customer_id = customer_id
        customer_data = self._customers_model.get_customers_by_id(customer_id)
        if customer_data:
            self.documentTextLine.setText(customer_data[1])
            self.firstNameTextLine.setText(customer_data[2])
            self.lastNameTextLine.setText(customer_data[3])
            self.emailTextLine.setText(customer_data[4])