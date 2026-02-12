from ..core import Context, Scanner
from ..core.console import print_data


def scan(args, context: Context):
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
