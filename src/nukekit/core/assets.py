from __future__ import annotations
from .. import core
from .context import Context
from typing import Optional
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Asset():
    name:str 
    source_path:str
    version: core.Version
    changelog:str
    author: str = NotImplemented
    destination_path: Path = NotImplemented

    def __post_init__(self):
        #Convert to path if string
        if isinstance(self.source_path, str):
            self.source_path  = Path(self.source_path)




@dataclass
class Gizmo(Asset):
    type:str = 'gizmo'

@dataclass
class Scripts(Asset):
    type:str = 'scripts'




