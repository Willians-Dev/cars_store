import pathlib
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt, pyqtSignal
from models.cars_model import CarsModel
from models.category_model import CategoryModel
from PyQt5 import uic

class CarsForm(QMainWindow):
    cars_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self._cars_model = CarsModel()
        self._category_model = CategoryModel()
        self._cars_id = None
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/cars_form.ui", self)

        css_path = pathlib.Path(__file__).parent.parent / "views/styles.css"
        with open(css_path, "r") as f:
            self.setStyleSheet(f.read())
            
        self.saveCarsButton.clicked.connect(lambda: self.save_cars())
        self.cancelCarsButton.clicked.connect(lambda: self.close())
        self.load_categories()

    def load_categories(self):
        categories = self._category_model.get_categories()  # Método para obtener las categorías del modelo
        self.categoryComboBox.clear()
        for category_id, category_name, _ in categories:
            self.categoryComboBox.addItem(category_name, userData=category_id)  # Agregar solo el category_name al combo box, pero almacenar el id_category como userData
        # Método para guardar las categorias a traves del update_categoria
    
    def save_cars(self):
        if self._cars_id:   
            category_id = self.categoryComboBox.currentData()  # Obtener el id_category seleccionado
            self._cars_model.update_cars(
                self._cars_id,
                self.serialTextLine.text(),
                self.brandTextLine.text(),
                self.modelTextLine.text(),
                self.transmisionTextLine.text(),
                self.priceTextLine.text(),
                self.yearTextLine.text(),
                category_id  # Pasar el id_category como argumento
            )
        else:
            category_id = self.categoryComboBox.currentData()  # Obtener el id_category seleccionado
            self._cars_model.create_cars(
                self.serialTextLine.text(),
                self.brandTextLine.text(),
                self.modelTextLine.text(),
                self.transmisionTextLine.text(),
                self.priceTextLine.text(),
                self.yearTextLine.text(),
                category_id  # Pasar el id_category como argumento
            )    
        self.cars_saved.emit()
        self.close()  

    def load_cars_data(self, cars_id):
        self.cars_id = cars_id
        cars_data = self._cars_model.get_cars_by_id(cars_id)
        if cars_data:
            self.serialTextLine.setText(cars_data[1])
            self.brandTextLine.setText(cars_data[2])
            self.modelTextLine.setText(cars_data[3])
            self.transmisionTextLine.setText(cars_data[4])
            self.priceTextLine.setText(str(cars_data[5]))
            self.yearTextLine.setText(str(cars_data[6]))

        # Metodo para limpiar los campos al abrir el studen_form 
    def reset_form(self):
        self.serialTextLine.setText("")
        self.brandTextLine.setText("")
        self.modelTextLine.setText("")
        self.transmisionTextLine.setText("")
        self.priceTextLine.setText("")
        self.yearTextLine.setText("")
        self._cars_id = None