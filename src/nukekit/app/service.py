"""
Application service - orchestrates workflows with dependency injection.

This is the entry point for all use cases. It handles:
- Dependency injection
- Error handling and translation
- Logging
- Transaction management
"""

from typing import Any

from ..core.exceptions import (
    NukeKitError,
    UserAbortedError,
    WorkflowError,
)
from ..workflows import install_workflow, publish_workflow, scan_workflow
from .container import Dependencies


class ApplicationService:
    """
    Application service that orchestrates all workflows.

    This is the single entry point for CLI and GUI. It handles:
    - Creating/injecting dependencies
    - Error handling
    - Logging
    - Result formatting
    """

    def __init__(self, deps: Dependencies):
        """
        Initialize application service.

        Args:
            deps: Application dependencies
        """
        self.deps = deps
        self.logger = deps.logger

    def publish_asset(
        self, scan_local: bool = False, interactive: bool = True
    ) -> dict[str, Any]:
        """
        Execute publish workflow.

        Args:
            scan_local: If True, scan current directory; else scan Nuke dir
            interactive: If True, prompt user for selection

        Returns:
            Result dictionary with status and data

        Raises:
            WorkflowError: If workflow fails
            UserAbortedError: If user cancels
        """
        self.logger.info("Starting publish workflow")

        try:
            result = publish_workflow.execute(
                deps=self.deps, scan_local=scan_local, interactive=interactive
            )

            self.logger.info(f"Published {result['asset']}")
            return {
                "status": "success",
                "asset": result["asset"],
                "message": f"Successfully published {result['asset']}",
            }

        except UserAbortedError:
            self.logger.info("Publish cancelled by user")
            raise

        except NukeKitError as e:
            self.logger.error(f"Publish failed: {e}")
            raise WorkflowError(f"Publish failed: {e}") from e

        except Exception as e:
            self.logger.exception("Unexpected error during publish")
            raise WorkflowError(f"Unexpected error: {e}") from e

    def install_asset(
        self,
        asset_name: str | None = None,
        version: str | None = None,
        interactive: bool = True,
    ) -> dict[str, Any]:
        """
        Execute install workflow.

        Args:
            asset_name: Optional specific asset to install (not yet supported)
            version: Optional specific version (not yet supported)
            interactive: If True, prompt user for selection

        Returns:
            Result dictionary with status and message

        Raises:
            WorkflowError: If workflow fails
            UserAbortedError: If user cancels
        """
        self.logger.info("Starting install workflow")

        try:
            result = install_workflow.execute(deps=self.deps, interactive=interactive)

            self.logger.info(f"Installed {result['asset']}")
            return {
                "status": "success",
                "asset": result["asset"],
                "message": f"Successfully installed {result['asset']}",
            }

        except UserAbortedError:
            self.logger.info("Install cancelled by user")
            raise

        except NukeKitError as e:
            self.logger.error(f"Install failed: {e}")
            raise WorkflowError(f"Install failed: {e}") from e

        except Exception as e:
            self.logger.exception("Unexpected error during install")
            raise WorkflowError(f"Install failed: {e}") from e

    def scan_assets(self, location: str = "local") -> dict[str, Any]:
        """
        Execute scan workflow.

        Args:
            location: "local" to scan NUKE_DIR, "remote" for repository manifest

        Returns:
            Result dict with 'assets' (manifest data) and 'count'
        """
        self.logger.info("Starting scan workflow", extra={"location": location})

        try:
            result = scan_workflow.execute(deps=self.deps, location=location)
            self.logger.info(f"Scan found {result['count']} assets")
            return {
                "status": "success",
                "assets": result["assets"],
                "count": result["count"],
            }
        except NukeKitError as e:
            self.logger.error(f"Scan failed: {e}")
            raise WorkflowError(f"Scan failed: {e}") from e
        except Exception as e:
            self.logger.exception("Unexpected error during scan")
            raise WorkflowError(f"Scan failed: {e}") from e
