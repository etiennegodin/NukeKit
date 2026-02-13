from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from ..utils import UserPaths
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
    repo: Repository,
    local_manifest: Manifest,
    asset: Asset,
    destination_path: Path | None = None,
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

    if destination_path is None:
        destination_path = UserPaths.NUKE_KIT_DIR
    elif isinstance(destination_path, str):
        destination_path = Path(destination_path)
    elif not isinstance(destination_path, Path):
        raise TypeError("Destination path not valid")

    # Force back type if read from string
    source_path = repo.build_asset_path(asset)
    logger.debug(source_path)
    logger.debug(destination_path)
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
