from pathlib import Path

from ..core import (
    Asset,
    EnvContext,
    Manifest,
    ManifestStore,
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
    # 1. Setup repository (directory structure)
    repo = Repository.from_config(env.config)

    # 2. Load manifests (persistence layer)
    repo_manifest = ManifestStore.load_from_json(repo.manifest_path)
    cached_manifest = ManifestStore.load_from_json(env.user_paths.CACHED_MANIFEST)

    # 3. Scan local state (if not using --local flag)
    if args.local:
        data = scanner.scan_folder(Path.cwd())
        local_state = Manifest.from_dict(data)
    else:
        local_state = ManifestStore.load_from_filesystem(
            env.user_paths.NUKE_DIR, cached_manifest=cached_manifest
        )

    # 4. User chooses asset
    console.print_data(local_state)
    asset = console.choose_menu(local_state)

    if asset is None:
        publisher.logger.info("Asset publish aborted.")
        quit()
    elif not isinstance(asset, Asset):
        raise TypeError(f"Provided asset is not of type {Asset}")

    # 5. Resolve version
    asset = publisher.resolve_version(repo.manifest, asset)

    # 6. Ensure metadata
    asset.ensure_metadata()

    # 7. Publish to repository
    destination_path = repo.get_asset_path(asset)
    publisher.publish_asset_to_repo(asset.source_path, destination_path)

    # 8. Upate asset status
    asset.set_publish_status("published")

    # 9. Update manifest and save
    repo_manifest.add_asset(asset)
    ManifestStore.save_to_json(repo_manifest, repo.manifest_path)

    # 10. Install locally and update local manifest
    installer.install_asset_from_repo(env, repo, asset)
    cached_manifest.add_asset(asset)
    ManifestStore.save_to_json(cached_manifest, env.user_paths.CACHED_MANIFEST)
