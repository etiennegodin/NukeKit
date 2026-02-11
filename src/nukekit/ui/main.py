from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from ..core.context import Context
from .main_window import MainWindow
from .presenter import MainPresenter


def launch(context: Context):
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(900, 500)
    window.show()

    MainPresenter(context, window)

    sys.exit(app.exec())


if __name__ == "__main__":
    launch()
