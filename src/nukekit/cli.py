import os
import argparse
from pathlib import Path

from dotenv import load_dotenv

from .core.context import Context
from .core.repository import Repository
from .core.publisher import Publisher
from .core.installer import Installer

from nukekit import ui 
from .utils._logger import init_logger
from .utils.config import ConfigLoader
from .utils.paths import UserPaths
from .utils.scanner import Scanner
from .utils.console import print_manifest, choose_menu


ROOT_FOLDER = Path(os.getcwd())
LOG_PATH = f'{ROOT_FOLDER}/nukekit.log'

def get_context()->Context:
    """
    Initialize context for this session
    
    :return: Context instance for current session
    :rtype: Context
    """

    # Load .env 
    load_dotenv()

    #Setup user paths 
    USER_PATHS = UserPaths()

    # Init logger
    logger = init_logger(USER_PATHS.LOG_FILE)

    # Config solver
    CONFIG = ConfigLoader().load()

    # Init Central Repo
    REPO = Repository(CONFIG['repository'])
    
    # Create and return context instance
    return Context(REPO,
                USER_PATHS,
                CONFIG,
                )

def publish(args, context:Context):
    """
    Publish a local asset to remote repository 
    
    :param context: This sessions's context
    :type context: Context
    """

    publisher = Publisher(context)
    if args.directory is not None:
        scanner = Scanner()
        data = scanner.scan_folder(args.directory)
    else:
        data = context.local_state.data

    #Print visual cue for explorer 
    print_manifest(data)
    
    asset = choose_menu(data)

    if asset is not None:
        publisher.publish_asset(asset)
    else: 
        print('Asset publish aborted')     
    

def install(args, context:Context):
    """
    Install a remote asset to local nuke directory 
    
    :param context: This sessions's context
    :type context: Context
    """

    installer = Installer(context)
    print_manifest(context.repo_manifest.data)
    asset = choose_menu(context.repo_manifest.data)
    if asset is not None:
        installer.install_asset(asset)

def scan(args, context:Context):
    """
    Scan nuke directory and print available assets to console  
    
    :param context: This sessions's context
    :type context: Context
    """  

    scanner = Scanner(context)
    assets = scanner.scan_local(verbose = True)
    print_manifest(assets)


def main():

    parser = argparse.ArgumentParser(prog='NukeKit',
                    description='--- Nuke Gizmo and Script manager ---')
    
    parser.add_argument("--force", action = 'store_true', help = "Wipe Local State Clean")
    parser.add_argument("--no-gui", action = 'store_true', help = "Launch without gui")

    subparsers = parser.add_subparsers(help='Available subcommands')

    # Create the parser for the "publish" command
    parser_publish = subparsers.add_parser('publish', help='Record changes to the repository')
    parser_publish.add_argument("--directory", "--d", help = "From this directory" )

    parser_publish.set_defaults(func=publish) # Associate a function

    # Create the parser for the "install" command
    parser_install = subparsers.add_parser('install', help='Push changes to a remote repository')
    parser_install.set_defaults(func=install) # Associate a function

    # Create the parser for the "scan" command
    parser_scan = subparsers.add_parser('scan', help='Push changes to a remote repository')
    #parser_scan.add_argument("--directory", "-dir", help = "Folder to scan" )
    parser_scan.set_defaults(func=scan) # Associate a function

    args = parser.parse_args()

    context = get_context()

    # Call the function associated with the subcommand
    if hasattr(args, 'func'):
        # Dev force clean state 
        if args.force:
            UserPaths.clean()
        # Create context 
        args.func(args, context)
    else:
        ui.launch(context)

if __name__ == '__main__':
    main()