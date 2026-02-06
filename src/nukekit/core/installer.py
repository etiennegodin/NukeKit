from __future__ import annotations
import shutil
import logging
from pathlib import Path

from ..core.assets import Asset
from .context import Context
from ..core.versioning import Version
from .manifest import Manifest 
from ..utils.ux import user_input_choice
from .assets import asset_factory
logger = logging.getLogger(__name__)

class Installer():
    def __init__(self, context:Context):
        self.context = context

    def install_all(self):
        pass

    def install_asset(self, asset_path:Path):

        asset = asset_factory(asset_path)
        source_path = asset.get_remote_path(self.context.repo)
        destination_path = self.context.user_paths.NUKE_KIT_DIR

        try:
            shutil.copy2(source_path, destination_path )
            logger.info(f"Successfully saved {asset} to {destination_path} ")
            asset.set_install_status('local')
            self.context.local_manifest.update(asset)

            return True
        except shutil.SameFileError as e :
            print("Source and destination represent the same file.")
        except PermissionError:
            print("Permission denied.")
        except FileNotFoundError:
            print("The source file or destination directory was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        pass


    