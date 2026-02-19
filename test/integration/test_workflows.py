from pathlib import Path

import pytest
from nukekit.core import Asset, ManifestStore, Repository, copy, envContextBuilder


@pytest.mark.dependency(name="publish")
def test_publish_asset(
    sample_asset: Asset, sample_config: dict, sample_repo: Repository
):
    repo_manifest = ManifestStore.load_from_json(sample_repo.manifest_path)
    destination_path = sample_repo.get_asset_path(sample_asset)
    copy.copy_asset(sample_asset.source_path, destination_path)

    assert destination_path.exists(), f"Asset was not copied to {destination_path}"
    repo_manifest.add_asset(sample_asset)
    ManifestStore.save_to_json(repo_manifest, sample_repo.manifest_path)
    assert repo_manifest.source_path.exists()


@pytest.mark.dependency(depends=["publish"])
def test_install_asset_from_repo(
    tmp_path: Path, sample_asset: Asset, sample_repo: Repository
):
    env = envContextBuilder()
    local_folder = tmp_path / "local"
    local_folder.mkdir(exist_ok=True)

    cached_manifest = ManifestStore.load_from_json(env.user_paths.CACHED_MANIFEST)

    source_path = sample_repo.get_asset_path(sample_asset)
    destination_path = local_folder / sample_asset.get_file_name()
    print(f"\nDEBUG: {source_path}")
    assert source_path.exists()
    assert local_folder.exists()

    assert copy.copy_asset(source_path, destination_path)
    assert destination_path.exists()
    assert destination_path.is_file()

    cached_manifest.add_asset(sample_asset)
    ManifestStore.save_to_json(cached_manifest, cached_manifest.source_path)
    assert cached_manifest.source_path.exists()
