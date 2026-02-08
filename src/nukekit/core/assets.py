from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from .versioning import Version
import logging
import getpass
import shortuuid
from enum import Enum


logger = logging.getLogger(__name__)


ASSET_TYPES = Literal['Gizmo', 'Script']
class AssetType(str, Enum):
    Gizmo = 'Gizmo'
    Script = 'Script'

    def __repr__(self):
        return self.name

class AssetStatus(str, Enum):
    LOCAL = 'local'
    NON_LOCAL = 'non_local'
    UNPUBLISHED = 'unpublished'
    SYNCED = 'synced'
    PUBLISHED = 'published'
    CACHED = 'cached'



INSTALL_STATUS = Literal['non_local', 'local']
PUBLISH_STATUS = Literal["unpublished", 'synced', 'published']



@dataclass
class Asset():
    name:str 
    version: Version = None
    source_path:Path = None
    status:AssetStatus = None
    changelog:str = None
    author: str = None
    time:str = None
    id:str = None
    type:str = None

    def _set_time(self):
        self.time = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def _set_author(self):
        if self.author is None:
            self.author = getpass.getuser()
    
    def _set_uuid(self):
        unique_id = shortuuid.uuid()[:10]
        self.id = str(unique_id)

    def ensure_metadata(self):
        self._set_time()
        self._set_author()
        self._set_uuid()

    def get_remote_path(self, repo:Repository):
        repo_path = repo.get_subdir(self.type) / self.name
        # Create asset folder if first publish 
        if not repo_path.exists():
            repo_path.mkdir(exist_ok=True)

        return repo_path / f"{self.name}_v{self.version}.gizmo"

    def set_publish_status(self, status: PUBLISH_STATUS):
        self.status = AssetStatus(status)

    def set_install_status(self,status: INSTALL_STATUS):
        self.status = AssetStatus(status)

    def __str__(self):
        return f"{self.name}_v{self.version}"
    
    @classmethod
    def from_path(cls, context:Context, asset_path:Path):
    #Force Path for stem and suffix methods
        if isinstance(asset_path, str):
            asset_path = Path(asset_path)

        # Get stem & suffix 
        asset_stem = asset_path.stem
        asset_suffix = asset_path.suffix

        logger.debug(asset_stem)
        logger.debug(asset_suffix)

        # Check if naming matches with enforced versionning
        if "_v" in asset_stem:
            asset_name = asset_stem.split(sep='_v')[0]
            asset_version = Version(asset_stem.split(sep='_v')[1])
        else:
            # No specified version
            asset_name = asset_stem
            asset_version = Version('0.1.0')
            logger.warning(f'No specified version for {asset_name}')

        # Get object class from suffix 
        cls = ASSET_SUFFIXES.get(asset_suffix) 

        if cls:
            # Check if asset is a copy from repo
            try: 
                obj = context.repo_manifest.data[cls.type][asset_name]['versions'][str(asset_version)]
            except Exception as e:
                # New asset 
                return cls(asset_name, asset_version, asset_path, AssetStatus.UNPUBLISHED)
            else:
                return obj
        else:
            raise TypeError(f'\nProvided path is not a supported asset type. \nPlease submit a file with this type {[str(k) for k in ASSET_SUFFIXES.keys()]} ')

        

    
@dataclass
class Gizmo(Asset):
    type:str = "Gizmo"

@dataclass
class Script(Asset):
    type:str = "Script"


ASSET_REGISTRY = {"Gizmo": Gizmo, "Script": Script}
ASSET_SUFFIXES = {".gizmo": Gizmo, ".nk": Script}
