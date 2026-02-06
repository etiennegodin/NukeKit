import argparse
import os 
import sys 
from pprint import pprint
from pathlib import Path
from dotenv import load_dotenv
from datetime import date

from .core.manifest import Manifest
from .core.context import Context
from .core.repository import Repository
from .core.publisher import Publisher
from .core.assets import asset_factory

from .utils.logger import setup_logger
from .utils.config import ConfigLoader
from .utils.paths import UserPaths
from .utils.scanner import Scanner

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
    REPO = Repository(CONFIG['repository'])

    #Read remote and local manifest
    REPO_MANIFEST = Manifest(REPO.MANIFEST)
    LOCAL_MANIFEST = Manifest(UserPaths.STATE_FILE)

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
    actions = ["publish", "scan", "sync"]
    global_parser = argparse.ArgumentParser(add_help = False)
    global_parser.add_argument("action", nargs='?', default = None,choices= actions,help = 'Actions to take')
    global_parser.add_argument("--file", "-f", help = "File" )
    global_parser.add_argument("--directory", "-dir", help = "Folder to scan" )
    global_parser.add_argument("--no-gui", action = 'store_true', help = "Launch without gui")

    parser = argparse.ArgumentParser(
                    prog='NukeKit',
                    description='--- Nuke Gizmo and Script manager ---',
                    epilog='Text at the bottom of help',
                    parents=[global_parser]
    )
    args = parser.parse_args()

    # Create context 
    context = init()
    
    # Scan for local files and update local manifest


    pprint(context.local_manifest.data)
    print("*"*100)
    pprint(context.repo_manifest.data)


    # Ui 
    if args.no_gui:
        if args.action is None:
            print('Please chose an action in non gui mode')
        if args.action == 'publish':
            #scanner
            #choose asset
            asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/city.gizmo"
            asset = asset_factory(asset_path)
            publisher = Publisher(context)
            context = publisher.publish_asset(asset)
        elif args.action == 'scan':
            scanner = Scanner(context)
            if args.directory is not None:
                assets = scanner.scan_folder(args.directory)
            else:
                assets = scanner.scan_local()
            #pprint(assets)

    else:
        ui.launchUi(context)







    #Create asset 
    
    #Init publisher
    #pub = Publisher()

    #pub.publish_asset(asset, CONTEXT.repo)


        



if __name__ == '__main__':
    main()