from nukekit.utils import set_context, create_central_repo 
from .core import publisher, Version
from pathlib import Path
import os 

ROOT_FOLDER = Path(os.getcwd())
gizmo_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
version = Version('1.1.0')

def main():
    context = set_context(ROOT_FOLDER)
    create_central_repo(context)
    publisher.publish_gizmo(context,gizmo_path,version, 'change',author= 'eti')