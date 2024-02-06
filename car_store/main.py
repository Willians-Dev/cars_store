import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_window import MainWindow

app = QApplication(sys.argv)
catalog_cars = MainWindow()
catalog_cars.show()
sys.exit(app.exec())