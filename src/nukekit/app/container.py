"""
Dependency injection container.

Manages all application dependencies and their lifecycles.
"""

import logging
from dataclasses import dataclass

from ..core import Manifest, ManifestStore, Repository
from ..core.exceptions import ConfigurationError
from ..utils import UserPaths, init_logger


@dataclass
class Dependencies:
    """
    Container for application dependencies.

    All dependencies are created here and injected into workflows.
    Makes testing easy (just inject mocks) and ensures consistent setup.
    """

    # Core components
    repository: Repository
    user_paths: UserPaths
    config: dict
    logger: logging.Logger

    # Manifests
    repo_manifest: Manifest | None = None
    cached_manifest: Manifest | None = None

    @classmethod
    def create(
        cls, config: dict, logger: logging.Logger | None = None
    ) -> "Dependencies":
        """
        Create dependencies from configuration.

        Args:
            config: Configuration dictionary
            logger: Optional logger (creates default if None)

        Returns:
            Initialized dependencies

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if logger is None:
            logger = init_logger()

        # Validate config
        cls._validate_config(config)

        # Create core components
        repository = Repository.from_config(config)
        user_paths = UserPaths()

        # Load manifests
        repo_manifest = ManifestStore.load_from_json(repository.manifest_path)
        cached_manifest = ManifestStore.load_from_json(user_paths.CACHED_MANIFEST)

        return cls(
            repository=repository,
            user_paths=user_paths,
            config=config,
            logger=logger,
            repo_manifest=repo_manifest,
            cached_manifest=cached_manifest,
        )

    @staticmethod
    def _validate_config(config: dict) -> None:
        """Validate configuration has required keys."""
        required = ["repository"]
        missing = [key for key in required if key not in config]

        if missing:
            raise ConfigurationError(
                f"Missing required configuration keys: {', '.join(missing)}"
            )

    def reload_manifests(self) -> None:
        """Reload manifests from disk."""
        self.repo_manifest = ManifestStore.load_from_json(self.repository.manifest_path)
        self.cached_manifest = ManifestStore.load_from_json(
            self.user_paths.CACHED_MANIFEST
        )
