from __future__ import annotations

import logging
import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .assets import Asset
    from .context import Context

logger = logging.getLogger(__name__)

class Installer:
    def __init__(self, context:Context):
        self.context = context

    def install_all(self):
        raise NotImplementedError("Not implemented")
        pass

    def install_from_repo(self):
        raise NotImplementedError("Not implemented")

    def install_asset(self, asset:Asset) -> bool:
        """
        Docstring for install_asset

        :param self: Description
        :param asset: Description
        :type asset: Asset
        :return: Description
        :rtype: bool
        """
        installed = False
        #Force back type if read from string
        source_path = asset.get_remote_path(self.context.repo)
        destination_path = self.context.user_paths.NUKE_KIT_DIR

        try:
            shutil.copy2(source_path, destination_path)
        except shutil.SameFileError:
            logger.error("Source and destination represent the same file.")
        except PermissionError:
            logger.error("Permission denied.")
        except FileNotFoundError:
            logger.error("The source file or destination directory was not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        else:
            logger.info(f"Successfully saved {asset} to {destination_path} ")
            asset.set_install_status("local")
            self.context.local_manifest.update(asset)
            installed = True

        return installed
