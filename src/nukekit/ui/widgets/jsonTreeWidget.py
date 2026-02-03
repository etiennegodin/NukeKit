
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeView
from PyQt5 import QtWidgets


class JsonTreeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(JsonTreeWidget, self).__init__(parent)
        self.treeView = QTreeView()
        self.treeView.setHeader(["Key", "Value"])
        self.treeView.setColumnCount(2)

    def fill_tree(self, data):
        """Initializes the tree view with data."""
        self.clear()
        self.fill_item(self.invisibleRootItem(), data)
    
    def fill_item(self,item, value):
        """Recursively fills tree items from a JSON dictionary."""
        if isinstance(value, dict):
            for key, val in value.items():
                child = QTreeWidgetItem([key])
                self.fill_item(child, val)
                item.addChild(child)
        elif isinstance(value, list):
            for i, val in enumerate(value):
                child = QTreeWidgetItem([str(i)])
                self.fill_item(child, val)
                item.addChild(child)
        else:
            # If value is not a container, add it to the column
            item.setText(1, str(value))

