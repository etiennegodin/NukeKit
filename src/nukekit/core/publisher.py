# Copy 
gizmo_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
from ..utils import Context
from pathlib import Path


def copy():
    pass
# Update manifest

def metadata():
    pass


def main(context:Context):
    gizmo = Path(gizmo_path)
    context.logger.info(gizmo)
    print(gizmo)
    pass