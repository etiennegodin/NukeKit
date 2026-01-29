from __future__ import annotations
from .versioning import Version
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from pprint import pprint

@dataclass
class Asset():
    name:str 
    source_path:str
    version: Version = None
    changelog:str = None
    author: str = None
    destination_path: Path = None
    time:str = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
    type:str = 'Asset'

    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.source_path, str):
            self.source_path  = Path(self.source_path)

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

def asset_factory(asset_path:Path):
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
        #to-do log no specified version

    cls = ASSET_SUFFIXES.get(asset_suffix) 
    if cls:
        return cls(asset_name, asset_path, asset_version)
    else: 
        raise TypeError(f'\nProvided path is not a supported asset type. \nPlease submit a file with this type {[str(k) for k in ASSET_SUFFIXES.keys()]} ')

    





