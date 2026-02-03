from __future__ import annotations
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets, uic
from pathlib import Path
from ..core.context import Context

class Ui(QMainWindow):
    def __init__(self, context:Context):
        super(Ui,self).__init__()
        ui_module_root = Path(__file__).parents[0] 
        ui_file_path = ui_module_root / 'nukekit.ui'
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle('NukeKit')
        self.show()

    def _update_textBrowser(self, msg:str):
        self.textBrowser.setPlainText(msg)

    







