from ..core import Context, scan_folder
from ..core.console import print_data


def scan(args, context: Context):
    """
    Scan nuke directory and print available assets to console

    :param context: This sessions"s context
    :type context: Context
    """
    context.set_mode("scan")
    if args.location == "local":
        assets = context.local_state.data
    elif args.location == "remote":
        assets = scan_folder(context, context.repo.ROOT)
    print_data(assets)
