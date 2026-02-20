"""
Publish workflow with dependency injection.

This is pure business logic - no I/O creation, no error handling.
The ApplicationService handles those concerns.
"""

import logging
from pathlib import Path

from ..app.container import Dependencies
from ..core import (
    Manifest,
    ManifestStore,
    console,
    copy,
    scanner,
)
from ..core.exceptions import UserAbortedError
from ..core.validator import resolve_version

logger = logging.getLogger(__name__)


def execute(
    deps: Dependencies, scan_local: bool = False, interactive: bool = True
) -> dict:
    """
    Execute publish workflow.

    Scans for assets (local directory or NUKE_DIR), prompts user to select one,
    resolves version conflicts, ensures metadata, publishes to repository,
    and installs locally.

    Args:
        deps: Injected dependencies containing repository, manifests, and user paths.
        scan_local: If True, scan current directory (Path.cwd()); else scan NUKE_DIR.
        interactive: If True, prompt user for asset selection.
            If False, raises NotImplementedError (non-interactive not yet supported).

    Returns:
        Dictionary with 'asset' key containing the published Asset instance.

    Raises:
        UserAbortedError: If user cancels during selection.
        NotImplementedError: If interactive=False (not yet supported).
        ValidationError: If asset validation fails (currently commented out).
    """

    # Get assets to choose from
    if scan_local:
        data = scanner.scan_folder(Path.cwd())
        local_state = Manifest.from_dict(data)
    else:
        local_state = ManifestStore.load_from_filesystem(
            deps.user_paths.NUKE_DIR, cached_manifest=deps.cached_manifest
        )

    # User selects asset
    if interactive:
        asset = console.choose_asset_fuzzy(local_state.to_dict(), prompt="Publish")
        if asset is None:
            raise UserAbortedError("User cancelled asset selection")
    else:
        # For GUI or programmatic use
        raise NotImplementedError("Non-interactive publish not yet supported")

    # Resolve version conflicts
    asset = resolve_version(deps.repo_manifest.get_latest_asset_version(asset), asset)

    # Ensure metadata
    asset.ensure_metadata()
    asset.ensure_message()

    # Validate asset

    """
    is_valid, errors = AssetValidator.validate_asset(asset)
    if not is_valid:
        raise ValidationError(
            f"Asset validation failed: {', '.join(errors)}", details={"errors": errors}
        )

    """
    # Publish to repository
    destination_path = deps.repository.get_asset_path(asset)
    copy.copy_asset(asset.source_path, destination_path)

    # Upate asset status
    asset.set_publish_status("published")

    # Update repository manifest and save
    deps.repo_manifest.add_asset(asset)
    ManifestStore.save_to_json(deps.repo_manifest, deps.repository.manifest_path)

    # Install locally
    copy.copy_asset(
        deps.repository.get_asset_path(asset),
        deps.user_paths.NUKE_KIT_DIR / asset.get_file_name(),
    )

    # Update local manifest
    deps.cached_manifest.add_asset(asset)
    ManifestStore.save_to_json(deps.cached_manifest, deps.user_paths.CACHED_MANIFEST)

    return {"asset": asset}
