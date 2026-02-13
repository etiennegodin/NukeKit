from nukekit.core import Manifest, Repository, publisher


def test_publish_asset(sample_asset, sample_config):
    repo = Repository(sample_config)
    manifest = Manifest.from_json(repo.MANIFEST_PATH)
    repo.add_manifest(manifest)
    publisher.publish_asset_to_repo(repo, sample_asset)
    assert (
        sample_asset
        == repo.manifest.data["Gizmo"][sample_asset.name][sample_asset.version]
    )
