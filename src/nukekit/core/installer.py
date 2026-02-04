from __future__ import annotations
import shutil
import logging

from ..core.assets import Asset
from .context import Context
from ..core.versioning import Version
from .manifest import Manifest 
from ..utils.ux import user_input_choice


class Installer():
    def __init__(self, context:Context):
        self.context = context

    def install_all(self):
        pass

    def install_asset(self, asset:Asset):

        pass


    