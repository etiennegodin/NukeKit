from nukekit.core import Gizmo, Version



def test_create_gizmo():
    gizmo_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
    version = Version('1.1.0')
    assert Gizmo('my_gizmo',gizmo_path, version, 'change', author= 'eti')



