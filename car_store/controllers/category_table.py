import pathlib
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHeaderView, QMessageBox, QMainWindow
from PyQt5 import uic, QtCore
from models.category_model import CategoryModel
from controllers.category_form import CategoryForm

class CategoryTable(QMainWindow):
    def __init__(self):
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_category.ui", self)
        self._category_model = CategoryModel()
        self.load_category()
        self.categoryForm = CategoryForm()
        self.newCategoryFormButton.triggered.connect(lambda: self.categoryForm.show())
        self.categoryForm.category_saved.connect(self.on_category_saved) 

    def on_category_saved(self):
        self.categoryForm.close()
        self.load_category()

        # Metodo para cargar la base de datos en el category_table
    
    def load_category(self):
        category_list = self._category_model.get_categories()
        self.categoryTable.setRowCount(len(category_list))
        for i, category in enumerate(category_list):
            id_category, category_name, description = category
            self.categoryTable.setItem(i, 0, QTableWidgetItem(str(id_category)))
            self.categoryTable.setItem(i, 1, QTableWidgetItem(str(category_name)))
            self.categoryTable.setItem(i, 2, QTableWidgetItem(str(description)))
            self.categoryTable.item(i, 0).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

            # Botón para editar las categorias
             
            edit_button = QPushButton("Editar")
            edit_button.clicked.connect(self.edit_category)
            edit_button.setProperty("row", i)
            self.categoryTable.setCellWidget(i, 3, edit_button)

            # Botón para Borrar las categoreias

            delete_button = QPushButton("Borrar")
            delete_button.clicked.connect(self.delete_category)
            delete_button.setProperty("row", i)
            self.categoryTable.setCellWidget(i, 4, delete_button)
    
        # Ajustar automáticamente el tamaño de todas las columnas
        # self.studentsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.categoryTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Ajustar a contenido para la primera columna
        self.categoryTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Estirar automáticamente para las otras columnas
        self.categoryTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.categoryTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def edit_category(self):
        sender = self.sender()
        row = sender.property("row")
        category_id = self.categoryTable.item(row, 0).text()
        self.categoryForm.load_category_data(category_id)
        self.categoryForm.show()

    # Metodo para la eliminación de los resgistro a travez del category model
        
    def delete_category(self):
        sender = self.sender()
        row = sender.property("row")
        category_id = self.categoryTable.item(row, 0).text()
        
        # Mostrar un Mensaje para confirmar la eliminación
        
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(f"¿Está seguro de querer borrar la categoria con ID {category_id}?")
        msgBox.setWindowTitle("Confirmar eliminación")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        
        if ret == QMessageBox.Yes:
            self._category_model.delete_category(category_id)
            self.load_category()                               # Volver a cargar la lista de las categorias después de eliminar
        
            #Mensaje de confirmación de borrado de registro con éxito

            success_msg = QMessageBox()
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setText("Operación realizada con éxito")
            success_msg.setWindowTitle("Confirmación")
            success_msg.exec_()

    def closeEvent(self, ev) -> None:
        self._category_model.close()
        return super().closeEvent(ev)

