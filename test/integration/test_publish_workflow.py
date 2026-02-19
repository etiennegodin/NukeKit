from nukekit.core import Asset, ManifestStore, Repository, copy


def test_publish_asset(sample_asset: Asset, sample_config: dict):
    repo = Repository.from_config(sample_config)
    repo_manifest = ManifestStore.load_from_json(repo.manifest_path)

    destination_path = repo.get_asset_path(sample_asset)
    copy.copy_asset(sample_asset.source_path, destination_path)

    repo_manifest.add_asset(sample_asset)
    ManifestStore.save_to_json(repo_manifest, repo.manifest_path)
