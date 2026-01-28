from nukekit.core import Gizmo, Version, Publisher

gizmo_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
version = Version('1.1.0')
gizmo = Gizmo('my_gizmo',gizmo_path, version, 'change', author= 'eti')

