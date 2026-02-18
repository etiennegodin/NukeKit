from ..core import (
    EnvContext,
    ManifestStore,
    Repository,
    console,
    installer,
)


def install(args, env: EnvContext):
    # 1. Setup repository (directory structure)
    repo = Repository.from_config(env.config)

    # 2. Load manifests (persistence layer)
    repo_manifest = ManifestStore.load_from_json(repo.manifest_path)
    cached_manifest = ManifestStore.load_from_json(env.user_paths.CACHED_MANIFEST)

    # 3. User chooses asset
    asset = console.choose_menu(repo_manifest.data)

    # 4. Install locally
    installer.install_asset_from_repo(repo, asset)
    asset.set_install_status("local")

    # 5. Update local manifest and save
    cached_manifest.add_asset(asset)
    ManifestStore.save_to_json(cached_manifest, env.user_paths.CACHED_MANIFEST)
