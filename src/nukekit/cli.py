"""
CLI entry point.

Thin layer that:
- Parses arguments
- Creates dependencies
- Calls application service
- Handles presentation (output formatting)
"""

import argparse
import logging
import sys

from rich.console import Console
from rich.panel import Panel

from .app.container import Dependencies
from .app.service import ApplicationService
from .core.exceptions import (
    ConfigurationError,
    NukeKitError,
    UserAbortedError,
)
from .utils import ConfigLoader, init_logger

console = Console()


def main():
    parser = create_parser()
    args = parser.parse_args()

    # Setup logging
    logger = init_logger(level=logging.DEBUG if args.verbose else logging.INFO)

    try:
        # Load configuration
        try:
            config = ConfigLoader().load()
        except Exception as e:
            console.print(f"[red]Failed to load configuration: {e}[/red]")
            sys.exit(1)

        # Create dependencies
        try:
            deps = Dependencies.create(config, logger=logger)
        except ConfigurationError as e:
            console.print(f"[red]Configuration error: {e}[/red]")
            sys.exit(1)

        # Create application service
        app = ApplicationService(deps)

        # Execute command
        if hasattr(args, "func"):
            exit_code = args.func(args, app)
            sys.exit(exit_code)
        else:
            parser.print_help()
            sys.exit(0)

    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(130)
    except Exception as e:
        logger.exception("Unexpected error")
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="nukekit", description="Nuke asset management system"
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    subparsers = parser.add_subparsers(
        title="commands", description="Available commands"
    )

    # Publish command
    publish_parser = subparsers.add_parser(
        "publish", help="Publish assets to repository"
    )
    publish_parser.add_argument(
        "--local",
        "-l",
        action="store_true",
        help="Scan current directory instead of Nuke directory",
    )
    publish_parser.set_defaults(func=cmd_publish)

    # Install command
    install_parser = subparsers.add_parser(
        "install", help="Install assets from repository"
    )
    install_parser.add_argument("--asset", "-a", help="Specific asset to install")
    install_parser.add_argument("--version", "-ver", help="Specific version to install")
    install_parser.set_defaults(func=cmd_install)

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan for assets")
    scan_parser.add_argument(
        "location",
        choices=["local", "remote"],
        default="local",
        nargs="?",
        help="Where to scan (default: local)",
    )
    scan_parser.set_defaults(func=cmd_scan)

    return parser


def cmd_publish(args, app: ApplicationService) -> int:
    """Handle publish command."""
    try:
        result = app.publish_asset(scan_local=args.local, interactive=True)

        console.print(
            Panel(
                f"[green]✓[/green] {result['message']}",
                title="Success",
                border_style="green",
            )
        )
        return 0

    except UserAbortedError:
        console.print("[yellow]Publish cancelled[/yellow]")
        return 0

    except NukeKitError as e:
        console.print(f"[red]✗ {e}[/red]")
        return 1


def cmd_install(args, app: ApplicationService) -> int:
    """Handle install command."""
    try:
        result = app.install_asset(
            asset_name=args.asset, version=args.version, interactive=True
        )

        console.print(
            Panel(
                f"[green]✓[/green] {result['message']}",
                title="Success",
                border_style="green",
            )
        )
        return 0

    except UserAbortedError:
        console.print("[yellow]Install cancelled[/yellow]")
        return 0

    except NukeKitError as e:
        console.print(f"[red]✗ {e}[/red]")
        return 1


def cmd_scan(args, app: ApplicationService) -> int:
    """Handle scan command."""
    try:
        result = app.scan_assets(location=args.location)

        console.print(f"[green]Found {result['count']} assets[/green]")

        # Pretty print assets
        from rich.table import Table

        table = Table(title=f"Assets ({args.location})")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Versions", style="green")

        for asset_type, assets in result["assets"].items():
            for name, versions in assets.items():
                table.add_row(
                    name, asset_type, ", ".join(str(v) for v in versions.keys())
                )

        console.print(table)
        return 0

    except NukeKitError as e:
        console.print(f"[red]✗ {e}[/red]")
        return 1


if __name__ == "__main__":
    main()
