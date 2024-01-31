import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_window import MainWindow

app = QApplication(sys.argv)
psycopg_example = MainWindow()
psycopg_example.show()
sys.exit(app.exec())