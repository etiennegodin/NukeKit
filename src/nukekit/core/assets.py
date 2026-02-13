from __future__ import annotations

import getpass
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Literal

import shortuuid

from .versioning import Version

if TYPE_CHECKING:
    from .repository import Repository


logger = logging.getLogger(__name__)


class AssetType(StrEnum):
    GIZMO = "Gizmo"
    SCRIPT = "Script"


class AssetStatus(StrEnum):
    LOCAL = "local"
    NON_LOCAL = "non_local"
    UNPUBLISHED = "unpublished"
    SYNCED = "synced"
    PUBLISHED = "published"
    CACHED = "cached"


INSTALL_STATUS = Literal["non_local", "local"]
PUBLISH_STATUS = Literal["unpublished", "synced", "published"]

ASSET_SUFFIXES = {".gizmo": AssetType.GIZMO, ".nk": AssetType.SCRIPT}


@dataclass
class Asset:
    name: str
    version: Version
    source_path: Path
    status: AssetStatus
    type: AssetType
    message: str = NotImplemented
    author: str = NotImplemented
    time: str = NotImplemented
    id: str = NotImplemented

    def _set_time(self):
        self.time = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def _set_author(self):
        if self.author is None:
            self.author = getpass.getuser()

    def _set_uuid(self):
        unique_id = shortuuid.uuid()[:10]
        self.id = str(unique_id)

    def ensure_message(self):
        """Prompt user for changelog if not provided."""
        while True:
            message = input(
                f"No message found for {self.name}, please enter a message: \n"
            )
            if message:
                break
            else:
                print("\033[1A\033[K", end="")

        self.message = message

    def ensure_metadata(self):
        """Ensure all metadata fields are set."""
        self._set_time()
        self._set_author()
        self._set_uuid()

    def get_remote_path(self, repo: Repository) -> Path:
        """Get the path where this asset should be stored in the repository."""
        repo_path = repo.get_asset_subdir(self.type) / self.name
        # Create asset folder if first publish
        if not repo_path.exists():
            repo_path.mkdir(exist_ok=True)
        return repo_path / f"{self.name}_v{self.version}.gizmo"

    def set_publish_status(self, status: PUBLISH_STATUS):
        self.status = AssetStatus(status)

    def set_install_status(self, status: INSTALL_STATUS):
        self.status = AssetStatus(status)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": str(self.version),
            "author": self.author,
            "id": self.id,
            "message": self.message,
            "status": self.status.value if self.status else None,
            "type": self.type,
            "source_path": str(self.source_path) if self.source_path else None,
        }

    def __str__(self) -> str:
        return f"{self.name}_v{self.version}"

    def __eq__(self, other: object) -> bool:
        """Assets are equal if they have same name, version, and type."""
        if not isinstance(other, Asset):
            return NotImplemented
        return (
            self.name == other.name
            and self.version == other.version
            and self.type == other.type
        )

    def __hash__(self) -> int:
        """Make Asset hashable for use in sets/dicts."""
        return hash((self.name, str(self.version), self.type))

    @classmethod
    def from_path(cls, asset_path: Path) -> Asset:
        """
        Create Asset instance from file path.

        Args:
            context: Current session context
            asset_path: Path to the asset file

        Returns:
            Asset instance (Gizmo or Script)

        Raises:
            TypeError: If file extension is not supported
        """
        # Force Path for stem and suffix methods
        if isinstance(asset_path, str):
            asset_path = Path(asset_path)

        # Get stem & suffix
        asset_stem = asset_path.stem
        asset_suffix = asset_path.suffix

        # Check if naming matches with enforced versioning
        if "_v" in asset_stem:
            asset_name = asset_stem.split(sep="_v")[0]
            asset_version = Version.from_string(asset_stem.split(sep="_v")[1])
        else:
            # No specified version, local asset
            asset_name = asset_stem
            asset_version = Version.from_string("0.0.0")
            logger.info(f"No specified version for {asset_path}")

        # Get object class from path suffix
        asset_type = ASSET_SUFFIXES.get(asset_suffix)

        if asset_type is None:
            raise TypeError(
                "\nProvided asset tpye is not a supported.\n"
                "Please submit a file with this type"
                f"{[str(k) for k in ASSET_SUFFIXES.keys()]} "
            )

        return Asset(
            name=asset_name,
            version=asset_version,
            source_path=asset_path,
            status=AssetStatus.UNPUBLISHED,
            type=asset_type,
        )


"""

        # Check if asset is a copy from repo
        try:
            return context.repo_manifest.data[asset_type][asset_name][asset_version]
        except KeyError:
            # Asset doesn't exist in repo, create new one


"""
