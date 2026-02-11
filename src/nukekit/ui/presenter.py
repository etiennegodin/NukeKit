from ..core.assets import Asset
from ..core.context import AppMode, Context
from .json_tree import ROLE_OBJECT, JsonTreeBuilder
from .main_window import MainWindow


class MainPresenter:
    def __init__(self, ctx: Context, view: MainWindow):
        self.ctx = ctx
        self.view = view

        self.view.publish_radio.toggled.connect(self.on_mode_changed)

        self.refresh()

        self.view.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def refresh(self):
        model = JsonTreeBuilder.build_model(self.ctx.get_current_data())
        self.view.set_model(model)
        # self.view.set_status(self.ctx.status)

        # reconnect after model reset
        self.view.tree.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def on_selection_changed(self):
        index = self.view.tree.currentIndex()
        if not index.isValid():
            return

        model = self.view.tree.model()
        item = model.itemFromIndex(index)
        obj = item.data(ROLE_OBJECT)

        if isinstance(obj, Asset):
            self.view.show_asset(obj)
        else:
            self.view.show_text(item.text())

    def on_mode_changed(self):
        if self.view.publish_radio.isChecked():
            self.ctx.set_mode(AppMode.PUBLISH)
        else:
            self.ctx.set_mode(AppMode.INSTALL)

        self.refresh()
