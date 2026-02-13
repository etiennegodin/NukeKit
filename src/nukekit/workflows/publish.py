from pathlib import Path

from ..core import (
    Asset,
    EnvContext,
    Manifest,
    Repository,
    console,
    installer,
    publisher,
    scanner,
)


def publish(args, env: EnvContext):
    """_summary_

    Args:
        args (_type_): _description_
        context (EnvContext): _description_
    """

    repo = Repository(env.config)
    repo.add_manifest(Manifest.from_json(repo.MANIFEST_PATH))
    local_manifest = Manifest.from_json(env.user_paths.CACHED_MANIFEST)
    local_state_manifest = Manifest.from_local_state(env.user_paths, local_manifest)

    if args.local:
        data = scanner.scan_folder(Path.cwd())
    else:
        data = local_state_manifest.data

    # Print visual cue for menu
    console.print_data(data)

    # Choose asset from terminal menu
    asset = console.choose_menu(data)

    if asset is None:
        publisher.logger.info("Asset publish aborted.")
        quit()
    elif not isinstance(asset, Asset):
        raise TypeError(f"Provided asset is not of type {Asset}")

    # Resolve asset version conflicts
    asset = publisher.resolve_version(repo.manifest, asset)

    # Ensures message
    asset.ensure_message()

    # Ensures metadata
    asset.ensure_metadata()

    # Publish asset and add repo
    if publisher.publish_asset_to_repo(repo, asset):
        installer.install_asset_from_repo(env, repo, local_manifest, asset)
