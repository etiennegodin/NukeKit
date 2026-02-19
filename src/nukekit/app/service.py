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
from ..workflows import publish_workflow
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
