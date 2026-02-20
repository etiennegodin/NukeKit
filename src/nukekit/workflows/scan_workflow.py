"""
Scan workflow with dependency injection.

This is pure business logic - no I/O creation, no error handling.
The ApplicationService handles those concerns.
"""

import logging

from ..app.container import Dependencies
from ..core import ManifestStore

logger = logging.getLogger(__name__)


def execute(
    deps: Dependencies,
    location: str = "local",
) -> dict:
    """
    Execute scan workflow.

    Scans for assets either from the local filesystem (NUKE_DIR) or from
    the repository manifest. For local scans, merges with cached manifest
    metadata when available.

    Args:
        deps: Injected dependencies containing user paths and manifests.
        location: "local" to scan NUKE_DIR filesystem, "remote" to use
            repository manifest.

    Returns:
        Dictionary with:
            - 'assets': Nested dict from Manifest.to_dict()
            - 'count': Total number of asset versions found

    Raises:
        ValueError: If location is invalid or repository manifest not loaded.
    """
    if location == "local":
        if deps.cached_manifest is None:
            cached = None
        else:
            cached = deps.cached_manifest
        manifest = ManifestStore.load_from_filesystem(
            deps.user_paths.NUKE_DIR,
            cached_manifest=cached,
        )
    elif location == "remote":
        if deps.repo_manifest is None:
            raise ValueError("Repository manifest not loaded")
        manifest = deps.repo_manifest
    else:
        raise ValueError(f"Unknown scan location: {location}")

    data = manifest.to_dict()
    count = sum(
        len(versions) for type_data in data.values() for versions in type_data.values()
    )

    return {"assets": data, "count": count}
