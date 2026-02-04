from __future__ import annotations
from typing import Any

from PyQt5.QtCore import QModelIndex

from ..core.context import Context
from .json_tree import ROLE_VALUE
from .main_window import MainWindow

class MainPresenter:
    def __init__(self, ctx:Context, view:MainWindow):
        self.ctx = ctx
        self.view = view

    def _connect_signals(self) -> None:
        # tree selection
        sel = self.view.ui.treeView.selectionModel()
        sel.selectionChanged.connect(self.on_tree_selection_changed)

        # (optional) refresh button
        # self.view.ui.refreshButton.clicked.connect(self.refresh_all)

    def refresh_all(self) -> None:
        self.view.set_json(self.ctx.repo_manifest)
        #self.view.set_status(self.ctx.status)

        # After model reset, selectionModel changes -> reconnect
        sel = self.view.ui.treeView.selectionModel()
        sel.selectionChanged.connect(self.on_tree_selection_changed)

    def on_tree_selection_changed(self, selected, deselected) -> None:
        idxs = self.view.ui.treeView.selectionModel().selectedIndexes()
        if not idxs:
            return

        idx: QModelIndex = idxs[0]  # column 0 item
        model = self.view.ui.treeView.model()

        # Since we used QStandardItemModel, we can do itemFromIndex
        item = model.itemFromIndex(idx)
        value: Any = item.data(ROLE_VALUE)
        self.view.set_text_preview(value)        