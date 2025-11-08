"""
Logging system for Gitty Up.

Provides file-based logging with rotation for debugging and audit trails.
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class GittyUpLogger:
    """Logger for Gitty Up operations."""

    def __init__(self, log_dir: Optional[Path] = None, enabled: bool = True):
        """
        Initialize the logger.

        Args:
            log_dir: Directory to store log files. If None, uses default location.
            enabled: Whether logging is enabled
        """
        self.enabled = enabled
        self.logger = logging.getLogger("gittyup")
        self.logger.setLevel(logging.DEBUG if enabled else logging.CRITICAL)

        # Don't add handlers if logging is disabled
        if not enabled:
            return

        # Remove any existing handlers
        self.logger.handlers.clear()

        # Determine log directory
        if log_dir is None:
            log_dir = self._get_default_log_dir()

        # Create log directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)

        # Set up file handler with rotation
        log_file = log_dir / "gittyup.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10,  # Keep last 10 log files
        )
        file_handler.setLevel(logging.DEBUG)

        # Set up formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)

        # Add handler to logger
        self.logger.addHandler(file_handler)

        # Log initialization
        self.info("Gitty Up logger initialized")

    def _get_default_log_dir(self) -> Path:
        """
        Get the default log directory.

        Returns:
            Path to default log directory
        """
        # Check for XDG_DATA_HOME first (Linux standard)
        data_home = os.environ.get("XDG_DATA_HOME")
        if data_home:
            log_dir = Path(data_home) / "gittyup" / "logs"
        else:
            # Fall back to platform-specific locations
            home = Path.home()
            if os.name == "nt":  # Windows
                log_dir = home / "AppData" / "Local" / "gittyup" / "logs"
            elif os.name == "posix":  # macOS/Linux
                log_dir = home / ".local" / "share" / "gittyup" / "logs"
            else:
                # Fallback for unknown systems
                log_dir = home / ".gittyup" / "logs"

        return log_dir

    def debug(self, message: str) -> None:
        """Log a debug message."""
        if self.enabled:
            self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message."""
        if self.enabled:
            self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        if self.enabled:
            self.logger.warning(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        if self.enabled:
            self.logger.error(message)

    def exception(self, message: str) -> None:
        """Log an exception with traceback."""
        if self.enabled:
            self.logger.exception(message)

    def log_scan_start(self, path: str, max_depth: int) -> None:
        """Log the start of a repository scan."""
        self.info(f"Starting scan: path={path}, max_depth={max_depth}")

    def log_scan_complete(self, repo_count: int, duration: float) -> None:
        """Log the completion of a repository scan."""
        self.info(f"Scan complete: {repo_count} repositories found in {duration:.2f}s")

    def log_repo_update_start(self, repo_path: str) -> None:
        """Log the start of a repository update."""
        self.debug(f"Updating repository: {repo_path}")

    def log_repo_update_success(self, repo_path: str, message: str) -> None:
        """Log a successful repository update."""
        self.info(f"Update successful: {repo_path} - {message}")

    def log_repo_update_skip(self, repo_path: str, reason: str) -> None:
        """Log a skipped repository update."""
        self.info(f"Update skipped: {repo_path} - {reason}")

    def log_repo_update_error(self, repo_path: str, error: str) -> None:
        """Log a failed repository update."""
        self.error(f"Update failed: {repo_path} - {error}")

    def log_operation_summary(
        self, total: int, updated: int, skipped: int, errors: int, duration: float
    ) -> None:
        """Log the summary of all operations."""
        self.info(
            f"Operation complete: total={total}, updated={updated}, "
            f"skipped={skipped}, errors={errors}, duration={duration:.2f}s"
        )

    def get_log_file_path(self) -> Optional[Path]:
        """
        Get the path to the current log file.

        Returns:
            Path to log file, or None if logging is disabled
        """
        if not self.enabled or not self.logger.handlers:
            return None

        for handler in self.logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                return Path(handler.baseFilename)

        return None

