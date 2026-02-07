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
from .core.installer import Installer

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
    REPO_MANIFEST = Manifest.from_file(REPO.MANIFEST)
    LOCAL_MANIFEST = Manifest.from_file(USER_PATHS.CACHED_MANIFEST)

    LOCAL_STATE = Manifest.from_scanner(USER_PATHS)
    
    try:
        context = Context(REPO,
                USER_PATHS,
                CONFIG,
                str(date.today()),
                REPO_MANIFEST,
                LOCAL_MANIFEST,
                LOCAL_STATE
                )
    except Exception as e:
        raise e 
    else:
        return context

def main():
    actions = ["publish", 'install', "scan"]
    global_parser = argparse.ArgumentParser(add_help = False)
    global_parser.add_argument("action", nargs='?', default = None,choices= actions,help = 'Actions to take')
    global_parser.add_argument("--file", "-f", help = "File" )
    global_parser.add_argument("--directory", "-dir", help = "Folder to scan" )
    global_parser.add_argument("--no-gui", action = 'store_true', help = "Launch without gui")
    global_parser.add_argument("--force", action = 'store_true', help = "Launch without gui")

    parser = argparse.ArgumentParser(
                    prog='NukeKit',
                    description='--- Nuke Gizmo and Script manager ---',
                    epilog='Text at the bottom of help',
                    parents=[global_parser]
    )
    args = parser.parse_args()        

    # Dev force clean state 
    if args.force:
        UserPaths.clean()

    # Create context 
    context = init()
    
    # Scan for local files and update local manifest

    print('local_manifest')
    pprint(context.local_manifest.data)
    print("*"*100)
    print('local_state')
    pprint(context.local_state.data)
    print("*"*100)
    print('remote')
    pprint(context.repo_manifest.data)

    publish_asset_path = "/home/etienne/projects/pipetd/NukeKit/examples/city.gizmo"
    install_asset_path = "/home/etienne/central_repo/Gizmo/city/city_v0.1.0.gizmo"


    # Ui 
    if args.no_gui:
        if args.action is None:
            print('Please chose an action in non gui mode')
        if args.action == 'publish':
            #scanner
            #choose asset
            publisher = Publisher(context)
            context = publisher.publish_asset(publish_asset_path)
        elif args.action == 'install':
            installer = Installer(context)
            installer.install_asset(install_asset_path)

        elif args.action == 'scan':
            scanner = Scanner(context)
            if args.directory is not None:
                assets = scanner.scan_folder(args.directory)
            else:
                assets = scanner.scan_local()
            #pprint(assets)

    else:
        pass
        #ui.launchUi(context)







    #Create asset 
    
    #Init publisher
    #pub = Publisher()

    #pub.publish_asset(asset, CONTEXT.repo)


        



if __name__ == '__main__':
    main()