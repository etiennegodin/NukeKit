import argparse
import os 
from pathlib import Path

from nukekit.utils import create_central_repo 
from .core.publisher import Publisher
from .core.versioning import Version
from .core.assets import Gizmo, Script
from .core.context import set_context

ROOT_FOLDER = Path(os.getcwd())
version = Version('1.1.0')

def main():




    actions = ['publish','load']
    global_parser = argparse.ArgumentParser(add_help = False)
    global_parser.add_argument("action", choices= actions,help = 'Actions to take')
    global_parser.add_argument("--file", "-f", help = "File" )
    global_parser.add_argument("--force", action= 'store_true', help = "Ignore last checkpoint")

    parser = argparse.ArgumentParser(
                    prog='NukeKit',
                    description='--- Nuke Gizmo and Script manager ---',
                    epilog='Text at the bottom of help',
                    parents=[global_parser]
    )
    args = parser.parse_args()


    context = set_context(ROOT_FOLDER)
    create_central_repo(context)

    if args.action == 'publish':
        if args.file is None:
            #scanner
            debug_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo.gizmo'
            debug_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_script.nk'
            asset_path = Path(debug_path)
        else:
            asset_path = Path(args.file)

        #Init publisher
        pub = Publisher(context)
        if asset_path.suffix == '.gizmo':
            gizmo = Gizmo('my_gizmo',asset_path)
            pub.publish_gizmo(gizmo)
        elif asset_path.suffix == '.nk':
            script = Script('my_script', asset_path)
            pub.publish_script(script)


if __name__ == '__main__':
    main()