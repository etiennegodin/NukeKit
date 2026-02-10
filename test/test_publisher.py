import pytest
from pathlib import Path
import os
from nukekit.core.publisher import Publisher
from nukekit.core.assets import asset_factory
from nukekit.core.context import init_context
from nukekit.core.repository import Repository
from nukekit.utils.logger import setuplogger
from nukekit.core.config import ConfigLoader
from nukekit.utils.paths import UserPaths


def test_publisher_script():
    pass

def test_publisher_gizmo():
    pass


def test_publisher_none_type():
 #Setup user paths 
    USER_PATHS = UserPaths()
    USER_PATHS.ensure()

    # Init logger
    logger = setuplogger(USER_PATHS.LOG_FILE)

    # Config solver
    CONFIG = ConfigLoader().load()

    # Init Central Repo
    REPO = Repository(CONFIG['repository'])

    # Setup Context dataclass
    CONTEXT = init_context(REPO, CONFIG, USER_PATHS)
    pub = Publisher()
    asset = None
    with pytest.raises(TypeError): # Catches any Exception type
        pub.publish_asset(asset)




