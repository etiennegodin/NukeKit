"""
NukeKit exception hierarchy.

Provides structured error handling across the application.
"""


class NukeKitError(Exception):
    """
    Base exception for all NukeKit errors.

    All custom exceptions inherit from this to allow catching
    all NukeKit-specific errors.
    """

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


# Domain Layer Exceptions
class AssetError(NukeKitError):
    """Errors related to asset operations."""

    pass


class InvalidAssetError(AssetError):
    """Asset is invalid or malformed."""

    pass


class AssetNotFoundError(AssetError):
    """Asset doesn't exist."""

    pass


class VersionConflictError(AssetError):
    """Version conflict detected."""

    pass


class ManifestError(NukeKitError):
    """Errors related to manifest operations."""

    pass


class ManifestCorruptedError(ManifestError):
    """Manifest file is corrupted."""

    pass


class RepositoryError(NukeKitError):
    """Errors related to repository operations."""

    pass


class RepositoryNotFoundError(RepositoryError):
    """Repository doesn't exist."""

    pass


# Infrastructure Layer Exceptions
class StorageError(NukeKitError):
    """Errors related to storage operations."""

    pass


class FileOperationError(StorageError):
    """File operation failed."""

    pass


# Application Layer Exceptions
class WorkflowError(NukeKitError):
    """Errors during workflow execution."""

    pass


class ValidationError(NukeKitError):
    """Validation failed."""

    pass


class UserAbortedError(NukeKitError):
    """User cancelled the operation."""

    pass


# Configuration Exceptions
class ConfigurationError(NukeKitError):
    """Configuration is invalid or missing."""

    pass
