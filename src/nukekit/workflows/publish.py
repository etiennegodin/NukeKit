from pathlib import Path

from ..core import Context, Scanner, publish_asset
from ..core.console import choose_menu, print_data


def publish(args, context: Context):
    """_summary_

    Args:
        args (_type_): _description_
        context (Context): _description_
    """
    context.set_mode("publish")

    if args.local:
        scanner = Scanner(context)
        data = scanner.scan_folder(Path.cwd())
    else:
        data = context.get_current_data()

    # Print visual cue for explorer
    print_data(data)

    asset = choose_menu(data)

    if asset is not None:
        publish_asset(context, asset)
    else:
        context.logger.info("Asset publish aborted")
