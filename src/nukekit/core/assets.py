from __future__ import annotations
from typing import TYPE_CHECKING, Literal, Self
import logging
from enum import Enum
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

import getpass
import shortuuid

from .versioning import Version

if TYPE_CHECKING:
    from .repository import Repository
    from .context import Context


logger = logging.getLogger(__name__)

ASSET_TYPES = Literal["Gizmo", "Script"]

class AssetStatus(str, Enum):
    LOCAL = "local"
    NON_LOCAL = "non_local"
    UNPUBLISHED = "unpublished"
    SYNCED = "synced"
    PUBLISHED = "published"
    CACHED = "cached"

INSTALL_STATUS = Literal["non_local", "local"]
PUBLISH_STATUS = Literal["unpublished", "synced", "published"]

@dataclass
class Asset():
    name:str 
    version: Version = None
    source_path:Path = None
    status:AssetStatus = None
    message:str = None
    author: str = None
    time:str = None
    id:str = None
    type:str = None

    @classmethod
    def from_path(
        cls,
        context:Context,
        asset_path:Path
    ) -> Self :
        """
        Construct an Asset from a path
        
        :param context: Current context used to parse remote repository
        :type context: Context
        :param asset_path: Path to construct asset from
        :type asset_path: Path
        :return: Asset instance constructed
        :rtype: Self
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
            asset_version = Version(asset_stem.split(sep="_v")[1])
        else:
            # No specified version, local asset
            asset_name = asset_stem
            asset_version = Version.from_string("0.0.0")
            logger.info(f"No specified version for {asset_path}")

        # Get object class from path suffix
        try:
            cls = ASSET_SUFFIXES.get(asset_suffix) 
        except KeyError:
            raise TypeError(f"\nProvided asset tpye is not a supported.\nPlease submit a file with this type {[str(k) for k in ASSET_SUFFIXES.keys()]} ")

        if cls:
            # Check if asset is a copy from repo
            try: 
                return context.repo_manifest.data[cls.type][asset_name][asset_version]
            except KeyError:
                # Asset doesn't exist in repo, create new one
                return cls(
                    name = asset_name,
                    version = asset_version,
                    source_path = asset_path,
                    status = AssetStatus.UNPUBLISHED,
                    type = cls.type)

    def ensure_message(self):
        while True:
            message = input(f"No message found for {self.name}, please enter a message: \n")
            if message:
                break
            else:
                print("\033[1A\033[K", end="") 

        self.message = message

    def ensure_metadata(self):
        """
        Adds time, author and uuid metadata to asset
    
        """
        self._set_time()
        self._set_author()
        self._set_uuid()

    def set_publish_status(self, status: PUBLISH_STATUS):
        self.status = AssetStatus(status)

    def set_install_status(self,status: INSTALL_STATUS):
        self.status = AssetStatus(status)

    def get_remote_path(self, repo:Repository) -> Path:
        repo_path = repo.get_asset_subdir(self.type) / self.name
        # Create asset folder if first publish 
        if not repo_path.exists():
            repo_path.mkdir(exist_ok=True)
        return repo_path / f"{self.name}_v{self.version}.gizmo"


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
    
    def _set_time(self):
        self.time = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def _set_author(self):
        if self.author is None:
            self.author = getpass.getuser()
    
    def _set_uuid(self):
        unique_id = shortuuid.uuid()[:10]
        self.id = str(unique_id)
    
    def __str__(self):
        return f"{self.name}_v{self.version}"
@dataclass
class Gizmo(Asset):
    type:str = "Gizmo"

@dataclass
class Script(Asset):
    type:str = "Script"


ASSET_REGISTRY = {"Gizmo": Gizmo, "Script": Script}
ASSET_SUFFIXES = {".gizmo": Gizmo, ".nk": Script}
