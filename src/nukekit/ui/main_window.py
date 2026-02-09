from __future__ import annotations
import json
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QTreeView,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSplitter,
    QRadioButton,
    QButtonGroup,
)

from ..core.assets import Asset

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asset Browser")

        # Main widgets
        self.tree = QTreeView()
        self.detail = QPlainTextEdit()
        self.detail.setReadOnly(True)

        self.status_icon = QLabel("●")
        self.status_label = QLabel("Status")

        # Layout
        splitter = QSplitter()
        splitter.addWidget(self.tree)
        splitter.addWidget(self.detail)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        main_layout.addLayout(status_layout)

        self.publish_radio = QRadioButton("Publish")
        self.install_radio = QRadioButton("Install")
        self.publish_radio.setChecked(True)

        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.publish_radio)
        self.mode_group.addButton(self.install_radio)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.publish_radio)
        mode_layout.addWidget(self.install_radio)
        mode_layout.addStretch()

        main_layout.insertLayout(0, mode_layout)

    # -------- UI Update Methods --------

    def set_model(self, model: QStandardItemModel):
        self.tree.setModel(model)
        self.tree.expandToDepth(2)

    def show_asset(self, asset: Asset):
        self.detail.setPlainText(
            json.dumps(asset.to_dict(), indent=2)
        )

    def show_text(self, text: str):
        self.detail.setPlainText(text)

    def set_status(self, status: dict):
        raise NotImplementedError
        ok = status.get("db") and status.get("cache")

        if ok:
            self.status_icon.setStyleSheet("color: green;")
            self.status_label.setText("All systems OK")
        else:
            self.status_icon.setStyleSheet("color: orange;")
            self.status_label.setText("Degraded mode")
