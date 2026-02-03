from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QSize, Qt

import sys 

class MainWindow(QMainWindow):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle('NukeKit')
        self.setFixedSize(QSize(500,500))


