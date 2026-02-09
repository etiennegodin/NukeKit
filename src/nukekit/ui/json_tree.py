from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem


ROLE_OBJECT = Qt.UserRole + 1

class JsonTreeBuilder:
    @staticmethod
    def build_model(data: dict) -> QStandardItemModel:
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "Info", "Type"])

        root = model.invisibleRootItem()

        for category, assets in data.items():
            cat_item = QStandardItem(category)
            root.appendRow([cat_item, QStandardItem(""), QStandardItem("Category")])

            for asset_name, asset_data in assets.items():
                asset_item = QStandardItem(asset_name)
                cat_item.appendRow(
                    [asset_item, QStandardItem(""), QStandardItem("Asset")]
                )

                versions = asset_data.get("versions", {})
                versions_item = QStandardItem("versions")
                asset_item.appendRow(
                    [versions_item, QStandardItem(""), QStandardItem("Container")]
                )

                for version, gizmo in versions.items():
                    version_item = QStandardItem(version)
                    info_item = QStandardItem(f"{gizmo.size} KB")
                    type_item = QStandardItem("Gizmo")

                    # Store actual object
                    version_item.setData(gizmo, ROLE_OBJECT)

                    versions_item.appendRow([version_item, info_item, type_item])

        return model