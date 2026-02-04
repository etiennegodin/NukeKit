from __future__ import annotations
import sys
from PyQt5.QtWidgets import QApplication

from .main_window import MainWindow
from .presenter import MainPresenter

from ..core.context import Context
from pprint import pprint

def launchUi(context:Context):
    app = QApplication(sys.argv)
    ui = MainWindow()
    presenter = MainPresenter(context, ui)
    presenter.refresh_all()
    sys.exit(app.exec_())
