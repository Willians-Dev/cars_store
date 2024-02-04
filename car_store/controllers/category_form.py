import pathlib
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal
from models.category_model import CategoryModel
from PyQt5 import uic

class CategoryForm(QMainWindow):
    category_saved = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self._category_model = CategoryModel()
        self.category_id = None
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/category_form.ui", self)     
        self.saveCategoryButton.clicked.connect(lambda: self.save_category())
        self.cancelCategoryButton.clicked.connect(lambda: self.close())

    # Método para guardar las categorias a traves del update_categoria
    
    def save_category(self):
        if self.category_id:
            self._category_model.update_categories(
                self.category_id,
                self.categoryNameLineText.text(),
                self.categoryDescriptionLineText.text(),
            )
        else:
            self._category_model.create_categories(
                self.categoryNameLineText.text(),
                self.categoryDescriptionLineText.text(),
            )    
        self.category_saved.emit()
        self.close()                     # Limpiar los campos después de guardar

    def load_category_data(self, category_id):
        self.category_id = category_id
        category_data = self._category_model.get_category_by_id(category_id)
        if category_data:
            self.categoryNameLineText.setText(category_data[1])
            self.categoryDescriptionLineText.setText(category_data[2])
            
    def reset_form(self):
        self.categoryNameLineText.setText("")
        self.categoryDescriptionLineText.setText("")
        self.category_id = None