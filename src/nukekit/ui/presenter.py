
from .main_window import MainWindow
from .json_tree import JsonTreeBuilder, ROLE_OBJECT
from ..core.context import Context
from ..core.assets import Asset

class MainPresenter:
    def __init__(self, ctx: Context, view: MainWindow):
        self.ctx = ctx
        self.view = view

        self.refresh()

        self.view.tree.selectionModel().selectionChanged.connect(
            self.on_selection_changed
        )

    def refresh(self):
        model = JsonTreeBuilder.build_model(self.ctx.data)
        self.view.set_model(model)
        self.view.set_status(self.ctx.status)

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