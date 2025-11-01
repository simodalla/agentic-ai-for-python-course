"""
Git operations module for executing Git commands on repositories.

This module provides functionality to safely execute Git operations,
particularly pulling changes from remote repositories.
"""

import subprocess
from pathlib import Path
from typing import Tuple
from .exceptions import GitNotFoundError, RepositoryError


class GitOperations:
    """Handles Git operations on repositories."""

    @staticmethod
    def check_git_available() -> bool:
        """
        Check if Git is installed and available in PATH.

        Returns:
            True if Git is available, False otherwise
        """
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    @staticmethod
    def ensure_git_available() -> None:
        """
        Ensure Git is available, raise error if not.

        Raises:
            GitNotFoundError: If Git is not installed or not in PATH
        """
        if not GitOperations.check_git_available():
            raise GitNotFoundError(
                "Git is not installed or not found in PATH. "
                "Please install Git: https://git-scm.com/downloads"
            )

    @staticmethod
    def pull_repository(repo_path: Path, timeout: int = 30) -> Tuple[bool, str]:
        """
        Pull changes from remote repository.

        Args:
            repo_path: Path to the Git repository
            timeout: Timeout in seconds for the operation

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Execute git pull --all
            result = subprocess.run(
                ["git", "pull", "--all"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            # Check if successful
            if result.returncode == 0:
                output = result.stdout.strip()
                # Check if already up to date
                if "Already up to date" in output or "Already up-to-date" in output:
                    return True, "Already up to date"
                else:
                    return True, "Successfully updated"
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                return False, error_msg

        except subprocess.TimeoutExpired:
            return False, "Operation timed out"
        except subprocess.SubprocessError as e:
            return False, f"Git error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    @staticmethod
    def get_repository_status(repo_path: Path) -> Tuple[bool, str]:
        """
        Get the status of a Git repository.

        Args:
            repo_path: Path to the Git repository

        Returns:
            Tuple of (is_clean: bool, status_message: str)
        """
        try:
            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode != 0:
                return False, "Unable to get status"

            # If output is empty, repository is clean
            if not result.stdout.strip():
                return True, "Clean"
            else:
                return False, "Uncommitted changes"

        except subprocess.TimeoutExpired:
            return False, "Timeout checking status"
        except subprocess.SubprocessError:
            return False, "Error checking status"

    @staticmethod
    def has_upstream(repo_path: Path) -> bool:
        """
        Check if the current branch has an upstream configured.

        Args:
            repo_path: Path to the Git repository

        Returns:
            True if upstream is configured, False otherwise
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "@{upstream}"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, subprocess.TimeoutExpired):
            return False

