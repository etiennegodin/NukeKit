import pytest
from pathlib import Path
import os
from nukekit.core.publisher import Publisher
from nukekit.core.versioning import Version
from nukekit.core.assets import asset_factory
from nukekit.core.context import init_context


def test_publisher_script():
    pass

def test_publisher_gizmo():
    pass


def test_publisher_none_type():
    ROOT_FOLDER = Path(os.getcwd())
    context = init_context(ROOT_FOLDER)
    pub = Publisher(context)
    asset = None
    with pytest.raises(TypeError): # Catches any Exception type
        pub.publish_asset(asset)




