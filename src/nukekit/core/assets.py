from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Literal
from .versioning import Version
import logging
import getpass
import uuid
from enum import Enum


class AssetStatus(str, Enum):
    LOCAL = 'local'
    NON_LOCAL = 'non_local'
    UNPUBLISHED = 'unpublished'
    SYNCED = 'synced'
    PUBLISHED = 'published'



INSTALL_STATUS = Literal['non_local', 'local']
PUBLISH_STATUS = Literal["unpublished", 'synced']


logger = logging.getLogger(__name__)

@dataclass
class Asset():
    name:str 
    source_path:str|Path
    version: Version = None
    changelog:str = None
    author: str = None
    destination_path: Path = None
    time:str = None
    id:str = None
    type:str = 'Asset'
    status:AssetStatus = None


    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.source_path, str):
            self.source_path  = Path(self.source_path)

    def _set_time(self):
        self.time = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def _set_author(self):
        if self.author is None:
            self.author = getpass.getuser()
    
    def _set_uuid(self):
        unique_id = uuid.uuid4()
        self.id = str(unique_id)

    def ensure_metadata(self):
        self._set_time()
        self._set_author()
        self._set_uuid()

    def update_destination_path(self, repo:Repository):
        asset_type_root = repo.get_subdir(self.type)
        assets_list = repo.list_assets(self.type)

        asset_folder = asset_type_root / self.name
        asset_path = asset_folder/ f"{self.name}_v{self.version}.gizmo"

        # Create folder if not existing 
        if asset_folder not in assets_list:
            asset_folder.mkdir()
        self.destination_path = asset_path

    def set_publish_status(self, status: PUBLISH_STATUS):
        self.status = AssetStatus(status)

    def set_install_status(self,status: INSTALL_STATUS):
        self.status = AssetStatus(status)

    def __str__(self):
        return f"{self.name}_v{self.version}"
    
@dataclass
class Gizmo(Asset):
    type:str = 'Gizmo'

@dataclass
class Script(Asset):
    type:str = 'Script'

ASSET_REGISTRY = {"Gizmo": Gizmo, "Script": Script}
ASSET_SUFFIXES = {".gizmo": Gizmo, ".nk": Script}



def asset_factory(asset_path:Path)->Gizmo|Script:
    #Force Path for stem and suffix methods
    if isinstance(asset_path, str):
        asset_path = Path(asset_path)

    # Get stem & suffix 
    asset_stem = asset_path.stem
    asset_suffix = asset_path.suffix

    # Check if naming matches with enforced versionning
    if "_v" in asset_stem:
        asset_name = asset_stem.split(sep='_v')[0]
        asset_version = Version(asset_stem.split(sep='_v')[1])
    else:
        # No specified version
        asset_name = asset_stem
        asset_version = Version('0.1.0') #assumes init version
        logger.warning(f'No specified version for {asset_name}')
        #to-do log no specified version


    cls = ASSET_SUFFIXES.get(asset_suffix) 
    if cls:
        return cls(asset_name, asset_path, asset_version)
    else: 
        raise TypeError(f'\nProvided path is not a supported asset type. \nPlease submit a file with this type {[str(k) for k in ASSET_SUFFIXES.keys()]} ')

    





