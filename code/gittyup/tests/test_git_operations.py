"""
Tests for the git operations module.
"""

import pytest
from unittest.mock import patch, MagicMock
import subprocess
from gittyup.git_operations import GitOperations
from gittyup.exceptions import GitNotFoundError


class TestGitOperations:
    """Test suite for GitOperations class."""

    def test_check_git_available_success(self):
        """Test checking Git availability when Git is installed."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert GitOperations.check_git_available() is True
            mock_run.assert_called_once()

    def test_check_git_available_not_found(self):
        """Test checking Git availability when Git is not installed."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            assert GitOperations.check_git_available() is False

    def test_check_git_available_subprocess_error(self):
        """Test checking Git availability when subprocess fails."""
        with patch("subprocess.run", side_effect=subprocess.SubprocessError):
            assert GitOperations.check_git_available() is False

    def test_ensure_git_available_success(self):
        """Test ensure_git_available when Git is available."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            # Should not raise an exception
            GitOperations.ensure_git_available()

    def test_ensure_git_available_raises_error(self):
        """Test ensure_git_available raises error when Git is not available."""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            with pytest.raises(GitNotFoundError, match="Git is not installed"):
                GitOperations.ensure_git_available()

    def test_pull_repository_success(self, tmp_path):
        """Test successful repository pull."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="Updating...\nFast-forward", stderr=""
            )
            success, message = GitOperations.pull_repository(tmp_path)

            assert success is True
            assert message == "Successfully updated"
            mock_run.assert_called_once()

    def test_pull_repository_already_up_to_date(self, tmp_path):
        """Test pulling repository that's already up to date."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="Already up to date.", stderr="")
            success, message = GitOperations.pull_repository(tmp_path)

            assert success is True
            assert message == "Already up to date"

    def test_pull_repository_error(self, tmp_path):
        """Test pulling repository with error."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1, stdout="", stderr="fatal: not a git repository"
            )
            success, message = GitOperations.pull_repository(tmp_path)

            assert success is False
            assert "fatal" in message.lower()

    def test_pull_repository_timeout(self, tmp_path):
        """Test pulling repository with timeout."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("git", 30)):
            success, message = GitOperations.pull_repository(tmp_path)

            assert success is False
            assert "timed out" in message.lower()

    def test_pull_repository_subprocess_error(self, tmp_path):
        """Test pulling repository with subprocess error."""
        with patch("subprocess.run", side_effect=subprocess.SubprocessError("error")):
            success, message = GitOperations.pull_repository(tmp_path)

            assert success is False
            assert "error" in message.lower()

    def test_get_repository_status_clean(self, tmp_path):
        """Test getting status of a clean repository."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            is_clean, status = GitOperations.get_repository_status(tmp_path)

            assert is_clean is True
            assert status == "Clean"

    def test_get_repository_status_dirty(self, tmp_path):
        """Test getting status of a dirty repository."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=" M file.txt\n", stderr="")
            is_clean, status = GitOperations.get_repository_status(tmp_path)

            assert is_clean is False
            assert status == "Uncommitted changes"

    def test_get_repository_status_error(self, tmp_path):
        """Test getting status with error."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")
            is_clean, status = GitOperations.get_repository_status(tmp_path)

            assert is_clean is False
            assert "Unable to get status" in status

    def test_get_repository_status_timeout(self, tmp_path):
        """Test getting status with timeout."""
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("git", 5)):
            is_clean, status = GitOperations.get_repository_status(tmp_path)

            assert is_clean is False
            assert "Timeout" in status

    def test_has_upstream_true(self, tmp_path):
        """Test checking upstream when it exists."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert GitOperations.has_upstream(tmp_path) is True

    def test_has_upstream_false(self, tmp_path):
        """Test checking upstream when it doesn't exist."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            assert GitOperations.has_upstream(tmp_path) is False

    def test_has_upstream_error(self, tmp_path):
        """Test checking upstream with subprocess error."""
        with patch("subprocess.run", side_effect=subprocess.SubprocessError):
            assert GitOperations.has_upstream(tmp_path) is False

    def test_pull_repository_custom_timeout(self, tmp_path):
        """Test that custom timeout is respected."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            GitOperations.pull_repository(tmp_path, timeout=60)

            # Check that timeout was passed to subprocess.run
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs["timeout"] == 60
