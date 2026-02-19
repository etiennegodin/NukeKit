from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

from ..utils.config import ConfigLoader, ConfigValidator
from ..utils.paths import UserPaths

logger = logging.getLogger(__name__)


class AppMode(StrEnum):
    PUBLISH = "publish"
    INSTALL = "install"
    SCAN = "scan"


def envContextBuilder():
    # Config solver
    config = ConfigLoader().load()
    ConfigValidator.validate(config)

    return EnvContext(
        nuke_version="",
        config=config,
        user_paths=UserPaths(),
    )


@dataclass(frozen=True)
class EnvContext:
    nuke_version: str
    config: dict
    user_paths: UserPaths
