import argparse
import os
from pathlib import Path

from .app import Dependencies
from .utils import ConfigLoader
from .workflows import install, publish_workflow, scan

ROOT_FOLDER = Path(os.getcwd())
LOG_PATH = ROOT_FOLDER / "nukekit.log"


def main():
    # Setup parsers and arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--force", action="store_true", help="Wipe Local State Clean"
    )
    parent_parser.add_argument(
        "--no-gui", action="store_true", help="Launch without gui"
    )

    parser = argparse.ArgumentParser(
        prog="NukeKit", description="--- Nuke Gizmo and Script manager ---"
    )

    subparsers = parser.add_subparsers(help="Available subcommands")

    # Publish
    parser_publish = subparsers.add_parser(
        "publish", parents=[parent_parser], help="Record changes to the repository"
    )
    parser_publish.add_argument(
        "--local", "-l", action="store_true", help="Publish from this directory"
    )
    parser_publish.set_defaults(func=publish_workflow)  # Associate a function

    # Install
    parser_install = subparsers.add_parser(
        "install", parents=[parent_parser], help="Install asset to nuke directory"
    )
    parser_install.set_defaults(func=install)  # Associate a function

    # Scan
    parser_scan = subparsers.add_parser(
        "scan", parents=[parent_parser], help="Scan directory for assets"
    )
    # parser_scan.add_argument("location", choices=scan_choices, help="Where to scan")
    parser_scan.set_defaults(func=scan)  # Associate a function

    args = parser.parse_args()

    config = ConfigLoader()

    deps = Dependencies.create(config)

    # Call the function associated with the subcommand
    if hasattr(args, "func"):
        args.func(args, deps)
    else:
        pass
        # context.set_mode("publish")
        # ui.launch(context)


if __name__ == "__main__":
    main()
