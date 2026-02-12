from pathlib import Path

from ..core import Context, Publisher, Scanner
from ..core.console import choose_menu, print_data


def publish(args, context: Context):
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

    # Print visual cue for explorer
    print_data(data)

    asset = choose_menu(data)

    if asset is not None:
        publisher.publish_asset(asset)
    else:
        context.logger.info("Asset publish aborted")
