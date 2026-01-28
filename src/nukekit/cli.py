from nukekit.utils import create_central_repo 
from .core.publisher import Publisher
from .core.versioning import Version
from .core.assets import Gizmo
from .core.context import set_context
from pathlib import Path
import os 
from pprint import pprint

ROOT_FOLDER = Path(os.getcwd())
gizmo_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
version = Version('1.1.0')

def main():
    context = set_context(ROOT_FOLDER)
    pprint(context)
    create_central_repo(context)
    pub = Publisher(context)

    gizmo = Gizmo('my_gizmo',gizmo_path, version, 'change', author= 'eti')

    pub.publish_gizmo(gizmo)