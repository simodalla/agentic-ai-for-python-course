"""
Custom exceptions for the Gitty Up application.
"""


class GittyUpError(Exception):
    """Base exception for all Gitty Up errors."""

    pass


class GitNotFoundError(GittyUpError):
    """Raised when Git is not installed or not found in PATH."""

    pass


class RepositoryError(GittyUpError):
    """Raised when there's an error with a Git repository."""

    pass


class ScanError(GittyUpError):
    """Raised when there's an error during directory scanning."""

    pass

