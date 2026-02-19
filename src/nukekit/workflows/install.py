from ..core import (
    EnvContext,
    ManifestStore,
    Repository,
    console,
    copy,
)


def install_workflow(args, env: EnvContext):
    # 1. Setup repository (directory structure)
    repository = Repository.from_config(env.config)

    # 2. Load manifests (persistence layer)
    repo_manifest = ManifestStore.load_from_json(repository.manifest_path)
    cached_manifest = ManifestStore.load_from_json(env.user_paths.CACHED_MANIFEST)

    # 3. User chooses asset
    asset = console.choose_menu(repo_manifest.data)

    # 4. Install locally
    copy.copy_asset(
        repository.get_asset_path(asset),
        env.user_paths.NUKE_KIT_DIR / asset.get_file_name(),
    )
    asset.set_install_status("local")

    # 5. Update local manifest and save
    cached_manifest.add_asset(asset)
    ManifestStore.save_to_json(cached_manifest, env.user_paths.CACHED_MANIFEST)
