"""
Directory scanner for discovering Git repositories.

This module provides functionality to traverse directory trees and identify
all Git repositories within them.
"""

from pathlib import Path
from typing import List, Set
from .exceptions import ScanError


class RepositoryScanner:
    """Scans directories to find Git repositories."""

    def __init__(
        self,
        root_path: str,
        max_depth: int = 10,
        exclude_patterns: List[str] | None = None,
    ):
        """
        Initialize the repository scanner.

        Args:
            root_path: Root directory to start scanning from
            max_depth: Maximum directory depth to traverse
            exclude_patterns: List of directory names to exclude from scanning
        """
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.exclude_patterns: Set[str] = set(exclude_patterns or [])

        # Add common patterns to exclude by default
        default_excludes = {
            "node_modules",
            "__pycache__",
            ".venv",
            "venv",
            ".tox",
            "build",
            "dist",
        }
        self.exclude_patterns.update(default_excludes)

    def scan(self) -> List[Path]:
        """
        Scan for Git repositories.

        Returns:
            List of paths to Git repositories found

        Raises:
            ScanError: If there's an error during scanning
        """
        if not self.root_path.exists():
            raise ScanError(f"Path does not exist: {self.root_path}")

        if not self.root_path.is_dir():
            raise ScanError(f"Path is not a directory: {self.root_path}")

        repositories: List[Path] = []

        try:
            self._scan_directory(self.root_path, 0, repositories)
        except PermissionError as e:
            raise ScanError(f"Permission denied: {e}")
        except Exception as e:
            raise ScanError(f"Error during scan: {e}")

        return sorted(repositories)

    def _scan_directory(
        self, directory: Path, current_depth: int, repositories: List[Path]
    ) -> None:
        """
        Recursively scan a directory for Git repositories.

        Args:
            directory: Directory to scan
            current_depth: Current depth in the directory tree
            repositories: List to append found repositories to
        """
        if current_depth > self.max_depth:
            return

        # Check if this directory is a Git repository
        git_dir = directory / ".git"
        if git_dir.exists() and git_dir.is_dir():
            repositories.append(directory)
            # Don't scan inside Git repositories
            return

        # Scan subdirectories
        try:
            for entry in directory.iterdir():
                # Skip files
                if not entry.is_dir():
                    continue

                # Skip symbolic links to avoid circular references
                if entry.is_symlink():
                    continue

                # Skip excluded directories
                if entry.name in self.exclude_patterns:
                    continue

                # Skip hidden directories (starting with .)
                if entry.name.startswith("."):
                    continue

                # Recursively scan subdirectory
                self._scan_directory(entry, current_depth + 1, repositories)

        except PermissionError:
            # Skip directories we don't have permission to read
            pass
        except OSError:
            # Skip directories with other OS errors
            pass

    def is_git_repository(self, path: Path) -> bool:
        """
        Check if a path is a Git repository.

        Args:
            path: Path to check

        Returns:
            True if the path is a Git repository, False otherwise
        """
        git_dir = path / ".git"
        return git_dir.exists() and git_dir.is_dir()
