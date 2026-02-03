import argparse
import os 
from pathlib import Path
from dotenv import load_dotenv

from .utils.paths import CentralRepo, UserPaths
from .utils.logger import setup_logger
from .utils.config import ConfigLoader

from .core.publisher import Publisher
from .core.versioning import Version
from .core.assets import asset_factory
from .core.context import init_context

ROOT_FOLDER = Path(os.getcwd())
LOG_PATH = f'{ROOT_FOLDER}/nukekit.log'


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

    # Load .env 
    load_dotenv()

    #Setup user paths 
    USER_PATHS = UserPaths()
    USER_PATHS.ensure()

    # Init logger
    logger = setup_logger(USER_PATHS.LOG_FILE)

    # Config solver
    CONFIG = ConfigLoader().load()

    # Init Central Repo
    REPO = CentralRepo(CONFIG['repository'])

    # Setup Context dataclass
    CONTEXT = init_context(REPO, CONFIG, USER_PATHS)

    if args.action == 'publish':
        if args.file is None:
            #scanner
            dev_path = '/home/etienne/projects/pipetd/NukeKit/examples/my_gizmo_v1.2.4.gizmo'
            asset_path = Path(dev_path)
            #raise FileExistsError('Please provide a file to publish')
        else:
            asset_path = Path(args.file)

        #Create asset 
        asset = asset_factory(asset_path)
        
        #Init publisher
        pub = Publisher()

        pub.publish_asset(asset, CONTEXT.repo)


        



if __name__ == '__main__':
    main()