from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from .repository import Repository
from ..core.manifest import Manifest
from ..utils.paths import UserPaths 

logger = logging.getLogger(__name__)

@dataclass
class Context():
    repo: Repository
    user_paths: UserPaths
    config: Dict[str, Any ]
    date: str
    repo_manifest: Manifest
    local_manifest: Manifest
    asset_types: TypeAlias = Literal['Gizmo', 'Script']

    def compare_to_remote(self):
        self.local_manifest.compare(self.repo_manifest)
