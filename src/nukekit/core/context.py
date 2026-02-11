from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Literal

from .manifest import Manifest

if TYPE_CHECKING:
    from ..utils.paths import UserPaths
    from .repository import Repository

logger = logging.getLogger(__name__)


class AppMode(StrEnum):
    PUBLISH = "publish"
    INSTALL = "install"
    SCAN = "scan"


APP_MODE = Literal["publish", "install", "scan"]


@dataclass
class Context:
    """
    Main class for session context

    :param repo: Repository instance from this session
    :type repo: Repository
    :param user_paths: UserPaths instance from this session
    :type user_paths: UserPaths
    :param config: Dictionnary read from ConfigLoader class
    :type config: dict
    :param repo_manifest: Manifest instance from remote repository state
    :type repo_manifest: Manifest
    :param local_manifest: Manifest instance from cached local state
    :type local_manifest: Manifest
    :param local_state: Manifest instance from local state
    :type local_state: Manifest


    """

    repo: Repository
    user_paths: UserPaths
    config: dict[str, Any]
    repo_manifest: Manifest = NotImplemented
    local_manifest: Manifest = NotImplemented
    local_state: Manifest = NotImplemented
    mode: AppMode = NotImplemented

    def __post_init__(self):
        # Read cached manifests from disk
        self.repo_manifest = Manifest.from_file(self.repo.MANIFEST)
        self.local_manifest = Manifest.from_file(self.user_paths.CACHED_MANIFEST)

        # Create local state manifest from scanner
        self.local_state = Manifest.from_scanner(self)

        # Set specific install status for repo assets

    def set_mode(self, mode: APP_MODE):
        self.mode = AppMode(mode)

    def get_current_data(self) -> dict[str, Any]:
        if self.mode == AppMode.PUBLISH:
            return self.local_state.data
        elif self.mode == AppMode.INSTALL:
            return self.repo_manifest.data
        else:
            raise NotImplementedError(f"App mode {self.mode} is not implemented")
