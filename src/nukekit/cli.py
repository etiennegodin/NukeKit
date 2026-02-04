import argparse
import os 
import sys 
from pprint import pprint
from pathlib import Path
from dotenv import load_dotenv
from datetime import date


from .utils.logger import setup_logger
from .utils.config import ConfigLoader
from .utils.paths import UserPaths

from .core.manifest import Manifest
from .core.context import Context, AppContext
from .core.repo import CentralRepo
from .core.publisher import Publisher
from .core.assets import asset_factory

from . import ui

ROOT_FOLDER = Path(os.getcwd())
LOG_PATH = f'{ROOT_FOLDER}/nukekit.log'

def init()->Context:

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


    
    #Read remote and local manifest
    REPO_MANIFEST = Manifest(REPO.MANIFEST).read_manifest()
    LOCAL_MANIFEST = Manifest(UserPaths.STATE_FILE).read_manifest()

    try:
        context = Context(REPO,
                USER_PATHS,
                CONFIG,
                str(date.today()),
                REPO_MANIFEST,
                LOCAL_MANIFEST
                )
    except Exception as e:
        raise e 
    else:
        return context

def main():
    actions = ['publish']
    global_parser = argparse.ArgumentParser(add_help = False)
    global_parser.add_argument("-action", choices= actions,help = 'Actions to take')
    #global_parser.add_argument("--file", "-f", help = "File" )
    global_parser.add_argument("--no-gui", action = 'store_true', help = "Launch without GUi")
    global_parser.add_argument("--force", action= 'store_true', help = "Ignore last checkpoint")

    parser = argparse.ArgumentParser(
                    prog='NukeKit',
                    description='--- Nuke Gizmo and Script manager ---',
                    epilog='Text at the bottom of help',
                    parents=[global_parser]
    )
    args = parser.parse_args()

    context = init()
    #pprint(context)
    test = AppContext(context.repo_manifest)
    # Ui 
    if args.no_gui:
        if args.action is None:
            print('Please chose an action in non gui mode')
        if args.action == 'publish':
            print('publish ') 
        pass
    else:
        ui.launchUi(context)







    #Create asset 
    #asset = asset_factory(asset_path)
    
    #Init publisher
    #pub = Publisher()

    #pub.publish_asset(asset, CONTEXT.repo)


        



if __name__ == '__main__':
    main()