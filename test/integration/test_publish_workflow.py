from nukekit.core import Asset, Repository, publisher


def test_publish_asset(sample_asset: Asset, sample_empty_repo: Repository):
    assert publisher.publish_asset_to_repo(sample_empty_repo, sample_asset)
    assert (
        sample_asset
        == sample_empty_repo.manifest.data["Gizmo"][sample_asset.name][
            sample_asset.version
        ]
    )
    assert sample_empty_repo.manifest.ROOT.exists()
