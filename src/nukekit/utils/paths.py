from __future__ import annotations
import shutil
import logging
from pathlib import Path
from typing import Literal

path_types = Literal['str', 'Path']

logger = logging.getLogger(__name__)

class UserPaths:
    """Class for all local user paths."""

    BASE_DIR = Path.home() / ".nukekit"
    NUKE_DIR = Path.home() / ".nuke"
    NUKE_KIT_DIR = NUKE_DIR / "nukekit"
    STATE_FILE = BASE_DIR / "local_state.json"
    LOG_FILE = BASE_DIR / "nukekit.log"
    CACHED_MANIFEST = BASE_DIR / "cached_manifest.json"

    def __init__(self):
        self.ensure()

    @classmethod
    def clean(cls):
        shutil.rmtree(cls.BASE_DIR,ignore_errors=True)
        shutil.rmtree(cls.NUKE_KIT_DIR,ignore_errors=True)
        shutil.rmtree(cls.STATE_FILE,ignore_errors=True)
        shutil.rmtree(cls.CACHED_MANIFEST,ignore_errors=True)
        logger.warning('Removed local files')

    @classmethod
    def ensure(cls):
        """Create local dirs if thy don't exist. Called once"""
        cls.BASE_DIR.mkdir(exist_ok=True)
        cls.NUKE_KIT_DIR.mkdir(parents=True, exist_ok=True)
    
