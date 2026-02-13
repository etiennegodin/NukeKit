from ..core import (
    Asset,
    EnvContext,
    Manifest,
    Repository,
    console,
    installer,
)


def install(args, env: EnvContext):
    """
    Install a remote asset to local nuke directory

    :param context: This sessions"s context
    :type context: EnvContext
    """

    repo = Repository(env.config)
    repo.add_manifest(Manifest.from_json(repo.MANIFEST_PATH))
    local_manifest = Manifest.from_json(env.user_paths.CACHED_MANIFEST)

    asset = console.choose_menu(repo.manifest.data)

    if asset is None:
        installer.logger.info("Asset install aborted.")
        quit()
    elif not isinstance(asset, Asset):
        raise TypeError(f"Provided asset is not of type {Asset}")

    installer.install_asset_from_repo(env, repo, local_manifest, asset)
