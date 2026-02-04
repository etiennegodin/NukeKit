# json_tree.py
from __future__ import annotations
from typing import Any
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

ROLE_PATH = Qt.UserRole + 1
ROLE_VALUE = Qt.UserRole + 2

def build_json_model(data: Any) -> QStandardItemModel:
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Asset", "Version", "Type"])
    _fill_item(model.invisibleRootItem(), data, path=())
    return model

def _fill_item(parent: QStandardItem, obj: Any, path: tuple) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            _append_row(parent, key=str(k), value=v, path=path + (k,))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            _append_row(parent, key=f"[{i}]", value=v, path=path + (i,))
    else:
        # leaf scalar (shouldn't happen at root often, but safe)
        _append_row(parent, key="value", value=obj, path=path)

def _append_row(parent: QStandardItem, key: str, value: Any, path: tuple) -> None:
    key_item = QStandardItem(key)

    is_container = isinstance(value, (dict, list))
    val_item = QStandardItem("" if is_container else str(value))
    type_item = QStandardItem(type(value).__name__)

    key_item.setData(path, ROLE_PATH)
    key_item.setData(value, ROLE_VALUE)

    parent.appendRow([key_item, val_item, type_item])

    if is_container:
        _fill_item(key_item, value, path=path)
