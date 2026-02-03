from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QSize, Qt
import sys
from PyQt5 import QtWidgets, uic
import os
import sys 
from pathlib import Path

class Ui(QMainWindow):
    def __init__(self, context):
        super(Ui,self).__init__()
        ui_module_root = Path(__file__).parents[0] 
        ui_file_path = ui_module_root / 'untitled.ui'
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle('NukeKit')
        #self.setFixedSize(QSize(500,500))
        self.show()






