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
from .core.assets import AssetStatus

from .utils.logger import setup_logger
from .utils.config import ConfigLoader
from .utils.paths import UserPaths
from .utils.scanner import Scanner
from .utils.console import print_manifest, choose_menu


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
    #LOCAL_STATE = Manifest.from_scanner(USER_PATHS)
    
    try:
        context = Context(REPO,
                USER_PATHS,
                CONFIG,
                str(date.today()),
                REPO_MANIFEST,
                LOCAL_MANIFEST,
                )
    except Exception as e:
        raise e 
    else:
        return context

def publish(args, context:Context):
    publisher = Publisher(context)
    if args.file:
        context = publisher.publish_asset(args.file)
    else:
        #pprint(context.local_state.data)
        print_manifest(context.local_state.data)
        asset = choose_menu(context.local_state.data)
        publisher.publish_asset(asset)        
        pass

def install(args, context:Context):
    installer = Installer(context)
    installer.install_from_repo()

def scan(args, context:Context):
    scanner = Scanner(context.user_paths)
    if args.directory is not None:
        assets = scanner.scan_folder(args.directory)
    else:
        assets = scanner.scan_local(verbose = True)
def main():

    parser = argparse.ArgumentParser(prog='NukeKit',
                    description='--- Nuke Gizmo and Script manager ---')
    
    parser.add_argument("--force", action = 'store_true', help = "Wipe Local State Clean")
    parser.add_argument("--no-gui", action = 'store_true', help = "Launch without gui")

    subparsers = parser.add_subparsers(help='Available subcommands')

    parser_publish = subparsers.add_parser('publish', help='Record changes to the repository')
    #parser_publish.add_argument('message', type=str, help='A commit message')
    parser_publish.add_argument("--file", "-f", help = "File to publish" )
    parser_publish.set_defaults(func=publish) # Associate a function

    # Create the parser for the "push" command
    parser_install = subparsers.add_parser('install', help='Push changes to a remote repository')
    #parser_install.add_argument('remote', type=str, help='The remote repository name')
    parser_install.set_defaults(func=install) # Associate a function

    # Create the parser for the "sync" command
    parser_scan = subparsers.add_parser('scan', help='Push changes to a remote repository')
    parser_scan.add_argument("--directory", "-dir", help = "Folder to scan" )

    #parser_scan.add_argument('remote', type=str, help='The remote repository name')
    parser_scan.set_defaults(func=scan) # Associate a function


    args = parser.parse_args()
    context = init()

    # Call the function associated with the subcommand
    if hasattr(args, 'func'):
        # Dev force clean state 
        if args.force:
            UserPaths.clean()
        # Create context 
        args.func(args, context)
    else:
        # If no subcommand is given, show help
        parser.print_help()

    """
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

    """

    #ui.launchUi(context)

if __name__ == '__main__':
    main()