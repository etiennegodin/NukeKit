from __future__ import annotations

import logging
import shutil
from typing import TYPE_CHECKING

from .repository import Repository

if TYPE_CHECKING:
    from .assets import Asset
    from .context import EnvContext
    from .manifest import Manifest

logger = logging.getLogger(__name__)


def install_all(context: EnvContext):
    raise NotImplementedError("Not implemented")
    pass


def install_from_repo(env: EnvContext):
    raise NotImplementedError("Not implemented")


def install_asset_from_repo(
    env: EnvContext, repo: Repository, local_manifest: Manifest, asset: Asset
) -> bool:
    """
    Docstring for install_asset

    :param context:EnvContext: Description
    :param asset: Description
    :type asset: Asset
    :return: Description
    :rtype: bool
    """
    installed = False
    # Force back type if read from string
    source_path = repo.build_asset_path(asset)
    destination_path = env.user_paths.NUKE_KIT_DIR

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
        logger.info(f"Successfully installed {asset} to local nuke folder")
        asset.set_install_status("local")
        local_manifest.add(asset)
        installed = True

        return installed
