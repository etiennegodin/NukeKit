from ..core import Context, Installer
from ..core.console import choose_menu, print_data


def install(args, context: Context):
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
