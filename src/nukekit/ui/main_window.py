from __future__ import annotations
import json
from typing import Any
from PyQt5.QtWidgets import QMainWindow
from .ui import Ui_MainWindow
from .json_tree import build_json_model
from ..utils.json import UniversalEncoder

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('NukeKit')
        self.show()

    # ---------- UI update methods ----------
    def set_json(self, data: dict[str, Any]) -> None:
        model = build_json_model(data)
        self.ui.treeView.setModel(model)
        self.ui.treeView.expandToDepth(1)


    def set_text_preview(self, value: Any) -> None:
        if isinstance(value, (dict, list)):
            text = json.dumps(value, indent=2, ensure_ascii=False, cls=UniversalEncoder)
        else:
            text = str(value)
        self.ui.textBrowser.setPlainText(text)


#pyuic5 nukekit.ui -o ui.py

