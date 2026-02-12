from ..core import Context, install_asset
from ..core.console import choose_menu, print_data


def install(args, context: Context):
    """
    Install a remote asset to local nuke directory

    :param context: This sessions"s context
    :type context: Context
    """

    context.set_mode("install")
    data = context.get_current_data()

    print_data(data)
    asset = choose_menu(data)
    if asset is not None:
        install_asset(context, asset)
