from __future__ import annotations
from .versioning import Version
from typing import Optional
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Asset():
    name:str 
    source_path:str
    version: Version = NotImplemented
    changelog:str = NotImplemented
    author: str = NotImplemented
    destination_path: Path = NotImplemented
    time:str = str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))

    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.source_path, str):
            self.source_path  = Path(self.source_path)



@dataclass
class Gizmo(Asset):
    type:str = 'Gizmo'

@dataclass
class Script(Asset):
    type:str = 'Script'


ASSET_REGISTRY = {"Gizmo": Gizmo, "Script": Script, "Asset": Asset}
ASSET_SUFFIXES = {".gizmo": Gizmo, ".nk": Script}

def asset_factory(asset_path:Path):
    if isinstance(asset_path, str):
        asset_path = Path(asset_path)
    asset_name = asset_path.stem
    asset_suffix = asset_path.suffix
    #check if version s in naming
    #to-do

    if asset_suffix in ASSET_SUFFIXES:
        cls = ASSET_SUFFIXES.get(asset_suffix) 
        if cls:
            return cls(asset_name, asset_path)
    else: 
        raise TypeError('Provided path is not a supported asset [.gizmo, .nk] ')

    





