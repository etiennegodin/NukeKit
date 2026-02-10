import os
import argparse
from pathlib import Path

from dotenv import load_dotenv

from .core.context import Context
from .core.repository import Repository
from .core.publisher import Publisher
from .core.installer import Installer

from nukekit import ui 
from .utils.logger import initlogger
from .utils.config import ConfigLoader
from .utils.paths import UserPaths
from .utils.scanner import Scanner
from .utils.console import print_data, choose_menu


ROOT_FOLDER = Path(os.getcwd())
LOG_PATH = ROOT_FOLDER / "nukekit.log"

def get_context() -> Context:
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
    logger = initlogger(USER_PATHS.LOG_FILE)

    # Config solver
    CONFIG = ConfigLoader().load()

    # Init Central Repo
    REPO = Repository(CONFIG["repository"])
    
    # Create and return context instance
    return Context(REPO,
                USER_PATHS,
                CONFIG,
                )

def publish(args, context:Context):
    """
    Publish a local asset to remote repository 
    
    :param context: This sessions"s context
    :type context: Context
    """
    context.set_mode("publish")
    publisher = Publisher(context)

    if args.local:
        scanner = Scanner(context)
        data = scanner.scan_folder(Path.cwd())
    else:
        data = context.get_current_data()

    #Print visual cue for explorer 
    print_data(data)

    asset = choose_menu(data)

    if asset is not None:
        publisher.publish_asset(asset)
    else: 
        print("Asset publish aborted")      

def install(args, context:Context):
    """
    Install a remote asset to local nuke directory 
    
    :param context: This sessions"s context
    :type context: Context
    """

    context.set_mode("install")
    data = context.get_current_data()
    installer = Installer(context)

    print_data(data)
    asset = choose_menu(data)
    if asset is not None:
        installer.install_asset(asset)

def scan(args, context:Context):
    """
    Scan nuke directory and print available assets to console  
    
    :param context: This sessions"s context
    :type context: Context
    """  
    context.set_mode("scan")
    scanner = Scanner(context)
    if args.location == "local":
        assets = context.local_state.data
    elif args.location == "remote":
        assets = scanner.scan_folder(context.repo.ROOT)
    print_data(assets)

def main():

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--force", action = "store_true", help = "Wipe Local State Clean")
    parent_parser.add_argument("--no-gui", action = "store_true", help = "Launch without gui")

    parser = argparse.ArgumentParser(prog="NukeKit",
                    description="--- Nuke Gizmo and Script manager ---")
    

    subparsers = parser.add_subparsers(help="Available subcommands")

    # Create the parser for the "publish" command
    parser_publish = subparsers.add_parser("publish", parents=[parent_parser], help="Record changes to the repository")
    parser_publish.add_argument("--local", "-l", action= "store_true", help = "Publish from this directory" )

    parser_publish.set_defaults(func=publish) # Associate a function

    # Create the parser for the "install" command
    parser_install = subparsers.add_parser("install", parents=[parent_parser], help="Install asset to nuke directory")
    parser_install.set_defaults(func=install) # Associate a function

    # Create the parser for the "scan" command
    scan_choices = ["local", "remote"]
    parser_scan = subparsers.add_parser("scan", parents=[parent_parser], help="Scan directory for assets")
    parser_scan.add_argument("location", choices= scan_choices, help = "Where to scan" )

    #parser_scan.add_argument("--directory", "-dir", help = "Folder to scan" )
    parser_scan.set_defaults(func=scan) # Associate a function

    args = parser.parse_args()

    context = get_context()

    # Call the function associated with the subcommand
    if hasattr(args, "func"):
        # Dev force clean state 
        if args.force:
            UserPaths.clean()
        # Create context 
        args.func(args, context)
    else:
        context.set_mode("publish")
        ui.launch(context)

if __name__ == "__main__":
    main()