from nukekit.core import Asset, ManifestStore, Repository, installer


def test_install_asset_from_repo(tmp_path, sample_asset: Asset, sample_config: dict):
    local_folder = tmp_path / "local"
    repo = Repository.from_config(sample_config)
    cached_manifest = ManifestStore.load_from_json(local_folder)

    installer.install_asset_from_repo(repo, sample_asset, local_folder)
    cached_manifest.add_asset(sample_asset)
    ManifestStore.save_to_json(cached_manifest, cached_manifest.source_path)

    asset_path = local_folder / f"{sample_asset}.gizmo"
    assert asset_path.exists()
    assert cached_manifest.source_path.exists()
