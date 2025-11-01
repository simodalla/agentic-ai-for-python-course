"""
Tests for the CLI module.
"""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from gittyup.cli import main
from gittyup.exceptions import GitNotFoundError


class TestCLI:
    """Test suite for CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_version_option(self):
        """Test --version flag."""
        result = self.runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help_option(self):
        """Test --help flag."""
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Gitty Up" in result.output
        assert "Update all Git repositories" in result.output

    @patch("gittyup.cli.GitOperations.ensure_git_available")
    def test_git_not_available(self, mock_ensure_git):
        """Test behavior when Git is not available."""
        mock_ensure_git.side_effect = GitNotFoundError("Git not found")
        
        result = self.runner.invoke(main, ["."])
        assert result.exit_code == 1
        assert "Git not found" in result.output

    @patch("gittyup.cli.GitOperations.ensure_git_available")
    @patch("gittyup.cli.RepositoryScanner")
    def test_no_repositories_found(self, mock_scanner, mock_ensure_git):
        """Test behavior when no repositories are found."""
        mock_ensure_git.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = []
        mock_scanner.return_value = mock_scanner_instance
        
        result = self.runner.invoke(main, ["."], catch_exceptions=False)
        # Exit code 0 is expected when no repos found (not an error)
        assert result.exit_code == 0

    @patch("gittyup.cli.GitOperations")
    @patch("gittyup.cli.RepositoryScanner")
    def test_dry_run_mode(self, mock_scanner, mock_git_ops):
        """Test --dry-run flag."""
        # Setup mocks
        mock_git_ops.ensure_git_available.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = [MagicMock(name="test-repo")]
        mock_scanner.return_value = mock_scanner_instance
        
        result = self.runner.invoke(main, ["--dry-run", "."])
        assert "DRY RUN MODE" in result.output

    @patch("gittyup.cli.GitOperations")
    @patch("gittyup.cli.RepositoryScanner")
    def test_exclude_option(self, mock_scanner, mock_git_ops):
        """Test --exclude option."""
        mock_git_ops.ensure_git_available.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = []
        mock_scanner.return_value = mock_scanner_instance
        
        result = self.runner.invoke(
            main, ["--exclude", "node_modules", "--exclude", "venv", "."]
        )
        
        # Check that scanner was called with exclude patterns
        call_kwargs = mock_scanner.call_args[1]
        assert "node_modules" in call_kwargs.get("exclude_patterns", [])
        assert "venv" in call_kwargs.get("exclude_patterns", [])

    @patch("gittyup.cli.GitOperations")
    @patch("gittyup.cli.RepositoryScanner")
    def test_max_depth_option(self, mock_scanner, mock_git_ops):
        """Test --max-depth option."""
        mock_git_ops.ensure_git_available.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = []
        mock_scanner.return_value = mock_scanner_instance
        
        result = self.runner.invoke(main, ["--max-depth", "5", "."])
        
        # Check that scanner was called with max_depth
        call_kwargs = mock_scanner.call_args[1]
        assert call_kwargs.get("max_depth") == 5

