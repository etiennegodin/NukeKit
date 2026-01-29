import argparse
import os 
from pathlib import Path

from .utils.paths import init_central_repo
from .utils.logger import setup_logger
from .core.publisher import Publisher
from .core.versioning import Version
from .core.assets import asset_factory
from .core.context import init_context

ROOT_FOLDER = Path(os.getcwd())

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
    context = init_context(ROOT_FOLDER)
    central_repo = init_central_repo(context)
    logger = setup_logger(context.log_file)

    if args.action == 'publish':
        if args.file is None:
            #scanner
            #debug_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo_v1.2.4.gizmo'
            #asset_path = Path(debug_path)
            raise FileExistsError('Please provide a file to publish')
        else:
            asset_path = Path(args.file)

        #Create asset 
        asset = asset_factory(asset_path)
        
        #Init publisher
        pub = Publisher(context)

        pub.publish_asset(asset)


        



if __name__ == '__main__':
    main()