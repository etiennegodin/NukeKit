from __future__ import annotations
from .. import core
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class Gizmo():
    name:str 
    path:str
    version: core.Version
    changelog:str
    author: str = NotImplemented


