from pathlib import Path

from ..core import (
    EnvContext,
    Manifest,
    ManifestStore,
    Repository,
    console,
    copy,
    scanner,
)
from ..core.validator import resolve_version


def publish(args, env: EnvContext):
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
    console.print_data(local_state.data)
    asset = console.choose_menu(local_state.data)

    # 5. Resolve version
    asset = resolve_version(repo_manifest.get_latest_asset_version(asset), asset)

    # 6. Ensure metadata
    asset.ensure_metadata()

    # 7. Publish to repository
    destination_path = repo.get_asset_path(asset)
    copy.copy_asset(asset.source_path, destination_path)

    # 8. Upate asset status
    asset.set_publish_status("published")

    # 9. Update manifest and save
    repo_manifest.add_asset(asset)
    ManifestStore.save_to_json(repo_manifest, repo.manifest_path)

    # 10. Install locally and update local manifest

    copy.copy_asset(
        repo.get_asset_path(asset), env.user_paths.NUKE_KIT_DIR / asset.get_file_name()
    )
    cached_manifest.add_asset(asset)
    ManifestStore.save_to_json(cached_manifest, env.user_paths.CACHED_MANIFEST)
