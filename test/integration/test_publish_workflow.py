from nukekit.core import Asset, ManifestStore, Repository, publisher


def test_publish_asset(sample_asset: Asset, sample_config: dict):
    # env = envContextBuilder()
    repo = Repository.from_config(sample_config)
    repo_manifest = ManifestStore.load_from_json(repo.manifest_path)
    # cached_manifest = ManifestStore.load_from_json(env.user_paths.CACHED_MANIFEST)

    destination_path = repo.get_asset_path(sample_asset)
    publisher.publish_asset_to_repo(sample_asset.source_path, destination_path)

    repo_manifest.add_asset(sample_asset)
    ManifestStore.save_to_json(repo_manifest)
