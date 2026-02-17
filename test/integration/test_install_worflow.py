"""

def test_install_asset(tmp_path, sample_asset, sample_repo):
    local_manifest = Manifest.from_json(tmp_path / "local_manifest.json")
    assert installer.install_asset_from_repo(
        sample_repo, local_manifest, sample_asset, destination_path=tmp_path
    )
    assert (
        sample_asset
        == local_manifest.data["Gizmo"][sample_asset.name][sample_asset.version]
    )
    assert local_manifest.ROOT.exists()
"""
