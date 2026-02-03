from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, TypeAlias
import logging 
from ..core.repo import CentralRepo
from ..utils.paths import UserPaths 

logger = logging.getLogger(__name__)

@dataclass
class Context():
    repo: CentralRepo
    user_paths: UserPaths
    config: Dict[str, Any ]
    date: str
    repo_manifest: Dict[str, Any] = field(default_factory=dict)
    local_manifest: Dict[str, Any] = field(default_factory=dict)
    asset_types: TypeAlias = Literal['gizmo', 'script']
