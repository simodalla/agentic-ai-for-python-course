"""
Tests for the CLI module.
"""

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
        assert "0.2.0" in result.output

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

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["."])
            assert result.exit_code == 1
            assert "Git not found" in result.output or "ERROR" in result.output

    @patch("gittyup.cli.GitOperations.ensure_git_available")
    @patch("gittyup.cli.RepositoryScanner")
    def test_no_repositories_found(self, mock_scanner, mock_ensure_git):
        """Test behavior when no repositories are found."""
        mock_ensure_git.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = []
        mock_scanner.return_value = mock_scanner_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["."])
            # Should exit successfully when no repos found
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

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["--dry-run", "."])
            assert "DRY RUN" in result.output or "Would " in result.output

    @patch("gittyup.cli.GitOperations")
    @patch("gittyup.cli.RepositoryScanner")
    def test_verbose_option(self, mock_scanner, mock_git_ops):
        """Test --verbose option."""
        mock_git_ops.ensure_git_available.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = []
        mock_scanner.return_value = mock_scanner_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["-v", "."])
            assert result.exit_code == 0

    @patch("gittyup.cli.GitOperations")
    @patch("gittyup.cli.RepositoryScanner")
    def test_quiet_option(self, mock_scanner, mock_git_ops):
        """Test --quiet option."""
        mock_git_ops.ensure_git_available.return_value = None
        mock_scanner_instance = MagicMock()
        mock_scanner_instance.scan.return_value = []
        mock_scanner.return_value = mock_scanner_instance

        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["-q", "."])
            assert result.exit_code == 0

    def test_verbose_and_quiet_conflict(self):
        """Test that --verbose and --quiet cannot be used together."""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(main, ["-v", "-q", "."])
            assert result.exit_code == 1
            assert "Cannot use both" in result.output or "verbose and quiet" in result.output
