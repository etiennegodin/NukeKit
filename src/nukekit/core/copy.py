from __future__ import annotations

import logging
import shutil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def copy_asset(source_path, destination_path) -> bool:
    copied = False

    try:
        shutil.copy2(source_path, destination_path)
        logger.info(f"Successfully saved {destination_path}")
        copied = True

    except shutil.SameFileError:
        logger.error("Source and destination represent the same file.")
    except PermissionError:
        logger.error("Permission denied.")
    except FileNotFoundError:
        logger.error("The source file or destination directory was not found.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return copied
