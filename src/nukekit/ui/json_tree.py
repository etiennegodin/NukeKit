from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel

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

            for asset_name, asset_versions in assets.items():
                asset_item = QStandardItem(asset_name)
                cat_item.appendRow([asset_item, QStandardItem(""), QStandardItem("Asset")])
                print(asset_versions)

                for version, asset in asset_versions.items():
                    print(asset)
                    version_item = QStandardItem(version)
                    info_item = QStandardItem(f"{asset.message}")
                    type_item = QStandardItem("Gizmo")

                    # Store actual object
                    version_item.setData(asset, ROLE_OBJECT)

                    asset_item.appendRow([version_item, info_item, type_item])

        return model
