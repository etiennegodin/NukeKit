from __future__ import annotations
from pathlib import Path
from typing import Literal, List
import logging

path_types = Literal['str', 'Path']

logger = logging.getLogger(__name__)

class UserPaths:
    """All user paths."""

    BASE_DIR = Path.home() / ".nukekit"
    NUKE_DIR = Path.home() / ".nuke"
    NUKE_KIT_DIR = NUKE_DIR / "nukekit"
    STATE_FILE = BASE_DIR / "local_state.json"
    LOG_FILE = BASE_DIR / "nukekit.log"
    CACHED_MANIFEST = BASE_DIR / "cached_manifest.json"

    @classmethod
    def ensure(cls):
        """Create local dirs if thy don't exist. Called once"""
        cls.BASE_DIR.mkdir(exist_ok=True)
        cls.NUKE_KIT_DIR.mkdir(parents=True, exist_ok=True)

